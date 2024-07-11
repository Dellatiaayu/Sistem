import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox, QMessageBox, QTextEdit, QGridLayout)
from PySide6.QtCore import Qt

class ClassificationResults(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create widgets for displaying results
        resultsGroupBox = QGroupBox()
        resultsLayout = QGridLayout()
        resultsLayout.setAlignment(Qt.AlignTop)
        
        self.resultsTitleLabel = QLabel("Judul Berita:")
        self.resultsTitle = QLabel("-")
        
        self.preprocessedTextLabel = QLabel("Hasil Text Preprocessing:")
        self.preprocessedText = QTextEdit()
        self.preprocessedText.setReadOnly(True)
        
        self.classificationResultLabel = QLabel("Hasil Klasifikasi:")
        self.classificationResult = QLabel("-")
        
        self.accuracyLabel = QLabel("Tingkat Akurasi:")
        self.accuracy = QLabel("-")
        
        self.precisionLabel = QLabel("Presisi:")
        self.precision = QLabel("-")
        
        self.recallLabel = QLabel("Recall:")
        self.recall = QLabel("-")
        
        self.f1ScoreLabel = QLabel("F1-Score:")
        self.f1Score = QLabel("-")

        resultsLayout.addWidget(self.resultsTitleLabel, 0, 0)
        resultsLayout.addWidget(self.resultsTitle, 0, 1)
        resultsLayout.addWidget(self.preprocessedTextLabel, 1, 0)
        resultsLayout.addWidget(self.preprocessedText, 1, 1)
        resultsLayout.addWidget(self.classificationResultLabel, 2, 0)
        resultsLayout.addWidget(self.classificationResult, 2, 1)
        resultsLayout.addWidget(self.accuracyLabel, 3, 0)
        resultsLayout.addWidget(self.accuracy, 3, 1)
        resultsLayout.addWidget(self.precisionLabel, 4, 0)
        resultsLayout.addWidget(self.precision, 4, 1)
        resultsLayout.addWidget(self.recallLabel, 5, 0)
        resultsLayout.addWidget(self.recall, 5, 1)
        resultsLayout.addWidget(self.f1ScoreLabel, 6, 0)
        resultsLayout.addWidget(self.f1Score, 6, 1)

        resultsGroupBox.setLayout(resultsLayout)

        # Create main layout and add both group boxes
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(resultsGroupBox)

        # Set layout
        self.setLayout(mainLayout)

        # Set window title and size, and show
        self.setWindowTitle("Hasil Klasifikasi Berita Hoaks")
        self.setMinimumSize(800, 400)
        self.show()

    def displayResults(self):
        # Example data - replace with actual preprocessing and classification
        test_title = self.testTitleInput.text()
        preprocessed_text = "Contoh teks yang telah diproses"
        classification_result = "Misleading Content"
        accuracy = "95%"
        precision = "92%"
        recall = "93%"
        f1_score = "92.5%"

        self.resultsTitle.setText(test_title)
        self.preprocessedText.setPlainText(preprocessed_text)
        self.classificationResult.setText(classification_result)
        self.accuracy.setText(accuracy)
        self.precision.setText(precision)
        self.recall.setText(recall)
        self.f1Score.setText(f1_score)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ClassificationResults()
    sys.exit(app.exec())
