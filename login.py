import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt
import mysql.connector
from mysql.connector import Error

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create widgets
        self.usernameLabel = QLabel("Username:")
        self.usernameInput = QLineEdit()

        self.passwordLabel = QLabel("Password:")
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton("Login")
        self.loginButton.clicked.connect(self.handleLogin)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameInput)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.loginButton)
        layout.setAlignment(Qt.AlignTop)

        # Set layout
        self.setLayout(layout)

        # Set window title and size, and show
        self.setWindowTitle("Login")
        self.setMinimumSize(300, 200)
        self.show()

    def handleLogin(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        connection = None

        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='klasifikasi_nb',
                user='root', 
                password='root' 
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT username, role FROM users WHERE username=%s AND password=%s", (username, password))
                record = cursor.fetchone()
                if record:
                    user, role = record
                    if role == 1:
                        QMessageBox.information(self, "Login Successful", f"Welcome, admin {username}!")
                    elif role == 2:
                        QMessageBox.information(self, "Login Successful", f"Welcome, kepala bidang {username}!")
                    else:
                        QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error connecting to MySQL: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LoginWindow()
    sys.exit(app.exec())
