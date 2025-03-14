from PySide6.QtWidgets import (
    QPushButton, QLineEdit, QLabel, QFrame, QVBoxLayout
    , QHBoxLayout, 
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4C6FFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;  /* Slightly reduced padding */
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

class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4C6FFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;  /* Slightly reduced padding */
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
                padding: 8px 16px;
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
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4C6FFF;
            }
        """)


class StyledLabel(QLabel):
    def __init__(self, text, is_title=False, size=None, color=None, parent=None):
        super().__init__(text, parent)

        # Default values
        default_size = 18 if is_title else 14
        default_weight = "bold" if is_title else "normal"
        default_color = "#333333" if is_title else "#555555"

        # Use provided values or defaults
        font_size = size or default_size
        font_weight = default_weight
        font_color = color or default_color

        self.setStyleSheet(f"""
            QLabel {{
                font-size: {font_size}px;
                font-weight: {font_weight};
                color: {font_color};
                background: none;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
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


class ContentCard(QFrame):
    def __init__(self,content, parent = None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #EAEAEA;
            }
        """)
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(16)
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        self.content_layout.addWidget(content_label)


class PageHeader(QFrame):
    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #222222;
                background: none;
                border: none;
            }
        """)
        layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666666;
                background: none;
                border: none;
            }
        """)
        layout.addWidget(subtitle_label)


class SectionTitle(QLabel):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333;
            }
        """)


class SmallButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #FF4D4D;  /* Red for selling stocks */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 10px;  /* Smaller button size */
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D43F3F;
            }
            QPushButton:pressed {
                background-color: #B53131;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #888888;
            }
        """)


class StatCard(QFrame):
    def __init__(self, title, value, subtitle=None, icon=None, color="#5851DB", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setStyleSheet("""
            #StatCard {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.08);
                border: 1px solid #EAEAEA;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        
        # Header with title and icon
        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 15px; font-weight: 500;")
        header_layout.addWidget(title_label)
        
        if icon:
            icon_label = QLabel()
            pixmap = QPixmap(icon)
            icon_label.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            header_layout.addWidget(icon_label)
        else:
            header_layout.addStretch()
        
        self.layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: #000; font-size: 28px; font-weight: bold;")
        self.layout.addWidget(value_label)
        
        # Subtitle (optional)
        if subtitle:
            subtitle_layout = QHBoxLayout()
            
            # Create arrow icon based on positive/negative value
            arrow_label = QLabel()
            if "+" in subtitle:
                arrow_label.setText("↗")
                arrow_label.setStyleSheet(f"color: {color}; font-size: 18px;")
            elif "-" in subtitle:
                arrow_label.setText("↘")
                arrow_label.setStyleSheet("color: #F44336; font-size: 18px;")
            
            subtitle_text = QLabel(subtitle)
            subtitle_text.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 500;")
            
            subtitle_layout.addWidget(arrow_label)
            subtitle_layout.addWidget(subtitle_text)
            subtitle_layout.addStretch()
            
            self.layout.addLayout(subtitle_layout)
