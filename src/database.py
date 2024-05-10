import json
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QSettings, QTimer, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QHeaderView,
    QLabel,
    QMessageBox,
    QStyledItemDelegate,
    QTableWidget,
    QTableWidgetItem,
)

from add_entry import AddEntry
from custom_widgets import CustomQMainWindow
from edit_entry import EditEntry
from edit_profile import Profile
from utils import auth_delete_request, auth_get_request, get_error_message, post_request

settings = QSettings("Passify", "Passify")


class Database(CustomQMainWindow):
    def __init__(self):
        super().__init__("database.ui", "Passify - My Database")
        self.ui.actionExport.triggered.connect(self.export_data)
        self.ui.actionReload.triggered.connect(self.reload)
        self.ui.actionAddEntry.triggered.connect(self.add_entry)
        self.ui.actionEditEntry.triggered.connect(self.edit_entry)
        self.ui.actionDeleteEntry.triggered.connect(self.delete_entry)
        self.ui.actionProfile.triggered.connect(self.profile)
        self.ui.actionLightTheme.triggered.connect(self.light)
        self.ui.actionDarkTheme.triggered.connect(self.dark)
        self.ui.actionPasswordGenerator.triggered.connect(self.password_generator)
        self.ui.actionSignOut.triggered.connect(self.sign_out)
        self.ui.action_about.triggered.connect(self.show_about_dialog)
        self.ui.searchBar.textChanged.connect(self.filter_table)
        self.statusbar_label = QLabel("")
        self.ui.statusbar.addWidget(self.statusbar_label)
        # Schedule the reload method to be called after a short delay
        QTimer.singleShot(100, self.reload)

    def export_data(self) -> None:
        """Exports saved passwords to a json file.

        This method exports saved passwords to a json file (.json).
        It prompts the user to choose the location and name of the file, and then
        writes the saved passwords into the file.

        Returns:
            None

        Raises:
            None
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export saved passwords to a json file:",
            "",
            "JSON file (*.json)",
        )
        if file_path:
            with open(file_path, "w") as file:
                response = auth_get_request(
                    settings.value("MY_DATABASE_ENDPOINT")
                ).json()
                export_data = [
                    {k: v for k, v in password.items() if k != "id"}
                    for password in response
                ]
                json.dump(export_data, file, indent=4)
            QMessageBox.information(
                self,
                "Export Successful",
                "Saved passwords were exported successfully!",
            )

    def show_about_dialog(self) -> None:
        """
        Displays an about dialog box with information about the application.

        Returns:
            None

        Raises:
            None
        """
        about_text = (
            "Passify Desktop\n"
            "Version: 1.0.0\n"
            "Author: github.com/ixmjk\n"
            'Description: "Secure your digital life with Passify, Your Trusted Password Manager!"'
        )

        QMessageBox.about(self, "About Passify", about_text)

    def profile(self):
        new_window = Profile()
        new_window.finished.connect(self.reload)
        new_window.setModal(True)
        new_window.show()

    def sign_out(self):
        from sign_in import SignIn

        settings.remove("ACCESS_TOKEN")
        settings.remove("REFRESH_TOKEN")
        self.close()
        sign_in_window = SignIn()
        sign_in_window.show()

    def refresh_token(self):
        response = post_request(
            settings.value("REFRESH_TOKEN_ENDPOINT"),
            {"refresh": settings.value("REFRESH_TOKEN")},
        )
        ACCESS_TOKEN = response.json().get("access")
        settings.setValue("ACCESS_TOKEN", ACCESS_TOKEN)
        self.reload()

    def password_generator(self):
        from password_generator import PasswordGenerator

        password_generator_window = PasswordGenerator()
        password_generator_window.show()

    def add_entry(self):
        new_window = AddEntry(300, 300)
        new_window.finished.connect(self.reload)
        new_window.setModal(True)
        new_window.show()

    def edit_entry(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            id_url = self.ui.tableWidget.item(selected_row, 5).text()
            new_window = EditEntry(id_url, 300, 300)
            new_window.finished.connect(self.reload)
            new_window.setModal(True)
            new_window.show()
        else:
            QMessageBox.warning(
                self,
                "Edit entry",
                "No entries is selected.",
            )

    def delete_entry(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            response = QMessageBox.question(
                self,
                f"Delete entry {selected_row + 1}",
                "Are you sure you want to delete the selected entry?",
            )
            if response == QMessageBox.Yes:
                id_url = self.ui.tableWidget.item(selected_row, 5).text()
                response = auth_delete_request(id_url, {})
                if response.status_code == 204:
                    pass
                else:
                    error_message = get_error_message(response)
                    QMessageBox.warning(
                        self,
                        f"Error {response.status_code}",
                        error_message,
                    )
                self.reload()

    def reload(self):
        response = auth_get_request(settings.value("MY_DATABASE_ENDPOINT"))
        if response.status_code == 200:
            entries = response.json()
            row_count = len(entries)
            self.update_statusbar(f"{row_count} entries loaded.")
            self.ui.statusbar.addWidget(self.statusbar_label)
            self.ui.tableWidget.setRowCount(row_count)
            self.ui.tableWidget.setColumnHidden(5, True)
            self.ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
            self.ui.tableWidget.itemDoubleClicked.connect(self.copyRowToClipboard)
            self.ui.tableWidget.setItemDelegate(PasswordDelegate())
            self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
            header = self.ui.tableWidget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.Stretch)
            for row in range(row_count):
                self.ui.tableWidget.setItem(
                    row, 0, QTableWidgetItem(entries[row]["title"])
                )
                self.ui.tableWidget.setItem(
                    row, 1, QTableWidgetItem(entries[row]["username"])
                )
                self.ui.tableWidget.setItem(
                    row, 2, QTableWidgetItem(entries[row]["password"])
                )
                self.ui.tableWidget.setItem(
                    row, 3, QTableWidgetItem(entries[row]["url"])
                )
                self.ui.tableWidget.setItem(
                    row, 4, QTableWidgetItem(entries[row]["notes"])
                )
                self.ui.tableWidget.setItem(
                    row, 5, QTableWidgetItem(entries[row]["id"])
                )
            # print(response.json())
        elif response.status_code == 401:  # token expired
            self.refresh_token()
        else:
            error_message = get_error_message(response)
            QMessageBox.warning(
                self,
                f"Error {response.status_code}",
                error_message,
            )
            self.sign_out()

    def filter_table(self):
        search_text = self.searchBar.text().lower()

        for row in range(self.ui.tableWidget.rowCount()):
            show_row = False
            for col in [
                0,  # title
                1,  # username
                3,  # url
                4,  # notes
            ]:
                item = self.ui.tableWidget.item(row, col)
                if search_text in item.text().lower():
                    show_row = True
                    break
            self.ui.tableWidget.setRowHidden(row, not show_row)

    def update_statusbar(self, message: str) -> None:
        """Updates the status bar label with the given message.

        Args: message (str): The message to display in the status bar.

        Returns: None
        """
        self.statusbar_label.setText(f" {message} ")

    def copyRowToClipboard(self, item):
        if item.column() == 3:
            url = item.text()
            qurl = QUrl(url)
            if not QDesktopServices.openUrl(qurl):
                QDesktopServices.openUrl(qurl)
        else:
            clipboard = QApplication.clipboard()
            clipboard.setText(item.text())

    def dark(self):
        settings.setValue("THEME", "dark")
        self.restart()

    def light(self):
        settings.setValue("THEME", "light")
        self.restart()

    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)


class PasswordDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.column() == 2:
            hint = "*"
            option.text = hint * 8
