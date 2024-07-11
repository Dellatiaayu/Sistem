import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt

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

        if username == "admin" and password == "password":
            QMessageBox.information(self, "Login Successful", "Welcome, admin!")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LoginWindow()
    sys.exit(app.exec())
