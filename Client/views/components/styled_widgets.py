from PySide6.QtWidgets import (
    QPushButton, QLineEdit, QLabel, QFrame
)

class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4C6FFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3A5BCC;
            }
            QPushButton:pressed {
                background-color: #2D49A3;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #888888;
            }
        """)

class SecondaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4C6FFF;
                border: 1px solid #4C6FFF;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(76, 111, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(76, 111, 255, 0.2);
            }
            QPushButton:disabled {
                color: #CCCCCC;
                border-color: #CCCCCC;
            }
        """)

class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #EAEAEA;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4C6FFF;
            }
        """)

class StyledLabel(QLabel):
    def __init__(self, text, is_title=False, parent=None):
        super().__init__(text, parent)
        if is_title:
            self.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #333333;
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #555555;
                }
            """)

class Card(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #EAEAEA;
            }
        """)