from datetime import datetime

from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QShortcut,
)

from custom_widgets import CustomQDialog, DoubleClickShowPassword
from utils import (
    auth_delete_request,
    auth_get_request,
    auth_post_request,
    auth_put_request,
    get_error_message,
    is_valid_email,
)

settings = QSettings("Passify", "Passify")


class PasswordInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Delete Account")
        self.setFixedSize(300, 100)

        layout = QFormLayout()

        label = QLabel("Enter your account password:")
        self.password_input = DoubleClickShowPassword()
        self.password_input.setEchoMode(QLineEdit.Password)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(
            self.accept
        )  # Close the dialog when the OK button is clicked

        layout.addWidget(label)
        layout.addWidget(self.password_input)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def getPassword(self):
        return self.password_input.text()


class Profile(CustomQDialog):
    def __init__(self):
        super().__init__("profile.ui", "Passify - Profile")
        self.ui.btn_save_name.clicked.connect(self.save_name)
        self.ui.btn_save_email.clicked.connect(self.save_email)
        self.ui.btn_save_password.clicked.connect(self.save_password)
        self.ui.btn_delete_account.clicked.connect(self.delete_account)
        self.ui.le_current_password_ce.setEchoMode(QLineEdit.Password)
        self.ui.le_current_password.setEchoMode(QLineEdit.Password)
        self.ui.le_new_password.setEchoMode(QLineEdit.Password)
        self.ui.le_re_new_password.setEchoMode(QLineEdit.Password)
        self.load_profile()

        # Adding keyboard shortcut Ctrl+G
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_G), self)
        shortcut.activated.connect(self.password_generator)

    def password_generator(self):
        from password_generator import PasswordGenerator

        password_generator_window = PasswordGenerator()
        password_generator_window.setModal(True)
        password_generator_window.show()

    def format_datetime(self, current_time_str):
        current_time = datetime.fromisoformat(current_time_str.replace("Z", "+00:00"))
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time

    def load_profile(self):
        try:
            response = auth_get_request(settings.value("PROFILE_ENDPOINT"))
            if response.status_code == 200:
                profile_info = response.json()
                self.ui.le_firstname.setText(profile_info["first_name"])
                self.ui.le_lastname.setText(profile_info["last_name"])
                self.ui.lbl_email.setText(profile_info["email"])
                self.ui.lbl_id.setText(profile_info["id"])
                self.ui.lbl_last_login.setText(
                    self.format_datetime(
                        profile_info["last_login"],
                    )
                )
                self.ui.lbl_date_joined.setText(
                    self.format_datetime(
                        profile_info["date_joined"],
                    )
                )
            else:
                error_message = get_error_message(response)
                QMessageBox.warning(
                    self,
                    f"Error {response.status_code}",
                    error_message,
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"{str(e)}",
            )

    def save_name(self):
        try:
            data = {
                "first_name": self.ui.le_firstname.text(),
                "last_name": self.ui.le_lastname.text(),
            }
            response = auth_put_request(
                settings.value("EDIT_PROFILE_ENDPOINT"),
                data,
            )
            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    "Save name",
                    "Profile name updated successfully!",
                )
            else:
                error_message = get_error_message(response)
                QMessageBox.warning(
                    self,
                    f"Error {response.status_code}",
                    error_message,
                )
            self.load_profile()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"{str(e)}",
            )

    def save_email(self):
        try:
            data = self.validate_email()
            response = auth_post_request(settings.value("CHANGE_EMAIL_ENDPOINT"), data)
            if response.status_code == 204:  # no content
                QMessageBox.information(
                    self,
                    "Change Email",
                    "Email changed successfully!",
                )
                self.ui.le_current_password_ce.clear()
                self.ui.le_new_email.clear()
                self.ui.le_re_new_email.clear()
                self.load_profile()
            else:
                error_message = get_error_message(response)
                QMessageBox.warning(
                    self,
                    f"Error {response.status_code}",
                    error_message,
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"{str(e)}",
            )

    def validate_email(self):
        if not (
            self.ui.le_current_password_ce.text()
            and self.ui.le_new_email.text()
            and self.ui.le_re_new_email.text()
        ):
            raise Exception("Please fill all the required fields.")
        if self.ui.le_new_email.text() != self.ui.le_re_new_email.text():
            raise Exception("Emails do not match.")
        if not is_valid_email(self.ui.le_new_email.text()):
            raise Exception("Please enter a valid email address.")
        if self.ui.lbl_email.text() == self.ui.le_new_email.text():
            raise Exception("New email is already in use.")
        return {
            "current_password": self.ui.le_current_password_ce.text(),
            "new_email": self.ui.le_new_email.text(),
            "re_new_email": self.ui.le_re_new_email.text(),
        }

    def save_password(self):
        try:
            data = self.validate_password()
            response = auth_post_request(
                settings.value("CHANGE_PASSWORD_ENDPOINT"), data
            )
            if response.status_code == 204:  # no content
                QMessageBox.information(
                    self,
                    "Change Password",
                    "Password changed successfully!",
                )
                self.ui.le_current_password.clear()
                self.ui.le_new_password.clear()
                self.ui.le_re_new_password.clear()
            else:
                error_message = get_error_message(response)
                QMessageBox.warning(
                    self,
                    f"Error {response.status_code}",
                    error_message,
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"{str(e)}",
            )

    def validate_password(self):
        if not (
            self.ui.le_current_password.text()
            and self.ui.le_new_password.text()
            and self.ui.le_re_new_password.text()
        ):
            raise Exception("Please fill all the required fields.")
        if self.ui.le_new_password.text() != self.ui.le_re_new_password.text():
            raise Exception("Passwords don't match.")
        if len(self.ui.le_new_password.text()) < 8:
            raise Exception("Password must be at least 8 characters.")
        return {
            "current_password": self.ui.le_current_password.text(),
            "new_password": self.ui.le_new_password.text(),
            "re_new_password": self.ui.le_re_new_password.text(),
        }

    def delete_account(self):
        try:
            dialog = PasswordInputDialog()
            if dialog.exec():
                current_password = dialog.getPassword()
                if current_password:
                    confirmation = QMessageBox.question(
                        None,
                        "Account Deletion Confirmation",
                        "Are you sure you want to delete your account? This action cannot be undone!",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No,
                    )
                    if confirmation == QMessageBox.Yes:
                        # Delete the account
                        data = {"current_password": current_password}
                        response = auth_delete_request(
                            settings.value("EDIT_PROFILE_ENDPOINT"), data
                        )
                        if response.status_code == 204:
                            QMessageBox.information(
                                self,
                                "Delete Account",
                                "Account deleted successfully.",
                            )
                            self.go_to_sign_in()
                        else:
                            error_message = get_error_message(response)
                            QMessageBox.warning(
                                self,
                                f"Error {response.status_code}",
                                error_message,
                            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"{str(e)}",
            )

    def go_to_sign_in(self):
        from sign_in import SignIn

        self.close()
        sign_in_window = SignIn()
        sign_in_window.show()
