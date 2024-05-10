from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QShortcut

from custom_widgets import CustomQDialog
from utils import auth_post_request, get_error_message

settings = QSettings("Passify", "Passify")


class AddEntry(CustomQDialog):
    def __init__(self, width=None, height=None):
        super().__init__("entry.ui", "Passify - Add Entry", width, height)
        self.ui.le_password.setEchoMode(QLineEdit.Password)
        self.ui.btn_ok.clicked.connect(self.add_entry)

        # Adding keyboard shortcut Ctrl+G
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_G), self)
        shortcut.activated.connect(self.password_generator)

    def password_generator(self):
        from password_generator import PasswordGenerator

        password_generator_window = PasswordGenerator()
        password_generator_window.setModal(True)
        password_generator_window.show()

    def validate_input(self):
        if not (
            self.ui.le_title.text()
            and self.ui.le_username.text()
            and self.ui.le_password.text()
        ):
            raise Exception("Please fill in all the required fields.")
        return {
            "title": self.ui.le_title.text(),
            "username": self.ui.le_username.text(),
            "password": self.ui.le_password.text(),
            "url": self.ui.le_url.text(),
            "notes": self.ui.te_notes.toPlainText(),
        }

    def add_entry(self):
        try:
            data = self.validate_input()
            response = auth_post_request(settings.value("MY_DATABASE_ENDPOINT"), data)
            if response.status_code == 201:  # created
                self.close()
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
