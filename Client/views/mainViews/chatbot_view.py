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


class AnimatedMessageBubble(RoundedCard):
    """An elegant message bubble with improved animation effects"""

    def __init__(self, message, timestamp, is_user=False, parent=None):
        super().__init__(parent=parent, border_radius=16, shadow_enabled=True)
        self.setObjectName("messageBubble")
        self.is_user = is_user

        # Initial setup for animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)

        # Initial size and position for slide animation
        self.initial_height = 0
        self.final_height = 0
        self.slide_offset = 50  # Pixels to slide from

        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        # Message text - using QTextEdit for auto-wrapping with better sizing
        self.message_label = QTextEdit(message)
        self.message_label.setReadOnly(True)
        self.message_label.setFrameStyle(QFrame.NoFrame)
        self.message_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.message_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.message_label.setMinimumHeight(10)
        self.message_label.document().contentsChanged.connect(self._adjust_height)

        # Improved text styling
        font = QFont()
        font.setPointSize(14)
        font.setFamily("Segoe UI")  # More modern font
        self.message_label.setFont(font)

        # Enhanced timestamp display
        time_str = timestamp.toString("HH:mm")
        self.time_label = StyledLabel(time_str, size=10, color="#888888")
        self.time_label.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)

        # Add widgets to layout
        layout.addWidget(self.message_label)
        layout.addWidget(self.time_label)

        # Style based on user or assistant
        if is_user:
            # Use the requested color scheme
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
            # Light color for assistant
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

        # Make sure height is properly adjusted
        QTimer.singleShot(10, self._adjust_height)

        # Start animations after a brief delay
        QTimer.singleShot(50, self._start_animations)

    def _adjust_height(self):
        """Adjust height of text area to fit content dynamically"""
        document = self.message_label.document()
        document_height = int(document.size().height())

        # Add some padding for better appearance
        self.message_label.setFixedHeight(document_height + 12)

        # Update the widget
        self.updateGeometry()

    def _start_animations(self):
        """Start combined animations for more attractive appearance"""
        # Create animation group for parallel animations
        self.animation_group = QParallelAnimationGroup()

        # Fade-in animation
        fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_anim.setDuration(350)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Slide-in animation
        start_x = -self.slide_offset if not self.is_user else self.slide_offset
        slide_anim = QPropertyAnimation(self, b"pos")
        slide_anim.setDuration(400)
        current_pos = self.pos()
        slide_anim.setStartValue(current_pos + QPoint(start_x, 0))
        slide_anim.setEndValue(current_pos)
        slide_anim.setEasingCurve(QEasingCurve.OutBack)

        # Add animations to group
        self.animation_group.addAnimation(fade_anim)
        self.animation_group.addAnimation(slide_anim)

        # Start animations
        self.animation_group.start(QAbstractAnimation.DeleteWhenStopped)


class ChatbotView(QWidget):
    """Elegant and modernized chatbot interface"""
    send_message_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chatbotView")
        self.setWindowTitle("AI Trading Assistant")

        self.messages = []  # Store message bubbles for reference

        # Setup fonts and UI
        self.setup_fonts()
        self.setup_ui()

    def wellcome_message(self):
        """Add a welcome message to the chat"""

        if not self.messages:
            # Add a welcome message if the chat is empty
            self._add_assistant_message("Hello! I'm your AI trading assistant. How can I help you today?")

    def _enable_send_button_and_add_welcome_message(self):
        """Enable the send button and add the welcome message"""

    def setup_fonts(self):
        """Set up custom fonts for more elegant typography"""

        self.body_font = QFont("Segoe UI", 12)

    def setup_ui(self):
        """Set up the refined UI components with modern design"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # App title with modern font
        title = PageTitleLabel("AI Trading Assistant")
        main_layout.addWidget(title)

        # Enhanced chat area with better scrolling
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

        # Message container
        self.message_container = QWidget()
        self.message_container.setObjectName("messageContainer")
        self.message_container.setStyleSheet("""
            #messageContainer {
                background-color: #F9F9FB;
            }
        """)

        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setContentsMargins(25, 25, 25, 25)
        self.message_layout.setSpacing(12)  # Reduced spacing for better look
        self.message_layout.setAlignment(Qt.AlignTop)
        self.message_layout.addStretch()

        self.chat_container.setWidget(self.message_container)

        # Modern input area with solid color
        input_frame = RoundedCard(border_radius=30, shadow_enabled=True)

        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 10)
        input_layout.setSpacing(15)

        # Enhanced text input with animation
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

        # Send button with solid color
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

        # Add components to main layout
        main_layout.addWidget(self.chat_container, 1)
        main_layout.addWidget(input_frame, 0)

        # Set a modern theme for the whole application
        self.setStyleSheet("""
            QWidget#chatbotView {
                background-color: #F0F0F5;
            }
        """)

    def _on_send_clicked(self):
        """Handle send button click with animation"""
        message = self.message_input.text().strip()
        if message:
            self._add_user_message(message)
            self.send_message_signal.emit(message)
            self.message_input.clear()
            self.message_input.setFocus()

    def _add_user_message(self, message):
        """Add a user message bubble"""
        self._add_message_bubble(message, is_user=True)

    def _add_assistant_message(self, message):
        """Add an assistant message bubble"""
        self._add_message_bubble(message, is_user=False)

    def _add_message_bubble(self, message, is_user=False):
        """Add an animated message bubble to the chat"""
        # Remove stretch if it exists
        for i in range(self.message_layout.count() - 1, -1, -1):
            item = self.message_layout.itemAt(i)
            if isinstance(item, QSpacerItem):
                self.message_layout.removeItem(item)
                break

        # Create and add the message bubble
        timestamp = QDateTime.currentDateTime()
        bubble = AnimatedMessageBubble(message, timestamp, is_user)
        self.message_layout.addWidget(bubble)

        # Store message for later reference
        self.messages.append(bubble)

        # Add stretch back to keep messages aligned to top
        self.message_layout.addStretch()

        # Improved scrolling - wait for animations to initialize
        QTimer.singleShot(100, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """Smooth scroll to bottom of chat"""
        scrollbar = self.chat_container.verticalScrollBar()

        # Calculate target position
        max_value = scrollbar.maximum()

        # Smooth scroll animation
        self.scroll_animation = QPropertyAnimation(scrollbar, b"value")
        self.scroll_animation.setDuration(300)
        self.scroll_animation.setStartValue(scrollbar.value())
        self.scroll_animation.setEndValue(max_value)
        self.scroll_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.scroll_animation.start(QAbstractAnimation.DeleteWhenStopped)

    @Slot(str)
    def add_response(self, message):
        """Add an assistant response to the chat"""
        self._add_assistant_message(message)
