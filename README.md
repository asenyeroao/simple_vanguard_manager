# Vanguard Manager

A modern GUI tool for managing Riot Vanguard anti-cheat system.

## Features

* 🎯 **Start/Stop Vanguard** - Easy toggle for Vanguard services
* 🔄 **Autostart Control** - Manage Vanguard autostart settings
* 🌍 **Multi-language** - English and Traditional Chinese support
* 🎨 **Multiple Themes** - Dark, Light, and Vanguard themes
* 🖱️ **Draggable Interface** - Frameless, modern design
* ⚙️ **Settings Panel** - Right-click gear icon for options

## Requirements

* Windows 10/11
* Administrator privileges (for Vanguard control)
* Python 3.7+ (for running from source)

## Quick Start

### Option 1: Download Release (Recommended)

1. Download `VanguardManager.exe` from releases
2. Right-click → "Run as administrator"
3. Enjoy!

### Option 2: Run from Source

1. Ensure Python 3.7+ is installed
2. Run `simple_vanguard_manager.py`
3. Make sure `Vanguard.png` is in the same folder if used in the UI

## Usage

* **Settings**: Click the ⚙️ gear icon in top-right
* **Close**: Click the × icon in top-right
* **Move**: Drag anywhere on the window
* **Toggle Vanguard**: Use the main buttons

## Themes

* **Dark Theme**: Modern dark interface
* **Light Theme**: Clean light interface
* **Vanguard Theme**: Red/black Riot Vanguard colors (default)

## Default Settings

* Language: English
* Theme: Vanguard Theme
* Update Interval: 3 seconds

## Technical Details

Built with:

* PyQt5 for GUI
* PyInstaller for executable packaging
* Windows Services API for Vanguard control

## License
This project is for educational purposes. Respect Riot Games' terms of service.

