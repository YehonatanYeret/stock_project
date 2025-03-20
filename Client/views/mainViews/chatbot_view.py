import datetime
from time import sleep

from PySide6.QtCore import Qt, Signal, Slot, QSize, QDateTime, QTimer, QEasingCurve, QPropertyAnimation, \
    QParallelAnimationGroup, QAbstractAnimation, QPoint
from PySide6.QtGui import QColor, QPalette, QFont, QIcon, QFontDatabase
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
        # Ignore wheel events to disable scrolling inside the text edit.
        event.ignore()


class AnimatedMessageBubble(RoundedCard):
    """An elegant message bubble with improved animation effects.
    
    This version allows the text to use the full available width within the bubble.
    A minimum width is set on the bubble to ensure that the text has enough space.
    """

    def __init__(self, message, timestamp, is_user=False, parent=None):
        # Set a minimum width for the bubble (adjust as needed).
        super().__init__(parent=parent, border_radius=16, shadow_enabled=True)
        self.setObjectName("messageBubble")
        self.is_user = is_user

        # Optionally set a minimum width so the bubble doesn't shrink too much.
        self.setMinimumWidth(400)

        # Initial setup for animation.
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)

        # Reset maximum height to allow full expansion after the animation.
        self.setMaximumHeight(16777215)

        # Set up layout.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        # Message text using NonScrollableTextEdit.
        self.message_label = NonScrollableTextEdit(message)
        self.message_label.setFrameStyle(QFrame.NoFrame)
        self.message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.message_label.setMinimumHeight(10)
        self.message_label.setLineWrapMode(QTextEdit.WidgetWidth)  # Ensure text wraps within the widget.
        # Removed the maximum width so text can take full available width.

        # Improved text styling.
        font = QFont()
        font.setPointSize(14)
        font.setFamily("Segoe UI")  # More modern font.
        self.message_label.setFont(font)

        # Connect content change to height adjustment.
        self.message_label.document().contentsChanged.connect(self._adjust_height)

        # Enhanced timestamp display.
        time_str = timestamp.toString("HH:mm")
        self.time_label = StyledLabel(time_str, size=10, color="#888888")
        self.time_label.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)

        # Add widgets to layout.
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

        # Start animations after a brief delay.
        QTimer.singleShot(50, self._start_animations)

    def _adjust_height(self):
        """Adjust the height of the text area to fit its content."""
        document = self.message_label.document()
        document_size = document.documentLayout().documentSize()
        document_height = int(document_size.height())

        # Add padding for better appearance.
        new_height = document_height + 12
        self.message_label.setFixedHeight(new_height)
        self.updateGeometry()

    def _start_animations(self):
        """Animate the bubble using fade and expansion effects."""
        # Temporarily constrain height to animate expansion.
        self.setMaximumHeight(0)
        
        self.animation_group = QParallelAnimationGroup()

        # Fade-in animation.
        fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_anim.setDuration(350)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Expansion animation for maximumHeight.
        height_anim = QPropertyAnimation(self, b"maximumHeight")
        height_anim.setDuration(400)
        height_anim.setStartValue(0)
        # Calculate final height from the current layout size.
        final_height = self.layout().sizeHint().height()
        height_anim.setEndValue(final_height)
        height_anim.setEasingCurve(QEasingCurve.OutBack)

        self.animation_group.addAnimation(fade_anim)
        self.animation_group.addAnimation(height_anim)
        
        # Once animation finishes, remove the height constraint.
        self.animation_group.finished.connect(lambda: self.setMaximumHeight(16777215))
        self.animation_group.start(QAbstractAnimation.DeleteWhenStopped)


class ChatbotView(QWidget):
    """Elegant and modernized chatbot interface."""
    send_message_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chatbotView")
        self.setWindowTitle("AI Trading Assistant")

        self.messages = []  # Store message bubbles for reference.

        # Setup fonts and UI.
        self.setup_fonts()
        self.setup_ui()

    def wellcome_message(self):
        """Add a welcome message to the chat."""
        if not self.messages:
            self._add_assistant_message("Hello! I'm your AI trading assistant. How can I help you today?")

    def _enable_send_button_and_add_welcome_message(self):
        """Enable the send button and add the welcome message."""
        # (Implement if needed)

    def setup_fonts(self):
        """Set up custom fonts for more elegant typography."""
        self.body_font = QFont("Segoe UI", 12)

    def setup_ui(self):
        """Set up the refined UI components with modern design."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # App title with modern font.
        title = PageTitleLabel("AI Trading Assistant")
        main_layout.addWidget(title)

        # Enhanced chat area with better scrolling.
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

        # Message container.
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

        # Modern input area with solid color.
        input_frame = RoundedCard(border_radius=30, shadow_enabled=True)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 10)
        input_layout.setSpacing(15)

        # Enhanced text input with animation.
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

        # Send button with solid color.
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

        # Add components to main layout.
        main_layout.addWidget(self.chat_container, 1)
        main_layout.addWidget(input_frame, 0)

        self.setStyleSheet("""
            QWidget#chatbotView {
                background-color: #F0F0F5;
            }
        """)

    def _on_send_clicked(self):
        """Handle send button click with animation."""
        message = self.message_input.text().strip()
        if message:
            self._add_user_message(message)
            self.send_message_signal.emit(message)
            self.message_input.clear()
            self.message_input.setFocus()

    def _add_user_message(self, message):
        """Add a user message bubble."""
        self._add_message_bubble(message, is_user=True)

    def _add_assistant_message(self, message):
        """Add an assistant message bubble."""
        self._add_message_bubble(message, is_user=False)

    def _add_message_bubble(self, message, is_user=False):
        """Add an animated message bubble to the chat while ensuring proper order and scrolling."""
        # Remove any existing stretch before adding a new message.
        if self.message_layout.count() > 0:
            last_item = self.message_layout.itemAt(self.message_layout.count() - 1)
            if isinstance(last_item, QSpacerItem):
                self.message_layout.removeItem(last_item)

        # Create and add the message bubble.
        timestamp = QDateTime.currentDateTime()
        bubble = AnimatedMessageBubble(message, timestamp, is_user)
        self.message_layout.addWidget(bubble)
        self.messages.append(bubble)
        self.message_layout.addStretch()

        # Wait for animations to settle before scrolling.
        QTimer.singleShot(400, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """Smoothly scroll to the bottom of the chat container."""
        scrollbar = self.chat_container.verticalScrollBar()
        if scrollbar.value() < scrollbar.maximum():
            self.scroll_animation = QPropertyAnimation(scrollbar, b"value")
            self.scroll_animation.setDuration(300)
            self.scroll_animation.setStartValue(scrollbar.value())
            self.scroll_animation.setEndValue(scrollbar.maximum())
            self.scroll_animation.setEasingCurve(QEasingCurve.OutCubic)
            self.scroll_animation.start(QAbstractAnimation.DeleteWhenStopped)

    @Slot(str)
    def add_response(self, message):
        """Add an assistant response to the chat."""
        self._add_assistant_message(message)