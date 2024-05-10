from PyQt5.QtCore import QEvent, QSettings, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QShortcut

from custom_widgets import CustomQWidget
from utils import get_error_message, is_valid_email, post_request

settings = QSettings("Passify", "Passify")


class SignUp(CustomQWidget):
    def __init__(self):
        super().__init__("sign_up.ui", "Passify - Sign up")
        self.ui.le_password.setEchoMode(QLineEdit.Password)
        self.ui.le_re_password.setEchoMode(QLineEdit.Password)
        self.ui.btn_sign_up.clicked.connect(self.sign_up)
        self.ui.lbl_sign_in.clicked.connect(self.go_to_sign_in)

        # Adding keyboard shortcut Ctrl+G
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_G), self)
        shortcut.activated.connect(self.password_generator)

    def password_generator(self):
        from password_generator import PasswordGenerator

        password_generator_window = PasswordGenerator()
        password_generator_window.setModal(True)
        password_generator_window.show()

    def sign_up(self):
        try:
            data = self.validate_input()
            response = post_request(settings.value("SIGN_UP_ENDPOINT"), data)
            if response.status_code == 201:
                QMessageBox.information(
                    self,
                    "Sign up",
                    "Account created successfully! A verification email has been sent to your email address.",
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

    def validate_input(self):
        if not (
            self.ui.le_first_name.text()
            and self.ui.le_last_name.text()
            and self.ui.le_email.text()
            and self.ui.le_password.text()
            and self.ui.le_re_password.text()
        ):
            raise Exception("Please fill in all the required fields.")
        if not is_valid_email(self.ui.le_email.text()):
            raise Exception("Please enter a valid email address.")
        if self.ui.le_password.text() != self.ui.le_re_password.text():
            raise Exception("Passwords don't match.")
        if len(self.ui.le_password.text()) < 8:
            raise Exception("Password must be at least 8 characters.")
        return {
            "first_name": self.ui.le_first_name.text(),
            "last_name": self.ui.le_last_name.text(),
            "email": self.ui.le_email.text(),
            "password": self.ui.le_password.text(),
            "re_password": self.ui.le_re_password.text(),
        }

    def go_to_sign_in(self):
        from sign_in import SignIn

        self.close()
        sign_in_window = SignIn()
        sign_in_window.show()

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            if (
                self.ui.le_first_name.text()
                and self.ui.le_last_name.text()
                and self.ui.le_email.text()
                and self.ui.le_password.text()
                and self.ui.le_re_password.text()
            ):
                self.sign_up()
            else:
                self.focusNextPrevChild(True)
        return super().event(event)
