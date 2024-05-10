# Passify Desktop

## Abstract

Passify Desktop is the desktop client application for the [Passify backend](https://github.com/ixmjk/passify), providing a user-friendly interface for managing passwords.

## Features

- **Cross-Platform Compatibility**: Enjoy compatibility with major operating systems including macOS, Linux, and Windows.
- **Password Generator**: Generate strong, random passwords to enhance security and simplify password creation.
- **Light/Dark Theme**: Personalize your experience by switching between light and dark themes.
- **Shortcuts**: Efficiently navigate and perform actions using keyboard and mouse shortcuts.

## Technologies

- [Python](https://www.python.org/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet?tab=readme-ov-file#qdarkstylesheet)
- [Requests](https://github.com/psf/requests?tab=readme-ov-file#requests)
- [PyInstaller](https://github.com/pyinstaller/pyinstaller?tab=readme-ov-file#pyinstaller-overview)

## Running the Project

To run the application:

```bash
pip install -r requirements.txt
```

```bash
python src/main.py
```

## Shortcuts

- Double tap on the password field to show/hide the password.
- Double tap on the URL to open it in the default browser.
- Double tap on the username or password to copy it to the clipboard.
- Press `Enter` to edit a selected entry.
- Press `Delete` to delete a selected entry.
- `Ctrl+R` to reload entries.
- `Ctrl+I` to add a new entry.
- `Ctrl+G` to open the password generator.
- `Ctrl+X` to export all passwords to a file.
- `Ctrl+P` to open the profile page.
- `Ctrl+Q` to sign out.

## Building the Project

To build the application into a standalone executable, use the following command:

```bash
pyinstaller --noconfirm --onefile --windowed --name "passify" --add-data "src;src/" --add-data "ui;ui/" --distpath . "src/main.py"
```

## Screenshots

![python_YQK2CuPWp9](https://github.com/ixmjk/passify/assets/66163456/2956a997-a5af-46b1-9eab-15fce949bc38)
