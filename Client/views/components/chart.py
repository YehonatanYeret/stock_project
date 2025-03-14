import sys
sys.path.append('..')

from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QAreaSeries,
    QDateTimeAxis, QValueAxis
)
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPen
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pandas as pd

# Import the styled ContentCard for consistent styling
from components.styled_widgets import ContentCard

class StockChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a ContentCard to wrap the chart
        self.card = ContentCard(self)
        
        # Initialize the chart with light mode options
        self.chart = QChart()
        self.chart.setTitle("Stock Baseline Chart")
        self.chart.legend().hide()
        self.chart.setBackgroundBrush(Qt.white)
        self.chart.setPlotAreaBackgroundBrush(Qt.white)
        self.chart.setPlotAreaBackgroundVisible(True)
        
        # Create the chart view with antialiasing for smooth lines
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        # Place the chart view inside the ContentCard layout
        card_layout = QVBoxLayout(self.card)
        card_layout.addWidget(self.chart_view)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Main layout for the widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.card)
        self.setLayout(main_layout)
    
    def update_chart(self, data):
        """
        Update the chart with new stock data.
        
        :param data: List of dictionaries with keys:
                     't' - timestamp in ms,
                     'c' - close price.
        """
        df = pd.DataFrame(data)
        required_columns = {'t', 'c'}
        if not required_columns.issubset(df.columns):
            print("Error: Missing required columns in data")
            return
        
        # Convert timestamps and sort by datetime
        df['datetime'] = pd.to_datetime(df['t'], unit='ms')
        df = df.sort_values('datetime')
        
        # Create the stock price series
        stock_series = QLineSeries()
        for _, row in df.iterrows():
            # Use the QDateTime (in ms) as x-value and the close price as y-value
            timestamp = QDateTime(row['datetime']).toMSecsSinceEpoch()
            stock_series.append(timestamp, row['c'])
        
        # Calculate a baseline value (e.g., the average close price)
        baseline_value = df['c'].mean()
        baseline_series = QLineSeries()
        if not df.empty:
            start_ts = QDateTime(df['datetime'].iloc[0]).toMSecsSinceEpoch()
            end_ts = QDateTime(df['datetime'].iloc[-1]).toMSecsSinceEpoch()
            baseline_series.append(start_ts, baseline_value)
            baseline_series.append(end_ts, baseline_value)
        
        # Create an area series to fill between the stock price and the baseline
        area_series = QAreaSeries(stock_series, baseline_series)
        
        # Set a gradient fill for the area series (mimicking baseline fills)
        gradient = QLinearGradient()
        gradient.setStart(0, 0)
        gradient.setFinalStop(0, 1)
        # Use a gradient similar to: topFillColor1 rgba(38,198,218,0.28) to topFillColor2 rgba(38,198,218,0.05)
        gradient.setColorAt(0.0, QColor(38, 198, 218, int(0.28 * 255)))
        gradient.setColorAt(1.0, QColor(38, 198, 218, int(0.05 * 255)))
        area_series.setBrush(gradient)
        
        # Set pen (line) styling for the area series
        pen = QPen(QColor(38, 198, 218))
        pen.setWidth(2)
        area_series.setPen(pen)
        
        # Clear any existing series from the chart and add the new ones
        self.chart.removeAllSeries()
        self.chart.addSeries(area_series)
        self.chart.addSeries(baseline_series)
        
        # Create and attach a datetime axis for the x-axis
        axis_x = QDateTimeAxis()
        axis_x.setFormat("dd MMM")
        axis_x.setTitleText("Date")
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        area_series.attachAxis(axis_x)
        baseline_series.attachAxis(axis_x)
        
        # Create and attach a value axis for the y-axis
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%.2f")
        axis_y.setTitleText("Price")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        area_series.attachAxis(axis_y)
        baseline_series.attachAxis(axis_y)
        
        self.chart_view.repaint()
    
    def clear_chart(self):
        """Clears all series from the chart."""
        self.chart.removeAllSeries()
        self.chart_view.repaint()
