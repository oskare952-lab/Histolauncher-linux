Due to Kerbal planning to add linux support to b1.4 this repo will be mostly useless and most likely remain outdated for a while but i will remove most windows and macos specific things from the official thing if i am not lazy (planning to atleast do b1.4) Also i will change every release to stable instead of pre-release so github actually shows it. Btw b1.2 and b1.3 are vibe coded yeah i know shame on me might change b1.4 but no promises you will have to wait and see also apologies for trash formatting on this part and the below docs may or may not be outdated as i dont really update it mostly copy paste and ai to make it more accurate.
# What is Histolauncher?
Histolauncher is a lightweight, community-driven launcher built to grow and help users play any versions of Minecraft they like.

It provides a clean, modern interface for browsing and launching a massive library of Minecraft clients, all officially from Mojang!

The goal is simple: make it easy for anyone to play any Minecraft version offline without having to risk searching for 100% clean launcher. Everything is organized, searchable, and ready to download & launch with just a few clicks.

Histolauncher is a passion project - built for easy access to Minecraft clients offline whenever.

**Note:** This is a Linux-only fork. For the official Windows/Mac version, visit:
- Official Website: **https://histolauncher.org**
- Backup Website: **https://histolauncher.pages.dev**
- Discord Server: **https://discord.gg/P8dddrXFkn** (Not for this fork)

**Important:** Do not ask for Linux support or help on the official Histolauncher Discord or websites, as this fork is not affiliated with the official project.

# Requirements
You will need:
- **Java** for the clients *(only **1** java required!)*:
  - **JRE 8** - used by versions **oldest - 1.16.5**
  - **JDK 11** - used by versions **1.17 - 1.17.1**
  - **JDK 17** - used by versions **1.18 - 1.20.4**
  - **JDK 21** *(recommended)* - used by versions **1.20.5 - latest**
- **Python 3.x** for the launcher
- **xdotool** (optional, for window detection): `sudo pacman -S xdotool` (or equivalent for your package manager)

## How to install:
### Java (8, 11, 17, 21):
- JRE 8 (**oldest - 1.16.5**):
  1. Go to the official download page: **https://www.java.com/download/manual.jsp**
  2. Choose Linux and the correct architecture (64‑bit for most modern systems).
  3. Run the installer and follow the on‑screen steps.
  4. Done! The clients should load once you try to launch them!
- JDK 11 (**1.17 - 1.17.1**):
  1. Go to the official download page: **https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html**
  2. Choose Linux and the correct architecture.
  3. Download the installer (you may need to sign in with an Oracle account).
  4. Run the installer and follow the instructions.
  5. Done! The clients should load once you try to launch them!
- JDK 17 (**1.18 - 1.20.4**):
  1. Go to the official download page: **https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html**
  2. Choose Linux and the correct architecture.
  3. Download the installer.
  4. Run the installer and follow the instructions.
  5. Done! The clients should load once you try to launch them!
- JDK 21 (*recommended*, **1.20.5 - latest**):
  1. Go to the official download page: **https://www.oracle.com/java/technologies/downloads/#java21**
  2. Choose Linux and the correct architecture (64‑bit for most modern systems).
  3. Run the installer and follow the on‑screen steps.
  4. Done! The clients should load once you try to launch them!

### Python 3.x:
1. Download from **https://www.python.org/downloads/**
2. Click on the latest release (should be a bugfix or security patch, pre-releases are probably not recommended)
3. Click on Linux
4. Follow the instructions the installer tells you
5. Done! The launcher should load once you try to open it!

# Customization
This fork is designed to be simple and Linux-focused. If you want to customize certain behaviors, you can edit the following functions in `launcher.py`:

- **Dark mode**: Edit the `is_dark_mode()` function in launcher.py (by default returns `False` for light mode)
- **Console visibility**: The `set_console_visible()` function is a no-op on Linux
- **Package installation**: The `run_install()` function uses pip and is in launcher.py
- **Python path refresh**: The `refresh_python_path()` function handles Linux package paths

# Opening the Launcher
To open the launcher, run `python3 launcher.py` from the project directory. Make sure you have the requirements installed.

Enjoy!
(Mostly AI slop btw but atleast it works)
