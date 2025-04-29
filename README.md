## UE4SS Installer GUI

This is an unofficial gui installer/manager for [UE4SS](https://github.com/UE4SS-RE/RE-UE4SS).\
UE4SS consists of an injectable LUA scripting system, SDK generator, live property editor, other dumping utilities for UE4/5 games and more.


### Download
- Click [here](https://github.com/Mythical-Github/ue4ss_installer_gui/releases/latest) to be redirected to the latest prebuilt release.


### Project Example:
<img src="https://github.com/user-attachments/assets/f6a0ec21-4ee3-4f52-8eeb-2b79cafddf98" alt="example" width="50%" height="50%">


### Features:
- Online/Offline support
- Localization
- Install
- Uninstall
- Install from zip
- Supports windows/linux
- Filterable version tag selection
- Filterable release archive to install selection
- Tags, and releases sorted by newest to oldest
- Open game executable directory in file browser button
- Automatic game detection
- Ability to provide extra directories to scan for games
- Ability to add games manually
- Handles multiple installs of one game
- Portable install filter
- Developer install filter
- Prerelease install filter
- Social buttons


### Join the Discord
If you have any problems, suggestions, or just want to chat, feel free to join the [Discord](https://discord.gg/EvUuAD4QvS)


### Suggestions
If you have ideas or suggestions for the tool feel free to open a [suggestions issue](https://github.com/Mythical-Github/ue4ss_installer_gui/issues) or mention it in the discord.


### Bug Reports
If you encounter a bug or issue, please submit a report on the [issues page](https://github.com/Mythical-Github/ue4ss_installer_gui/issues).
When creating an issue, please provide as much information as possible, including:
- Steps to reproduce the issue
- What you expect to happen, versus what is happening
- Any error messages or logs
- Your system operating system


### Contributing
Contributions are always appreciated, but please keep in mind the following:
- Before coding new features, try to make an issue to see if the idea/implementation needs any tweaking, or is out of scope
- Please make sure all code submissions pass all pre-commit checks
- If you're interested in adding new localization, it's as simple as, forking the dev branch
     you can copy, paste, and rename the en.json in both locations (there are two, one in assets/base/assets/localization, and one in src/ue4ss_installer_gui/assets/localization, translate, and submit


### Credits
Inspired by [MelonLoader.Installer](https://github.com/LavaGang/MelonLoader.Installer)


### Technologies:

- **[DearPyGUI](https://github.com/hoffstadt/DearPyGui)** - Dear PyGui: A fast and powerful Graphical User Interface Toolkit for Python with minimal dependencies.
- **[Hatch](https://github.com/pypa/hatch)** - Modern project management tool for Python.
- **[UV](https://github.com/astral-sh/uv)** - An extremely fast Python package and project manager, written in Rust.
- **[PyInstaller](https://github.com/pyinstaller/pyinstaller)** - Tool to convert Python programs into standalone executables.
- **[Ruff](https://github.com/astral-sh/ruff)** - Fast Python linter and code formatting tool.
- **[PyProjectDevTools](https://github.com/Mythical-Github/py_project_dev_tools)** - A set of generic tools for Python applications, using Hatch, UV, and PyInstaller.
- **[Pyright](https://github.com/microsoft/pyright)** - A fast type checker for Python.
- **[Precommit](https://github.com/pre-commit/pre-commit)** - A framework for managing and maintaining multi-language pre-commit hooks.
- **[Commitizen](https://github.com/commitizen-tools/commitizen)** - A tool to help you write consistent commit messages, and manage versioning.


### License:
[![license](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)](LICENSE)
