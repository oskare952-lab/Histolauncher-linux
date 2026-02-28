import os
import subprocess
import shutil

from uuid import uuid3, NAMESPACE_DNS
from core.settings import load_global_settings, get_base_dir
from server.yggdrasil import _get_username_and_uuid


def _native_subfolder_for_platform():
    return os.path.join("native", "linux")


def _join_classpath(base_dir, entries):
    return os.pathsep.join(os.path.join(base_dir, e) for e in entries)


def _find_java():
    java = shutil.which("java")
    if not java:
        raise RuntimeError("Java not found. Install it with pacman.")
    return java

def _load_data_ini(version_dir):
    data_ini = os.path.join(version_dir, "data.ini")
    if not os.path.exists(data_ini):
        return {}
    meta = {}
    with open(data_ini, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                meta[k.strip()] = v.strip()
    return meta


def _parse_mc_version(version_identifier):
    if "/" in version_identifier:
        _, base = version_identifier.split("/", 1)
    else:
        base = version_identifier
    base = base.split("-", 1)[0]
    parts = base.split(".")
    try:
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        return major, minor
    except Exception:
        return None, None


def _is_authlib_injector_needed(version_identifier):
    major, minor = _parse_mc_version(version_identifier)
    if major is None:
        return False
    if major > 1:
        return True
    if major == 1 and minor >= 13:
        return True
    return False


def username_to_uuid(username: str) -> str:
    offline_uuid = uuid3(NAMESPACE_DNS, "OfflinePlayer:" + username)
    return str(offline_uuid).replace("-", "")


def _expand_placeholders(args_str, version_identifier, game_dir, version_dir, global_settings, meta):
    username, auth_uuid_raw = _get_username_and_uuid()
    base_dir = get_base_dir()
    assets_root = os.path.join(base_dir, "assets")
    asset_index_name = meta.get("asset_index") or ""
    version_type = meta.get("version_type") or ""
    auth_uuid = (
        f"{auth_uuid_raw[0:8]}-{auth_uuid_raw[8:12]}-{auth_uuid_raw[12:16]}-"
        f"{auth_uuid_raw[16:20]}-{auth_uuid_raw[20:]}"
    )
    auth_access_token = "0"
    user_type = "legacy"
    user_properties = "{}"
    game_dir = game_dir or ""
    replacements = {
        "${auth_player_name}": username,
        "${auth_uuid}": auth_uuid,
        "${auth_access_token}": auth_access_token,
        "${user_type}": user_type,
        "${user_properties}": user_properties,
        "${version_name}": version_identifier,
        "${game_directory}": game_dir,
        "${gameDir}": game_dir,
        "${assets_root}": assets_root,
        "${assets_index_name}": asset_index_name,
        "${version_type}": version_type,
        "${resolution_width}": "854",
        "${resolution_height}": "480",
    }
    out = args_str
    for k, v in replacements.items():
        out = out.replace(k, v)
    args = out.split()
    filtered = []
    for arg in args:
        # drop explicit demo/gameDir flags and quickPlay placeholders
        if arg.startswith("--demo") or arg.startswith("--gameDir") or arg.startswith("--quickPlay"):
            continue
        # drop any unresolved placeholder tokens and also remove preceding flag if orphaned
        if "${" in arg or "}" in arg:
            # if last filtered token looks like a flag without '=', remove it too
            if filtered and filtered[-1].startswith("--") and "=" not in filtered[-1]:
                filtered.pop()
            continue
        filtered.append(arg)
    return " ".join(filtered)

def launch_version(version_identifier, username_override=None):

    base_dir = get_base_dir()
    clients_dir = os.path.join(base_dir, "clients")

    # Check if clients directory exists
    if not os.path.isdir(clients_dir):
        print("ERROR: Clients directory does not exist:", clients_dir)
        return False

    version_dir = None
    
    # Handle "category/folder" format
    if "/" in version_identifier:
        parts = version_identifier.replace("\\", "/").split("/", 1)
        if len(parts) == 2:
            requested_category, folder = parts[0], parts[1]
            # Find the actual category directory with matching case-insensitive name
            try:
                for cat in os.listdir(clients_dir):
                    if cat.lower() == requested_category.lower():
                        candidate = os.path.join(clients_dir, cat, folder)
                        if os.path.isdir(candidate):
                            version_dir = candidate
                            break
            except OSError as e:
                print("ERROR: Failed to scan clients directory:", e)
                return False
    
    # Fall back to search if not found or no "/" in identifier
    if not version_dir:
        try:
            for cat in os.listdir(clients_dir):
                p = os.path.join(clients_dir, cat, version_identifier)
                if os.path.isdir(p):
                    version_dir = p
                    break
        except OSError as e:
            print("ERROR: Failed to scan clients directory:", e)
            return False

    if not version_dir:
        print("ERROR: Version directory not found:", version_identifier)
        return False


    meta = _load_data_ini(version_dir)

    main_class = meta.get("main_class", "net.minecraft.client.Minecraft")

    classpath_entries = [p.strip() for p in (meta.get("classpath") or "client.jar").split(",") if p.strip()]
    
    classpath = _join_classpath(version_dir, classpath_entries)

    global_settings = load_global_settings()

    username = username_override or global_settings.get("username", "Player")

    min_ram = global_settings.get("min_ram", "512M")
    max_ram = global_settings.get("max_ram", "2048M")

    game_dir = os.path.expanduser("~/.minecraft")

    java_bin = _find_java()

    cmd = [
        java_bin,
        f"-Xms{min_ram}",
        f"-Xmx{max_ram}",
    ]

    # Native libs
    native_path = os.path.join(version_dir, "native/linux")

    if os.path.isdir(native_path):
        cmd.append(f"-Djava.library.path={native_path}")

    # classpath and main class
    cmd.extend(["-cp", classpath])
    cmd.append(main_class)

    if game_dir is not None:
        cmd.extend(["--gameDir", game_dir])

    # extra JVM arguments defined in metadata (contains version, accessToken, username, etc.)
    extra = meta.get("extra_jvm_args")
    if extra:
        expanded = _expand_placeholders(extra, version_identifier, game_dir, version_dir, global_settings, meta)
        if expanded:
            cmd.extend(expanded.split())
    else:
        # fallback for very old versions: just supply username
        cmd.append(username)


    print("Launching version:", version_identifier)
    print("Java:", java_bin)
    print("Command:")
    print(" ".join(cmd))

    subprocess.Popen(cmd, cwd=version_dir)

    return True