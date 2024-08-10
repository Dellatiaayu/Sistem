import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView)
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

        # Create the tab widget
        self.tabs = QTabWidget()

        # Tab 1: Training and Testing
        tab1 = QWidget()
        tab1Layout = QHBoxLayout()

        # Create widgets for training section
        trainGroupBox = QGroupBox("Training")
        trainLayout = QVBoxLayout()
        trainLayout.setAlignment(Qt.AlignTop)

        self.trainTitleLabel = QLabel("Judul Berita Hoaks:")
        self.trainTitleInput = QLineEdit()

        self.trainCategoryLabel = QLabel("Kategori Hoaks:")
        self.trainCategoryDropdown = QComboBox()

        # get kategori from database
        kategories = "SELECT * FROM kategori"
        kategori = pd.read_sql(kategories, engine)
        kategori = kategori['name'].tolist()
        self.trainCategoryDropdown.addItems(kategori)

        self.trainSubmitButton = QPushButton("Proses Training")
        self.trainSubmitButton.clicked.connect(self.showTrainData)

        trainLayout.addWidget(self.trainTitleLabel)
        trainLayout.addWidget(self.trainTitleInput)
        trainLayout.addWidget(self.trainCategoryLabel)
        trainLayout.addWidget(self.trainCategoryDropdown)
        trainLayout.addWidget(self.trainSubmitButton)
        trainGroupBox.setLayout(trainLayout)

        # Create widgets for testing section
        testGroupBox = QGroupBox("Testing")
        testLayout = QVBoxLayout()
        testLayout.setAlignment(Qt.AlignTop)

        self.testTitleLabel = QLabel("Judul Berita Hoaks:")
        self.testTitleInput = QLineEdit()

        self.testSubmitButton = QPushButton("Proses Testing")
        self.testSubmitButton.clicked.connect(self.showTestData)

        testLayout.addWidget(self.testTitleLabel)
        testLayout.addWidget(self.testTitleInput)
        testLayout.addWidget(self.testSubmitButton)
        testGroupBox.setLayout(testLayout)

        tab1Layout.addWidget(trainGroupBox)
        tab1Layout.addWidget(testGroupBox)
        tab1.setLayout(tab1Layout)

        engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

        query = """
        SELECT t.*, k.name 
        FROM testing t
        JOIN kategori k ON t.id_kategori = k.id
        """
        test_data = pd.read_sql(query, engine)
        print(test_data) 
        

        def editACC(self):
            button = self.sender()
            if button:
                row = self.tableWidget.indexAt(button.pos()).row()
                acc_combo = self.tableWidget.cellWidget(row, 6)
                acc_value = acc_combo.currentText()
                QMessageBox.information(self, "Edit ACC", f"ACC untuk '{self.tableWidget.item(row, 0).text()}' diubah menjadi '{acc_value}'.")

        def filterTable(self):
            filter_text = self.search_input.text().lower()
            filter_category = self.filter_combo.currentText()

            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, 0)
                category_item = self.tableWidget.item(row, 1)
                if item and category_item:
                    item_text = item.text().lower()
                    category_text = category_item.text()
                    if (filter_text in item_text) and (filter_category == "All" or filter_category == category_text):
                        self.tableWidget.setRowHidden(row, False)
                    else:
                        self.tableWidget.setRowHidden(row, True)


        # Tab 2: Testing Results
        tab2 = QWidget()
        tab2Layout = QVBoxLayout()

        self.resultsTable = QTableWidget()
        self.resultsTable.setRowCount(len(test_data))
        self.resultsTable.setColumnCount(8)
        self.resultsTable.setHorizontalHeaderLabels(["Judul", "Kategori", "Akurasi", "Presisi", "Recall", "F1-Score", "ACC", "Edit ACC"])
        tab2Layout.addWidget(self.resultsTable)
        
        for row, data in test_data.iterrows():
            self.resultsTable.setItem(row, 0, QTableWidgetItem(data["Judul"]))
            self.resultsTable.setItem(row, 1, QTableWidgetItem(data['name']))
            self.resultsTable.setItem(row, 2, QTableWidgetItem(f"{data['akurasi']:.2f}"))
            self.resultsTable.setItem(row, 3, QTableWidgetItem(f"{data['presisi']:.2f}"))
            self.resultsTable.setItem(row, 4, QTableWidgetItem(f"{data['recall']:.2f}"))
            self.resultsTable.setItem(row, 5, QTableWidgetItem(f"{data['f1_score']:.2f}"))

            acc_combo = QComboBox()
            acc_combo.addItems(["ACC", "Tidak ACC"])
            self.resultsTable.setCellWidget(row, 6, acc_combo)

            edit_button = QPushButton("Edit ACC")
            edit_button.clicked.connect(self.editACC)
            self.resultsTable.setCellWidget(row, 7, edit_button)

        tab2.setLayout(tab2Layout)

        # Add tabs to the tab widget
        self.tabs.addTab(tab1, "Training & Testing")
        self.tabs.addTab(tab2, "Hasil Testing")
        
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filterTable)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        filter_label = QLabel("Filter:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Misleading Content", "Fabricated Content", "False Connection", "False Context", "Manipulated Content", "Satire or Parody"])
        self.filter_combo.currentTextChanged.connect(self.filterTable)
        search_layout.addWidget(filter_label)
        search_layout.addWidget(self.filter_combo)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(search_layout)
        mainLayout.addWidget(self.tabs)

        self.setLayout(mainLayout)

        # Set window title and size, and show
        self.setWindowTitle("Naive Bayes Classifier")
        self.setMinimumSize(800, 600)
        self.show()
    
    def editACC(self):
        button = self.sender()
        if button:
            row = self.resultsTable.indexAt(button.pos()).row()
            acc_combo = self.resultsTable.cellWidget(row, 6)
            acc_value = acc_combo.currentText()
            QMessageBox.information(self, "Edit ACC", f"ACC untuk '{self.resultsTable.item(row, 0).text()}' diubah menjadi '{acc_value}'.")

    def filterTable(self):
        filter_text = self.search_input.text().lower()
        filter_category = self.filter_combo.currentText()

        for row in range(self.resultsTable.rowCount()):
            item = self.resultsTable.item(row, 0)
            category_item = self.resultsTable.item(row, 1)
            if item and category_item:
                item_text = item.text().lower()
                category_text = category_item.text()
                if (filter_text in item_text) and (filter_category == "All" or filter_category == category_text):
                    self.resultsTable.setRowHidden(row, False)
                else:
                    self.resultsTable.setRowHidden(row, True)
                    
    def filterTable(self):
        filter_text = self.search_input.text().lower()
        filter_category = self.filter_combo.currentText()

        for row in range(self.resultsTable.rowCount()):
            item = self.resultsTable.item(row, 0)
            category_item = self.resultsTable.item(row, 1)
            if item and category_item:
                item_text = item.text().lower()
                category_text = category_item.text()
                if (filter_text in item_text) and (filter_category == "All" or filter_category == category_text):
                    self.resultsTable.setRowHidden(row, False)
                else:
                    self.resultsTable.setRowHidden(row, True)
    
    def showTrainData(self):
        engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

        title = self.trainTitleInput.text()
        category = self.trainCategoryDropdown.currentText()

        if not title:
            QMessageBox.warning(self, "Warning", "Judul tidak boleh kosong.")
            return

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

        QMessageBox.information(self, "Training Data", f"Judul: {title}")

    def showTestData(self):
        engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

        title = self.testTitleInput.text()


        if not title:
            QMessageBox.warning(self, "Warning", "Judul tidak boleh kosong.")
            return

        query = text("INSERT INTO testing (Judul) VALUES (:judul)")
        with engine.connect() as connection:
            result = connection.execute(query, {"judul": title})
            inserted_id = result.lastrowid
            connection.commit()
            connection.close()

        # get result from testing data
        os.system('python multinominal_testing.py ' + str(inserted_id))

        # After running the external script, load the results to the table
        self.loadTestResults()

        QMessageBox.information(self, "Berhasil Testing Data", f"Judul: {title}")
        
        

    def loadTestResults(self):
        engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

        # Query to fetch testing results
        results = pd.read_sql("SELECT t.id, t.Judul, k.name as Kategori FROM testing t JOIN kategori k ON t.id_kategori = k.id", engine)

        self.resultsTable.setRowCount(len(results))

        for index, row in results.iterrows():
            self.resultsTable.setItem(index, 0, QTableWidgetItem(row['Judul']))
            self.resultsTable.setItem(index, 1, QTableWidgetItem(row['Kategori']))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = NaiveBayesWindow()
    sys.exit(app.exec())