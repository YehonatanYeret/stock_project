from PySide6.QtWidgets import (
    QPushButton, QLineEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QGraphicsDropShadowEffect,
    QHeaderView, QScrollArea, QSizePolicy, QDateEdit, QWidget
)
from PySide6.QtGui import (
    QPixmap, QColor, QFont, QPainter, QPen, QBrush, QLinearGradient
)
from PySide6.QtCore import Qt, QMargins, QPointF, QDate
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis


# ========== TEXT ELEMENTS ==========

class StyledLabel(QLabel):
    def __init__(self, text, is_title=False, size=None, color=None, font_weight=None, margin_bottom=0, parent=None):
        super().__init__(text, parent)

        # Default values
        default_size = 18 if is_title else 14
        default_weight = "bold" if is_title else "normal"
        default_color = "#333333" if is_title else "#555555"

        # Use provided values or defaults
        font_size = size or default_size
        font_weight = font_weight or default_weight
        font_color = color or default_color
        margin = f"margin-bottom: {margin_bottom}px;" if margin_bottom > 0 else ""

        self.setStyleSheet(f"""
            QLabel {{
                font-size: {font_size}px;
                font-weight: {font_weight};
                color: {font_color};
                background: none;
                border: none;
                padding: 0px;
                {margin}
            }}
        """)


class PageTitleLabel(StyledLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, True, 24, "#333", parent=parent)
        self.setObjectName("PageTitle")


class SectionTitleLabel(StyledLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, True, 18, "#333", parent=parent)
        self.setObjectName("SectionTitle")


# ========== BUTTONS ==========

class StyledButton(QPushButton):
    def __init__(self, text, bg_color="#4C6FFF", hover_color="#3A5BCC",
                 pressed_color="#2D49A3", text_color="white",
                 border_radius=4, padding="8px 16px", font_size=14,
                 object_name=None, parent=None):
        super().__init__(text, parent)

        if object_name:
            self.setObjectName(object_name)
            obj_selector = f"#{object_name}"
        else:
            obj_selector = "QPushButton"

        self.setStyleSheet(f"""
            {obj_selector} {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: {border_radius}px;
                padding: {padding};
                font-size: {font_size}px;
                font-weight: bold;
            }}
            {obj_selector}:hover {{
                background-color: {hover_color};
            }}
            {obj_selector}:pressed {{
                background-color: {pressed_color};
            }}
            {obj_selector}:disabled {{
                background-color: #CCCCCC;
                color: #888888;
            }}
        """)


class PrimaryButton(StyledButton):
    def __init__(self, text, object_name=None, parent=None):
        super().__init__(
            text=text,
            bg_color="#3B82F6",
            hover_color="#2563EB",
            pressed_color="#1D4ED8",
            border_radius=10,
            padding="10px 25px",
            font_size=15,
            object_name=object_name,
            parent=parent
        )
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)


class DangerButton(StyledButton):
    def __init__(self, text, object_name=None, parent=None):
        super().__init__(
            text=text,
            bg_color="#FF4D4D",
            hover_color="#D43F3F",
            pressed_color="#B53131",
            border_radius=10,
            padding="10px 25px",
            font_size=15,
            object_name=object_name,
            parent=parent
        )
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)


class SuccessButton(StyledButton):
    def __init__(self, text, object_name=None, parent=None):
        super().__init__(
            text=text,
            bg_color="#10B981",
            hover_color="#059669",
            pressed_color="#047857",
            object_name=object_name,
            parent=parent
        )


class CompactButton(StyledButton):
    def __init__(self, text="", color="#4C6FFF", hover_color="#3A5BCC", pressed_color="#2D49A3", parent=None):
        super().__init__(
            text=text,
            bg_color=color,
            hover_color=hover_color,
            pressed_color=pressed_color,
            padding="4px 10px",
            font_size=12,
            parent=parent
        )
        self.setFixedSize(60, 24)


class SellButton(CompactButton):
    def __init__(self, text="Sell", parent=None):
        super().__init__(text, color="#FF4D4D", hover_color="#D43F3F", pressed_color="#B53131", parent=parent)


