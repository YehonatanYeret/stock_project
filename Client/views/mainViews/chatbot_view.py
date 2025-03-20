import datetime
from time import sleep

from PySide6.QtCore import (Qt, Signal, Slot, QSize, QDateTime, QTimer, QEasingCurve, 
                            QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, 
                            QPoint, QRunnable, QObject, QThreadPool)
from PySide6.QtGui import QColor, QPalette, QFont, QIcon, QFontDatabase, QMovie
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QFrame, QTextEdit, QLineEdit, QPushButton, QScrollArea,
                               QSizePolicy, QSpacerItem, QGraphicsOpacityEffect, QLabel)
from components.styled_widgets import (
    ScrollableContainer, StyledLineSeriesChart, StyledStatsCard, StyledTable,
    PageTitleLabel, SectionTitleLabel, StyledLabel, PrimaryButton, DangerButton,
    SellButton, Card, RoundedCard, StyledLineEdit
)


class NonScrollableTextEdit(QTextEdit):
    """Custom QTextEdit that ignores mouse wheel events to disable internal scrolling."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)

    def wheelEvent(self, event):
        event.ignore()


class AnimatedMessageBubble(RoundedCard):
    """An elegant message bubble with improved animation effects.
    
    This version allows the text to use the full available width within the bubble.
    A minimum width is set on the bubble to ensure that the text has enough space.
    """
    def __init__(self, message, timestamp, is_user=False, parent=None):
        super().__init__(parent=parent, border_radius=16, shadow_enabled=True)
        self.setObjectName("messageBubble")
        self.is_user = is_user

        # Set a minimum width for the bubble.
        self.setMinimumWidth(400)

        # Initial setup for animation.
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)
        self.setMaximumHeight(16777215)  # Remove height constraint

        # Set up layout.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        # Message text using NonScrollableTextEdit.
        self.message_label = NonScrollableTextEdit(message)
        self.message_label.setFrameStyle(QFrame.NoFrame)
        self.message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.message_label.setMinimumHeight(10)
        self.message_label.setLineWrapMode(QTextEdit.WidgetWidth)  # Text wraps to available width

        # Improved text styling.
        font = QFont()
        font.setPointSize(14)
        font.setFamily("Segoe UI")
        self.message_label.setFont(font)

        # Connect content change to height adjustment.
        self.message_label.document().contentsChanged.connect(self._adjust_height)

        # Enhanced timestamp display.
        time_str = timestamp.toString("HH:mm")
        self.time_label = StyledLabel(time_str, size=10, color="#888888")
        self.time_label.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)

        layout.addWidget(self.message_label)
        layout.addWidget(self.time_label)

        # Style based on user or assistant.
        if is_user:
            self.setStyleSheet("""
                #messageBubble {
                    background-color: #a0a6e8;
                    border-radius: 16px;
                    border-bottom-right-radius: 4px;
                    margin-left: 80px;
                }
            """)
            self.message_label.setStyleSheet("""
                background: transparent; 
                color: white; 
                border: none;
            """)
            self.time_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); background: transparent;")
        else:
            self.setStyleSheet("""
                #messageBubble {
                    background-color: #F5F5F7;
                    border-radius: 16px;
                    border-bottom-left-radius: 4px;
                    margin-right: 80px;
                }
            """)
            self.message_label.setStyleSheet("""
                background: transparent; 
                color: #333333; 
                border: none;
            """)
            self.time_label.setStyleSheet("color: #888888; background: transparent;")

        # Ensure height is adjusted.
        QTimer.singleShot(10, self._adjust_height)
        QTimer.singleShot(50, self._start_animations)

    def _adjust_height(self):
        document = self.message_label.document()
        document_size = document.documentLayout().documentSize()
        document_height = int(document_size.height())
        new_height = document_height + 12  # Add padding
        self.message_label.setFixedHeight(new_height)
        self.updateGeometry()

    def _start_animations(self):
        self.setMaximumHeight(0)
        self.animation_group = QParallelAnimationGroup()
        fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_anim.setDuration(600)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        height_anim = QPropertyAnimation(self, b"maximumHeight")
        height_anim.setDuration(700)
        height_anim.setStartValue(0)
        final_height = self.layout().sizeHint().height()
        height_anim.setEndValue(final_height)
        height_anim.setEasingCurve(QEasingCurve.OutBack)

        self.animation_group.addAnimation(fade_anim)
        self.animation_group.addAnimation(height_anim)
        self.animation_group.finished.connect(lambda: self.setMaximumHeight(16777215))
        self.animation_group.start(QAbstractAnimation.DeleteWhenStopped)


class WaitMessageBubble(RoundedCard):
    """A wait indicator bubble showing a spinner until the server responds."""
    def __init__(self, parent=None):
        super().__init__(parent=parent, border_radius=16, shadow_enabled=True)
        self.setObjectName("waitBubble")
        # Set a minimum width.
        self.setMinimumWidth(400)
        
        # Set up layout.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)
        
        # Create a QLabel to hold the spinner animation.


        # Optionally, add a "Waiting..." text below the spinner.
        self.wait_text = StyledLabel("Waiting...", size=10, color="#888888")
        self.wait_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.wait_text)
        
        # Start a simple fade-in animation.
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(350)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()


class ChatbotView(QWidget):
    """Elegant and modernized chatbot interface."""
    send_message_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chatbotView")
        self.setWindowTitle("AI Trading Assistant")
        self.messages = []  # Store message bubbles.
        self.wait_bubble = None  # Reference to the current wait indicator, if any.
        self.setup_fonts()
        self.setup_ui()

    def wellcome_message(self):
        if not self.messages:
            self._add_assistant_message("Hello! I'm your AI trading assistant. How can I help you today?")

    def setup_fonts(self):
        self.body_font = QFont("Segoe UI", 12)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = PageTitleLabel("AI Trading Assistant")
        main_layout.addWidget(title)

        self.chat_container = ScrollableContainer(
            parent=self,
            margins=(10, 10, 10, 10),
            spacing=10,
            bg_color="#FFFFFF",
            shadow_enabled=True,
            border_radius=12
        )
        self.chat_container.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
                height: 0px;
                width: 0px;
            }
        """)

        self.message_container = QWidget()
        self.message_container.setObjectName("messageContainer")
        self.message_container.setStyleSheet("""
            #messageContainer {
                background-color: #F9F9FB;
            }
        """)
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setContentsMargins(25, 25, 25, 25)
        self.message_layout.setSpacing(12)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.message_layout.addStretch()
        self.chat_container.setWidget(self.message_container)

        input_frame = RoundedCard(border_radius=30, shadow_enabled=True)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 10)
        input_layout.setSpacing(15)

        self.message_input = StyledLineEdit(parent=self, placeholder="Type your message...")
        self.message_input.setObjectName("messageInput")
        self.message_input.setMinimumHeight(50)
        self.message_input.setFont(self.body_font)
        self.message_input.setStyleSheet("""
            #messageInput {
                border: none;
                border-radius: 20px;
                padding: 0 20px;
                background-color: None;
                color: #333333;
            }
            #messageInput:focus {
                background-color: #FFFFFF;
                border: 1px solid #a0a6e8;
            }
        """)
        self.message_input.returnPressed.connect(self._on_send_clicked)

        self.send_button = QPushButton()
        self.send_button.setObjectName("sendButton")
        self.send_button.setFixedSize(50, 50)
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setStyleSheet("""
            #sendButton {
                background-color: #a0a6e8;
                border-radius: 25px;
                border: none;
                color: white;
                font-weight: bold;
                font-size: 20px;
            }
            #sendButton:hover {
                background-color: #8c93d8;
            }
            #sendButton:pressed {
                background-color: #7980c9;
            }
        """)
        self.send_button.setText("→")
        self.send_button.clicked.connect(self._on_send_clicked)

        input_layout.addWidget(self.message_input, 1)
        input_layout.addWidget(self.send_button, 0)

        main_layout.addWidget(self.chat_container, 1)
        main_layout.addWidget(input_frame, 0)
        self.setStyleSheet("""
            QWidget#chatbotView {
                background-color: #F0F0F5;
            }
        """)

    def _on_send_clicked(self):
        message = self.message_input.text().strip()
        if message:
            self._add_user_message(message)
            self.send_message_signal.emit(message)
            self.message_input.clear()
            self.message_input.setFocus()

    def _add_user_message(self, message):
        self._add_message_bubble(message, is_user=True)

    def _add_assistant_message(self, message):
        self._add_message_bubble(message, is_user=False)

    def _add_message_bubble(self, message, is_user=False):
        if self.message_layout.count() > 0:
            last_item = self.message_layout.itemAt(self.message_layout.count() - 1)
            if isinstance(last_item, QSpacerItem):
                self.message_layout.removeItem(last_item)
        timestamp = QDateTime.currentDateTime()
        bubble = AnimatedMessageBubble(message, timestamp, is_user)
        self.message_layout.addWidget(bubble)
        self.messages.append(bubble)
        self.message_layout.addStretch()
        QTimer.singleShot(400, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        scrollbar = self.chat_container.verticalScrollBar()
        if scrollbar.value() < scrollbar.maximum():
            self.scroll_animation = QPropertyAnimation(scrollbar, b"value")
            self.scroll_animation.setDuration(300)
            self.scroll_animation.setStartValue(scrollbar.value())
            self.scroll_animation.setEndValue(scrollbar.maximum())
            self.scroll_animation.setEasingCurve(QEasingCurve.OutCubic)
            self.scroll_animation.start(QAbstractAnimation.DeleteWhenStopped)

    def add_wait_indicator(self):
        """Add a wait/spinner bubble for the assistant response."""
        if not self.wait_bubble:
            # Remove stretch before adding wait bubble.
            if self.message_layout.count() > 0:
                last_item = self.message_layout.itemAt(self.message_layout.count() - 1)
                if isinstance(last_item, QSpacerItem):
                    self.message_layout.removeItem(last_item)
            self.wait_bubble = WaitMessageBubble()
            self.message_layout.addWidget(self.wait_bubble)
            self.message_layout.addStretch()
            QTimer.singleShot(400, self._scroll_to_bottom)

    def remove_wait_indicator(self):
        """Remove the wait bubble if it exists."""
        if self.wait_bubble:
            self.wait_bubble.setParent(None)
            self.wait_bubble.deleteLater()
            self.wait_bubble = None
            QTimer.singleShot(400, self._scroll_to_bottom)

    @Slot(str)
    def add_response(self, message):
        """Remove wait indicator and add an assistant message."""
        self.remove_wait_indicator()
        self._add_assistant_message(message)