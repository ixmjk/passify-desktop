from PyQt5.QtCore import QEvent, QSettings, Qt
from PyQt5.QtWidgets import QMessageBox

from custom_widgets import CustomQWidget
from utils import get_error_message, is_valid_email, post_request

settings = QSettings("Passify", "Passify")


class ForgetPassword(CustomQWidget):
    def __init__(self):
        super().__init__("forget_password.ui", "Passify - Reset password")
        self.ui.btn_submit.clicked.connect(self.send_password_reset_link)
        self.ui.lbl_sign_in.clicked.connect(self.go_to_sign_in)

    def validate_input(self):
        if not is_valid_email(self.ui.le_email.text()):
            raise Exception("Please enter a valid email address.")
        return {
            "email": self.ui.le_email.text(),
        }

    def send_password_reset_link(self):
        try:
            data = self.validate_input()
            response = post_request(settings.value("RESET_PASSWORD_ENDPOINT"), data)
            if response.status_code == 204:
                QMessageBox.information(
                    self,
                    "Password reset was successful",
                    "A password reset link was sent to your email address.",
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

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            if self.ui.le_email.text():
                self.send_password_reset_link()
        return super().event(event)
