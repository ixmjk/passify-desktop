import os

from PyQt5.QtCore import QSettings, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QDesktopWidget,
    QDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QWidget,
)
from PyQt5.uic import loadUi

settings = QSettings("Passify", "Passify")


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)


class DoubleClickShowPassword(QLineEdit):
    def mouseDoubleClickEvent(self, event) -> None:
        if self.echoMode() == 0:  # Normal Mode
            self.setEchoMode(QLineEdit.Password)
        else:
            self.setEchoMode(QLineEdit.Normal)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()

        custom_action = QAction("Password Generator", self)
        custom_action.triggered.connect(self.customOptionClicked)
        menu.addAction(custom_action)

        menu.exec_(event.globalPos())

    def customOptionClicked(self):
        from password_generator import PasswordGenerator

        window = PasswordGenerator()
        window.setModal(True)
        window.show()


class CustomQWidget(QWidget):
    def __init__(self, ui_file_name, window_title):
        super().__init__()
        self.ui_file = os.path.join(settings.value("UI_DIRECTORY"), ui_file_name)
        self.ui = loadUi(self.ui_file, self)
        self.ui.setWindowTitle(window_title)
        self.ui.resize(
            settings.value("Width"),
            settings.value("Height"),
        )
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class CustomQMainWindow(QMainWindow):
    def __init__(self, ui_file_name, window_title):
        super().__init__()
        self.ui_file = os.path.join(settings.value("UI_DIRECTORY"), ui_file_name)
        self.ui = loadUi(self.ui_file, self)
        self.ui.setWindowTitle(window_title)
        self.ui.resize(
            settings.value("Width"),
            settings.value("Height"),
        )
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class CustomQDialog(QDialog):
    def __init__(self, ui_file_name, window_title, width=None, height=None):
        super().__init__()
        self.ui_file = os.path.join(settings.value("UI_DIRECTORY"), ui_file_name)
        self.ui = loadUi(self.ui_file, self)
        self.ui.setWindowTitle(window_title)
        if width and height:
            self.ui.resize(width, height)
        else:
            self.ui.resize(
                settings.value("Width"),
                settings.value("Height"),
            )
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
