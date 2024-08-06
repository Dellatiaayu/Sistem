import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox, QMessageBox)
from PySide6.QtCore import Qt
import sqlalchemy
from sqlalchemy import create_engine, text
import pandas as pd
import os


class NaiveBayesWindow(QWidget):
    
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')
        # Create widgets for training section
        trainGroupBox = QGroupBox("Training")
        trainLayout = QVBoxLayout()
        trainLayout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        
        self.trainTitleLabel = QLabel("Judul Berita Hoaks:")
        self.trainTitleInput = QLineEdit()
        
        self.trainCategoryLabel = QLabel("Kategori Hoaks:")
        self.trainCategoryDropdown = QComboBox()
        
        # get kategori from database
        kategories = "SELECT * FROM kategori";
        kategori = pd.read_sql(kategories, engine)
        kategori = kategori['name'].tolist()
        self.trainCategoryDropdown.addItems(kategori)
        
        self.trainSubmitButton = QPushButton("Proses Training")
        self.trainSubmitButton.clicked.connect(self.showTrainData)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.trainSubmitButton)

        trainLayout.addWidget(self.trainTitleLabel)
        trainLayout.addWidget(self.trainTitleInput)
        trainLayout.addWidget(self.trainCategoryLabel)
        trainLayout.addWidget(self.trainCategoryDropdown)      
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
        engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')
        
        title = self.trainTitleInput.text()
        category = self.trainCategoryDropdown.currentText()
        
        # if title is empty
        if not title:
            QMessageBox.warning(self, "Warning", "Judul tidak boleh kosong.")
            return
        
        # get category id from database
        query = f"SELECT id FROM kategori WHERE name = '{category}'"
        category_id = pd.read_sql(query, engine)
        category_id = category_id['id'].values[0]
        
        query = text("INSERT INTO training (Judul, id_kategori) VALUES (:judul, :kategori)")
        with engine.connect() as connection:
            connection.execute(query, {"judul": title, "kategori": category_id})
            connection.commit()
            connection.close()
        
        os.system('python text_preprocessing.py')
        os.system('python multinomial_nb.py')
        

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
