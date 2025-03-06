# File: views/home_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Stock Portfolio Manager")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            padding: 20px;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Manage Your Investments Efficiently")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #BDBDBD;
            padding: 10px;
            text-align: center;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch(1)