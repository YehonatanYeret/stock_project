from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class IconButton(QPushButton):
    def __init__(self, icon_path=None, color="#5851DB", parent=None):
        super().__init__(parent)
        self.setFlat(True)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {color};
                font-size: 18px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: rgba(88, 81, 219, 0.1);
                border-radius: 4px;
            }}
        """)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))