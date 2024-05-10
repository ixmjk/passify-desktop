import os

from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QShortcut

from custom_widgets import CustomQDialog
from utils import auth_get_request, auth_patch_request, get_error_message

settings = QSettings("Passify", "Passify")


class EditEntry(CustomQDialog):
    def __init__(self, id_url, width=None, height=None):
        super().__init__("entry.ui", "Passify - Edit Entry", width, height)
        self.ui_file = os.path.join(
            settings.value("UI_DIRECTORY"),
        )
        self.ui.le_password.setEchoMode(QLineEdit.Password)
        self.ui.btn_ok.clicked.connect(self.edit_entry)
        self.id_url = id_url
        self.populate_fields()

        # Adding keyboard shortcut Ctrl+G
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_G), self)
        shortcut.activated.connect(self.password_generator)

    def password_generator(self):
        from password_generator import PasswordGenerator

        password_generator_window = PasswordGenerator()
        password_generator_window.setModal(True)
        password_generator_window.show()

    def populate_fields(self):
        try:
            response = auth_get_request(self.id_url)
            if response.status_code == 200:
                fields = response.json()
                self.ui.le_title.setText(fields["title"])
                self.ui.le_username.setText(fields["username"])
                self.ui.le_password.setText(fields["password"])
                self.ui.le_url.setText(fields["url"])
                self.ui.te_notes.setPlainText(fields["notes"])
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

    def edit_entry(self):
        try:
            data = self.validate_input()
            response = auth_patch_request(self.id_url, data)
            if response.status_code == 200:  # ok
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
