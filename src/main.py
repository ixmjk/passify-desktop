import os
import sys
from urllib.parse import urljoin

import qdarkstyle
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from database import Database
from sign_in import SignIn

if getattr(sys, "frozen", False):
    # used for compiled version
    UI_DIRECTORY = os.path.join(
        os.path.dirname(__file__),
        "ui",
    )
else:
    UI_DIRECTORY = os.path.join(
        os.path.dirname(__file__),
        "..",
        "ui",
    )


def load_settings():
    """
    Load and initialize application settings for Passify.

    This function uses PyQt5's QSettings to manage and store various configuration parameters for the Passify application.
    The settings include UI-related values such as the directory path for UI files, as well as window dimensions.
    Additionally, the function sets up endpoint-related configurations for communication with the backend API.

    Settings:
    - UI_DIRECTORY (str): Path to the directory containing UI files.
    - WIDTH (int): Width of the Passify application window.
    - HEIGHT (int): Height of the Passify application window.
    - DOMAIN (str): Domain of the backend API.
    - PROFILE_ENDPOINT (str): Endpoint for user profile.
    - EDIT_PROFILE_ENDPOINT (str): Endpoint for editing user profile.
    - CHANGE_EMAIL_ENDPOINT (str): Endpoint for changing user email.
    - CHANGE_PASSWORD_ENDPOINT (str): Endpoint for changing user password.
    - MY_DATABASE_ENDPOINT (str): Endpoint for user saved passwords.
    - SIGN_IN_ENDPOINT (str): Endpoint for user sign-in.
    - SIGN_UP_ENDPOINT (str): Endpoint for user sign-up.
    - RESET_PASSWORD_ENDPOINT (str): Endpoint for password reset.

    Example:
    ```python
    settings = load_settings()
    width = settings.value("WIDTH")
    height = settings.value("HEIGHT")
    ```

    Note:
    Make sure to call this function during the application initialization to ensure proper configuration.
    """
    settings = QSettings("Passify", "Passify")
    settings.setValue(
        "PROJECT_NAME",
        "Passify",
    )
    settings.setValue(
        "UI_DIRECTORY",
        UI_DIRECTORY,
        # Path to the UI files
    )
    settings.setValue(
        "WIDTH",
        800,
        # Width of the application window
    )
    settings.setValue(
        "HEIGHT",
        600,
        # Height of the application window
    )
    # Endpoints
    settings.setValue(
        "DOMAIN",
        "http://127.0.0.1:8000",
        # Domain of the API
    )
    settings.setValue(
        "PROFILE_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/users/me/"),
        # Endpoint for user profile
    )
    settings.setValue(
        "EDIT_PROFILE_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/users/me/"),
        # Endpoint for editing user profile
    )
    settings.setValue(
        "CHANGE_EMAIL_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/users/set_email/"),
        # Endpoint for changing user email
    )
    settings.setValue(
        "CHANGE_PASSWORD_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/users/set_password/"),
        # Endpoint for changing user password
    )
    settings.setValue(
        "MY_DATABASE_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/my/database/"),
        # Endpoint for user saved password
    )
    settings.setValue(
        "SIGN_IN_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/jwt/create/"),
        # Endpoint for user sign in
    )
    settings.setValue(
        "REFRESH_TOKEN_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/jwt/refresh/"),
        # Endpoint for user sign in
    )
    settings.setValue(
        "SIGN_UP_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/users/"),
        # Endpoint for user sign up
    )
    settings.setValue(
        "RESET_PASSWORD_ENDPOINT",
        urljoin(settings.value("DOMAIN"), "/auth/users/reset_password/"),
        # Endpoint for password reset
    )
    return settings


def main():
    settings = load_settings()
    app = QApplication(sys.argv)
    if settings.value("THEME") == "dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))
    if settings.value("ACCESS_TOKEN"):
        main_window = Database()
    else:
        main_window = SignIn()
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
