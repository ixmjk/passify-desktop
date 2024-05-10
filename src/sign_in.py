from PyQt5.QtCore import QEvent, QSettings, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QShortcut

from custom_widgets import CustomQWidget
from utils import get_error_message, is_valid_email, post_request

settings = QSettings("Passify", "Passify")


class SignIn(CustomQWidget):
    def __init__(self):
        super().__init__("sign_in.ui", "Passify - Sign In")
        self.ui.btn_sign_in.clicked.connect(self.sign_in)
        self.ui.lbl_forget_password.clicked.connect(self.go_to_forget_password)
        self.ui.lbl_sign_up.clicked.connect(self.go_to_sign_up)
        self.ui.le_password.setEchoMode(QLineEdit.Password)

        # Adding keyboard shortcut Ctrl+G
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_G), self)
        shortcut.activated.connect(self.password_generator)

    def password_generator(self):
        from password_generator import PasswordGenerator

        password_generator_window = PasswordGenerator()
        password_generator_window.setModal(True)
        password_generator_window.show()

    def sign_in(self):
        try:
            data = self.validate_input()
            response = post_request(settings.value("SIGN_IN_ENDPOINT"), data)
            if response.status_code == 200:
                ACCESS_TOKEN = response.json().get("access")
                REFRESH_TOKEN = response.json().get("refresh")
                settings.setValue("ACCESS_TOKEN", ACCESS_TOKEN)
                settings.setValue("REFRESH_TOKEN", REFRESH_TOKEN)
                self.go_to_database()
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
        if not (self.ui.le_email.text() and self.ui.le_password.text()):
            raise Exception("Please fill in all the required fields.")
        if not is_valid_email(self.ui.le_email.text()):
            raise Exception("Please enter a valid email address.")
        return {
            "email": self.ui.le_email.text(),
            "password": self.ui.le_password.text(),
        }

    def go_to_forget_password(self):
        from forget_password import ForgetPassword

        self.close()
        forget_password_page = ForgetPassword()
        forget_password_page.show()

    def go_to_sign_up(self):
        from sign_up import SignUp

        self.close()
        sign_up_window = SignUp()
        sign_up_window.show()

    def go_to_database(self):
        from database import Database

        self.close()
        sign_up_window = Database()
        sign_up_window.show()

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            if self.ui.le_email.text() and self.ui.le_password.text():
                self.sign_in()
            else:
                self.focusNextPrevChild(True)
        return super().event(event)
