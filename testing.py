import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt

class ClassificationResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Dummy data for testing
        test_data = [
            {"judul": "Judul Hoaks 1", "kategori": "Misleading Content", "akurasi": 0.95, "presisi": 0.93, "recall": 0.94, "f1_score": 0.935},
            {"judul": "Judul Hoaks 2", "kategori": "Fabricated Content", "akurasi": 0.92, "presisi": 0.90, "recall": 0.91, "f1_score": 0.905},
            # Add more test data as needed
        ]

        # Create table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(test_data))
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["Judul", "Kategori Hoaks", "Akurasi", "Presisi", "Recall", "F1-Score", "ACC", "Tidak ACC"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, data in enumerate(test_data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(data["judul"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(data["kategori"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(f"{data['akurasi']:.2f}"))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(f"{data['presisi']:.2f}"))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(f"{data['recall']:.2f}"))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(f"{data['f1_score']:.2f}"))

            acc_button = QPushButton("ACC")
            acc_button.clicked.connect(self.handleACC)
            self.tableWidget.setCellWidget(row, 6, acc_button)

            tidak_acc_button = QPushButton("Tidak ACC")
            tidak_acc_button.clicked.connect(self.handleTidakACC)
            self.tableWidget.setCellWidget(row, 7, tidak_acc_button)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        # Set layout
        self.setLayout(layout)

        # Set window title and size, and show
        self.setWindowTitle("Hasil Klasifikasi Berita Hoaks")
        self.setMinimumSize(800, 400)
        self.show()

    def handleACC(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()
            judul = self.tableWidget.item(row, 0).text()
            QMessageBox.information(self, "ACC", f"Hasil klasifikasi untuk '{judul}' diterima.")

    def handleTidakACC(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()
            judul = self.tableWidget.item(row, 0).text()
            QMessageBox.information(self, "Tidak ACC", f"Hasil klasifikasi untuk '{judul}' ditolak.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ClassificationResultWindow()
    sys.exit(app.exec())