class ToggleButton(QPushButton):
    def __init__(self, text, object_name, is_checked=False, active_color="#4C6FFF", parent=None):
        super().__init__(text, parent)
        self.setObjectName(object_name)
        self.setCheckable(True)
        self.setChecked(is_checked)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(45)

        self.setStyleSheet(f"""
            #{object_name} {{
                background-color: #F1F5F9;
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 15px;
                color: #334155;
            }}
            #{object_name}:checked {{
                background-color: {active_color};
                color: white;
                border: 2px solid {active_color};
            }}
            #{object_name}:hover:!checked {{
                background-color: #E2E8F0;
            }}
        """)


class BuyToggleButton(ToggleButton):
    def __init__(self, text="Buy", object_name="buyButton", is_checked=False, parent=None):
        super().__init__(text, object_name, is_checked, "#10B981", parent)


class SellToggleButton(ToggleButton):
    def __init__(self, text="Sell", object_name="sellButton", is_checked=False, parent=None):
        super().__init__(text, object_name, is_checked, "#EF4444", parent)


# ========== INPUT FIELDS ==========

class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px 15px;
                background-color: #F8FAFC;
                font-size: 15px;
                color: #1E293B;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
                background-color: white;
            }
        """)


class StyledDateEdit(QDateEdit):
    def __init__(self, default_date=None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(45)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd/MM/yyyy")

        if default_date:
            self.setDate(default_date)
        else:
            self.setDate(QDate.currentDate())

        self.setStyleSheet("""
            QDateEdit {
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px 15px;
                background-color: #F8FAFC;
                font-size: 15px;
                color: #1E293B;
            }
            QDateEdit:focus {
                border: 2px solid #3B82F6;
                background-color: white;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 25px;
                border: none;
            }
        """)


class StyledComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                background-color: #F8FAFC;
                min-width: 150px;
                min-height: 45px;
                font-size: 15px;
                color: #1E293B;
            }
            QComboBox:focus {
                border: 2px solid #3B82F6;
                background-color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 25px;
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #E2E8F0;
                selection-background-color: #F5F5F5;
            }
        """)


# ========== CONTAINERS ==========

class Card(QFrame):
    def __init__(self, parent=None, shadow_enabled=True):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #EAEAEA;
            }
        """)

        # Apply shadow effect
        if shadow_enabled:
            self.apply_shadow()

    def apply_shadow(self, blur_radius=15, offset=4, opacity=25):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur_radius)
        shadow.setColor(QColor(0, 0, 0, opacity))
        shadow.setOffset(0, offset)
        self.setGraphicsEffect(shadow)


class RoundedCard(Card):
    def __init__(self, parent=None, border_radius=16, shadow_enabled=True):
        super().__init__(parent, shadow_enabled)
        self.setObjectName("roundedCard")
        self.setStyleSheet(f"""
            #roundedCard {{
                background-color: white;
                border-radius: {border_radius}px;
                border: 1px solid #EAEAEA;
            }}
        """)


class GradientCard(Card):
    def __init__(self, parent=None, start_color="#F0F9FF", end_color="#EFF6FF", border_color="#E0F2FE", shadow_enabled=True):
        super().__init__(parent, shadow_enabled)
        self.setObjectName("gradientCard")
        self.setStyleSheet(f"""
            #gradientCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start_color}, stop:1 {end_color});
                border-radius: 14px;
                border: 1px solid {border_color};
            }}
        """)


class StyledStatsCard(Card):
    def __init__(self, title, value, subtitle=None, icon=None, color="#5851DB", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setStyleSheet("""
            #StatCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #EAEAEA;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(5)

        # Header with title and optional icon
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

        # Value display
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: #000; font-size: 28px; font-weight: bold;")
        self.layout.addWidget(self.value_label)

        # Optional subtitle with trend arrow
        if subtitle:
            subtitle_layout = QHBoxLayout()
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


# ========== TABLES ==========

class StyledTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("StyledTable")
        self.setStyleSheet("""
            #StyledTable {
                background-color: white;
                border: none;
                gridline-color: #EAEAEA;
            }
            #StyledTable::item {
                padding: 5px;
            }
            #StyledTable QHeaderView::section {
                background-color: #F5F5F5;
                border: none;
                border-bottom: 1px solid #EAEAEA;
                padding: 8px;
                font-weight: bold;
                color: #333;
            }
            QTableView {
                alternate-background-color: #F9F9F9;
                background-color: white;
            }
        """)

        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)

        # Apply shadow
        self.apply_shadow()

    def apply_shadow(self, blur_radius=15, offset=4, opacity=25):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur_radius)
        shadow.setColor(QColor(0, 0, 0, opacity))
        shadow.setOffset(0, offset)
        self.setGraphicsEffect(shadow)


# ========== CHARTS ==========

class StyledChartView(QChartView):
    def __init__(self, title="Chart", parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create and configure chart
        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setTitleFont(QFont("Arial", 14, QFont.Bold))
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QMargins(10, 10, 10, 10))

        # Set chart as the view's chart
        self.setChart(self.chart)
        self.chart.setBackgroundBrush(QColor("white"))

        # Apply shadow
        self.apply_shadow()

    def apply_shadow(self, blur_radius=15, offset=4, opacity=25):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur_radius)
        shadow.setColor(QColor(0, 0, 0, opacity))
        shadow.setOffset(0, offset)
        self.setGraphicsEffect(shadow)


class StyledLineSeriesChart(StyledChartView):
    def __init__(self, title="Line Chart", color="#5851DB", parent=None):
        super().__init__(title, parent)
        self.setMinimumHeight(350)

        # Create series
        self.series = QLineSeries()
        self.series.setName("Data Series")

        # Apply styling to the series
        pen = QPen(QColor(color))
        pen.setWidth(3)
        self.series.setPen(pen)

        # Create gradient fill
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 300))
        gradient.setColorAt(0.0, QColor(*(QColor(color).getRgb()[:3] + (100,))))
        gradient.setColorAt(1.0, QColor(*(QColor(color).getRgb()[:3] + (0,))))
        self.series.setBrush(QBrush(gradient))

        # Create axes
        self.axisX = QDateTimeAxis()
        self.axisX.setFormat("MMM yyyy")
        self.axisX.setTitleText("Date")
        self.axisX.setLabelsAngle(-45)
        self.axisX.setLabelsFont(QFont("Arial", 9))

        self.axisY = QValueAxis()
        self.axisY.setTitleText("Value")
        self.axisY.setLabelFormat("%.2f")
        self.axisY.setLabelsFont(QFont("Arial", 9))

        # Add axes to chart
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        # Add series to chart and attach axes
        self.chart.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

    def set_y_label_format(self, format_str):
        """Set the format for Y-axis labels (e.g., '$%.2f')"""
        self.axisY.setLabelFormat(format_str)

    def set_axis_titles(self, x_title="Date", y_title="Value"):
        """Set the titles for both axes"""
        self.axisX.setTitleText(x_title)
        self.axisY.setTitleText(y_title)


# ========== SCROLL AREA ==========

