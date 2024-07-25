import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox)
from PySide6.QtCore import Qt

class ClassificationResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Dummy data for testing
        self.test_data = [
            {"judul": f"Judul Hoaks {i+1}", "kategori": "Misleading Content", "akurasi": 0.95, "presisi": 0.93, "recall": 0.94, "f1_score": 0.935} for i in range(50)
        ]
        
        # Current page
        self.current_page = 0
        self.rows_per_page = 10

        # Create widgets
        self.searchBox = QLineEdit(self)
        self.searchBox.setPlaceholderText("Search...")
        self.searchBox.textChanged.connect(self.updateTable)

        self.filterBox = QComboBox(self)
        self.filterBox.addItems(["All", "Misleading Content", "Fabricated Content", "False Connection", "False Context", "Manipulated Content", "Satire or Parody"])
        self.filterBox.currentIndexChanged.connect(self.updateTable)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["Judul", "Kategori Hoaks", "Akurasi", "Presisi", "Recall", "F1-Score", "ACC/ Tidak ACC"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create navigation buttons
        self.prevButton = QPushButton("Previous")
        self.prevButton.clicked.connect(self.prevPage)

        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.nextPage)

        # Create layout
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.searchBox)
        topLayout.addWidget(self.filterBox)

        navLayout = QHBoxLayout()
        navLayout.addWidget(self.prevButton)
        navLayout.addWidget(self.nextButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.tableWidget)
        mainLayout.addLayout(navLayout)

        # Set layout
        self.setLayout(mainLayout)

        # Set window title and size, and show
        self.setWindowTitle("Hasil Klasifikasi Berita Hoaks")
        self.setMinimumSize(800, 400)
        self.updateTable()
        self.show()

    def updateTable(self):
        search_term = self.searchBox.text().lower()
        filter_term = self.filterBox.currentText()

        filtered_data = [data for data in self.test_data if search_term in data["judul"].lower()]
        if filter_term != "All":
            filtered_data = [data for data in filtered_data if data["kategori"] == filter_term]

        self.tableWidget.setRowCount(0)
        start = self.current_page * self.rows_per_page
        end = start + self.rows_per_page

        for row, data in enumerate(filtered_data[start:end]):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(data["judul"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(data["kategori"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(f"{data['akurasi']:.2f}"))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(f"{data['presisi']:.2f}"))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(f"{data['recall']:.2f}"))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(f"{data['f1_score']:.2f}"))

            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(0, 0, 0, 0)
            acc_button = QPushButton("ACC")
            acc_button.clicked.connect(self.handleACC)
            tidak_acc_button = QPushButton("Tidak ACC")
            tidak_acc_button.clicked.connect(self.handleTidakACC)
            button_layout.addWidget(acc_button)
            button_layout.addWidget(tidak_acc_button)

            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.tableWidget.setCellWidget(row, 6, button_widget)

        self.updateNavigationButtons(len(filtered_data))

    def updateNavigationButtons(self, total_rows):
        self.prevButton.setEnabled(self.current_page > 0)
        self.nextButton.setEnabled((self.current_page + 1) * self.rows_per_page < total_rows)

    def prevPage(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.updateTable()

    def nextPage(self):
        self.current_page += 1
        self.updateTable()

    def handleACC(self):
        button = self.sender()
        if button:
            index = self.tableWidget.indexAt(button.pos())
            row = index.row()
            col = index.column()
            if row >= 0 and col >= 0:
                button_layout = self.tableWidget.cellWidget(row, col).layout()
                acc_button = button_layout.itemAt(0).widget()
                tidak_acc_button = button_layout.itemAt(1).widget()
                acc_button.setEnabled(False)
                tidak_acc_button.setEnabled(True)
                QMessageBox.information(self, "ACC", f"Hasil klasifikasi untuk '{self.tableWidget.item(row, 0).text()}' diterima.")

    def handleTidakACC(self):
        button = self.sender()
        if button:
            index = self.tableWidget.indexAt(button.pos())
            row = index.row()
            col = index.column()
            if row >= 0 and col >= 0:
                button_layout = self.tableWidget.cellWidget(row, col).layout()
                acc_button = button_layout.itemAt(0).widget()
                tidak_acc_button = button_layout.itemAt(1).widget()
                acc_button.setEnabled(True)
                tidak_acc_button.setEnabled(False)
                QMessageBox.information(self, "Tidak ACC", f"Hasil klasifikasi untuk '{self.tableWidget.item(row, 0).text()}' ditolak.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ClassificationResultWindow()
    sys.exit(app.exec())
