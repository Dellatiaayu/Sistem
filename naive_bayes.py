import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox, QMessageBox)
from PySide6.QtCore import Qt

class NaiveBayesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create widgets for training section
        trainGroupBox = QGroupBox("Training")
        trainLayout = QVBoxLayout()
        trainLayout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        
        self.trainTitleLabel = QLabel("Judul Berita Hoaks:")
        self.trainTitleInput = QLineEdit()
        
        self.trainCategoryLabel = QLabel("Kategori Hoaks:")
        self.trainCategoryDropdown = QComboBox()
        self.trainCategoryDropdown.addItems([
            "Misleading Content", 
            "Imposter Content", 
            "Fabricated Content", 
            "False Connection", 
        ])
        
        self.trainSubmitButton = QPushButton("Proses Training")
        self.trainSubmitButton.clicked.connect(self.showTrainData)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.trainSubmitButton)
        buttonLayout.addWidget(self.addToDBSubmitButton)

        trainLayout.addWidget(self.trainTitleLabel)
        trainLayout.addWidget(self.trainTitleInput)
        trainLayout.addWidget(self.trainCategoryLabel)
        trainLayout.addWidget(self.trainCategoryDropdown)
        trainLayout.addWidget(self.addToDBSubmitButton)        
        trainLayout.addWidget(self.trainSubmitButton)
        trainLayout.addLayout(buttonLayout)
        trainGroupBox.setLayout(trainLayout)

        # Create widgets for testing section
        testGroupBox = QGroupBox("Testing")
        testLayout = QVBoxLayout()
        testLayout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        
        self.testTitleLabel = QLabel("Judul Berita Hoaks:")
        self.testTitleInput = QLineEdit()
        
        self.testSubmitButton = QPushButton("Proses Testing")
        self.testSubmitButton.clicked.connect(self.showTestData)

        testLayout.addWidget(self.testTitleLabel)
        testLayout.addWidget(self.testTitleInput)
        testLayout.addWidget(self.testSubmitButton)
        testGroupBox.setLayout(testLayout)

        # Create main layout and add both group boxes
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(trainGroupBox)
        mainLayout.addWidget(testGroupBox)

        # Set layout
        self.setLayout(mainLayout)

        # Set window title and size, and show
        self.setWindowTitle("Training and Testing Input Form")
        self.setMinimumSize(600, 400)
        self.show()

    def showTrainData(self):
        title = self.trainTitleInput.text()
        category = self.trainCategoryDropdown.currentText()
        QMessageBox.information(self, "Training Data", f"Judul: {title}\nKategori: {category}")
        
    def addToDB(self):
        QMessageBox.information(self, "Add to Database", "Data has been added to the database.")

    def showTestData(self):
        title = self.testTitleInput.text()
        QMessageBox.information(self, "Testing Data", f"Judul: {title}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = NaiveBayesWindow()
    sys.exit(app.exec())
