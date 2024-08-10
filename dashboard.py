import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSortFilterProxyModel
from sqlalchemy import create_engine, text
import pandas as pd

class ClassificationResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Dummy data for testing
        engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

        query = """
        SELECT t.*, k.name 
        FROM testing t
        JOIN kategori k ON t.id_kategori = k.id
        """
        test_data = pd.read_sql(query, engine)

        self.resultsTable = QTableWidget()
        tab2Layout = QVBoxLayout()
        self.resultsTable.setRowCount(len(test_data))
        self.resultsTable.setColumnCount(8)
        self.resultsTable.setHorizontalHeaderLabels(["Judul", "Kategori", "Akurasi", "Presisi", "Recall", "F1-Score", "ACC", "Edit ACC"])
        tab2Layout.addWidget(self.resultsTable)
        
        for row, data in test_data.iterrows():
            self.resultsTable.setItem(row, 0, QTableWidgetItem(data["Judul"]))
            self.resultsTable.setItem(row, 1, QTableWidgetItem(data["name"]))
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
            
        # Create search and filter layout
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

        # Create layout
        layout = QVBoxLayout()
        layout.addLayout(search_layout)
        layout.addWidget(self.resultsTable)

        # Set layout
        self.setLayout(layout)

        # Set window title and size, and show
        self.setWindowTitle("Hasil Klasifikasi Berita Hoaks")
        self.setMinimumSize(800, 400)
        self.show()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ClassificationResultWindow()
    sys.exit(app.exec())
