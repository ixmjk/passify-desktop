import random
import string

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from custom_widgets import CustomQDialog

settings = QSettings("Passify", "Passify")


class PasswordGenerator(CustomQDialog):
    def __init__(self):
        super().__init__(
            "password_generator.ui", "Passify - Password Generator", 414, 130
        )
        self.ui.hs_length.valueChanged.connect(self.hsValueChanged)
        self.ui.sb_length.valueChanged.connect(self.sbValueChanged)
        self.ui.lbl_generate.clicked.connect(self.generate)
        self.ui.lbl_copy.clicked.connect(self.copy_to_clipboard)

        self.ui.cb_upper.stateChanged.connect(self.generate)
        self.ui.cb_lower.stateChanged.connect(self.generate)
        self.ui.cb_numbers.stateChanged.connect(self.generate)
        self.ui.cb_symbols.stateChanged.connect(self.generate)

        self.generate()

    def hsValueChanged(self, value):
        self.ui.sb_length.setValue(value)
        self.generate()

    def sbValueChanged(self, value):
        self.ui.hs_length.setValue(value)
        self.generate()

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.le_password.text())

    def generate(self):
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        numbers = string.digits
        symbols = string.punctuation

        all = ""

        if self.ui.cb_upper.isChecked():
            all += upper
        if self.ui.cb_lower.isChecked():
            all += lower
        if self.ui.cb_numbers.isChecked():
            all += numbers
        if self.ui.cb_symbols.isChecked():
            all += symbols

        if all:
            password = "".join(random.choices(all, k=self.ui.sb_length.value()))
            self.ui.le_password.setText(password)
        else:
            self.ui.le_password.setText(all)