class ScrollableContainer(QScrollArea):
    def __init__(self, parent=None, margins=(20, 20, 20, 20), spacing=20, bg_color="#F7F8FA"):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Container widget
        self.container = QWidget()
        self.setWidget(self.container)

        # Layout for the container
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(*margins)
        self.layout.setSpacing(spacing)

        # Style
        self.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {bg_color};
            }}
            QScrollBar:vertical {{
                background: #E2E8F0;
                width: 14px;
                margin: 0px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #94A3B8;
                min-height: 30px;
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #64748B;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)


# ========== LAYOUT HELPERS ==========

def create_form_field(label_text, input_field, label_size=14, is_bold=True, color="#334155", margin_bottom=5):
    """Create a form field with label and input"""
    layout = QVBoxLayout()

    label = StyledLabel(label_text, size=label_size, font_weight="bold" if is_bold else "normal",
                        color=color, margin_bottom=margin_bottom)

    layout.addWidget(label)
    layout.addWidget(input_field)

    return layout


# ========== UTILITY FUNCTIONS ==========

def apply_shadow_effect(widget, blur_radius=20, color=QColor(15, 23, 42, 40), offset=4):
    """Apply a shadow effect to a widget"""
    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(blur_radius)
    shadow_effect.setColor(color)
    shadow_effect.setOffset(0, offset)
    widget.setGraphicsEffect(shadow_effect)

'''
# UI Framework Components and Functions

## Charts
### StyledChartView(QChartView)
- `__init__(self, title="Chart", parent=None)`
- `apply_shadow(self, blur_radius=15, offset=4, opacity=25)`

### StyledLineSeriesChart(StyledChartView)
- `__init__(self, title="Line Chart", color="#58510B", parent=None)`
- `set_y_label_format(self, format_str)`
- `set_axis_titles(self, x_title="Date", y_title="Value")`

## Containers
### ScrollableContainer(QScrollArea)
- `__init__(self, parent=None, margins=(20, 20, 20, 20), spacing=20, bg_color="#F7F8FA")`

### Card(QFrame)
- `__init__(self, parent=None, shadow_enabled=True)`
- `apply_shadow(self, blur_radius=15, offset=4, opacity=25)`

### RoundedCard(Card)
- `__init__(self, parent=None, border_radius=16, shadow_enabled=True)`

### GradientCard(Card)
- `__init__(self, parent=None, start_color="#F0F9FF", end_color="#EFF6FF", border_color="#E0F2FE", shadow_enabled=True)`

### StyledStatsCard(Card)
- `__init__(self, title, value, subtitle=None, icon=None, color="#58510B", parent=None)`

## Tables
### StyledTable(QTableWidget)
- `__init__(self, parent=None)`
- `apply_shadow(self, blur_radius=15, offset=4, opacity=25)`

## Text Elements
### StyledLabel(QLabel)
- `__init__(self, text, is_title=False, size=None, color=None, font_weight=None, margin_bottom=0, parent=None)`

### PageTitleLabel(StyledLabel)
- `__init__(self, text, parent=None)`

### SectionTitleLabel(StyledLabel)
- `__init__(self, text, parent=None)`

## Buttons
### StyledButton(QPushButton)
- `__init__(self, text, bg_color="#4C6FFF", hover_color="#3A5BCC", pressed_color="#2D49A3", text_color="white", border_radius=4, padding="8px 16px", font_size=14, object_name=None, parent=None)`

### PrimaryButton(StyledButton)
- `__init__(self, text, object_name=None, parent=None)`

### DangerButton(StyledButton)
- `__init__(self, text, object_name=None, parent=None)`

### CompactButton(StyledButton)
- `__init__(self, text="", color="#4C6FFF", hover_color="#3A5BCC", pressed_color="#2D49A3", parent=None)`

### SellButton(CompactButton)
- `__init__(self, text="Sell", parent=None)`
  - [Calls `super().__init__(text, color="#FF4D4D", hover_color="#D43F3F", pressed_color="#B53131", parent=parent)`]

### ToggleButton(QPushButton)
- `__init__(self, text, object_name, is_checked=False, active_color="#4C6FFF", parent=None)`

### BuyToggleButton(ToggleButton)
- `__init__(self, text="Buy", object_name="buyButton", is_checked=False, parent=None)`
  - [Calls `super().__init__(text, object_name, is_checked, active_color="#10B981", parent)`]

### SellToggleButton(ToggleButton)
- `__init__(self, text="Sell", object_name="sellButton", is_checked=False, parent=None)`
  - [Calls `super().__init__(text, object_name, is_checked, active_color="#EF4444", parent)`]

## Input Fields
### StyledLineEdit(QLineEdit)
- `__init__(self, placeholder="", parent=None)`

### StyledDateEdit(QDateEdit)
- `__init__(self, default_date=None, parent=None)`

## Utility Functions
### create_form_field(label_text, input_field, label_size=14, is_bold=True, color="#334155", margin_bottom=5)

### apply_shadow_effect(widget, blur_radius=20, color=QColor(15, 23, 42, 40), offset=4)
'''