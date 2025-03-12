from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame
)
from PySide6.QtCore import Qt, QPointF, QMargins
from PySide6.QtGui import QColor, QPen, QFont, QPainter, QLinearGradient, QGradient
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries

class StockPerformanceChart(QWidget):
    def __init__(self, parent=None, data=None, min_y=None, max_y=None, title="Stock Performance"):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create chart
        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setTitleFont(QFont("Arial", 16))
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QMargins(10, 10, 10, 10))
        self.chart.setContentsMargins(10, 10, 10, 10)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeLight)
        self.chart.setDropShadowEnabled(True)
        
        # Create line series
        self.series = QLineSeries()
        self.series.setPen(QPen(QColor("#4C6FFF"), 3))
        
        # Create area series for shaded area under curve
        self.area_series = QAreaSeries(self.series)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(76, 111, 255, 150))
        gradient.setColorAt(1.0, QColor(76, 111, 255, 20))
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        self.area_series.setBrush(gradient)
        self.area_series.setPen(Qt.NoPen)
        
        # Add data to series
        if data is None:
            data = self.generate_random_data()
        
        self.update_chart_data(data, min_y, max_y)
        
        # Create chart view
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(300)
        
        # Add padding around the chart
        chart_container = QFrame()
        chart_container.setObjectName("chartContainer")
        chart_container.setStyleSheet("""
            #chartContainer {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #EAEAEA;
            }
        """)
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(10, 20, 10, 10)
        chart_layout.addWidget(self.chart_view)
        
        self.layout.addWidget(chart_container)
    
    def update_chart_data(self, data, min_y=None, max_y=None):
        """Update the chart with new data"""
        self.series.clear()
        
        for i, value in enumerate(data):
            self.series.append(QPointF(i, value))
        
        # Remove existing series and axes
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
        for series in self.chart.series():
            self.chart.removeSeries(series)
        
        # Add series
        self.chart.addSeries(self.area_series)
        self.chart.addSeries(self.series)
        
        # Create X axis
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, len(data) - 1)
        self.axis_x.setLabelsVisible(False)
        self.axis_x.setGridLineVisible(True)
        self.axis_x.setGridLineColor(QColor("#E5E5E5"))
        self.axis_x.setTickCount(10)
        self.axis_x.setLinePenColor(QColor("#CCCCCC"))
        
        # Create Y axis
        self.axis_y = QValueAxis()
        if min_y is not None and max_y is not None:
            self.axis_y.setRange(min_y, max_y)
        else:
            self.axis_y.setRange(min(data) * 0.9, max(data) * 1.1)
        self.axis_y.setLabelsVisible(True)
        self.axis_y.setGridLineVisible(True)
        self.axis_y.setGridLineColor(QColor("#E5E5E5"))
        self.axis_y.setTickCount(6)
        self.axis_y.setLinePenColor(QColor("#CCCCCC"))
        self.axis_y.setLabelFormat("%.0f")
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)
        self.area_series.attachAxis(self.axis_x)
        self.area_series.attachAxis(self.axis_y)
    
    def generate_random_data(self, points=30, start_value=1000):
        """Generate random data for testing"""
        import random
        data = [start_value]
        for i in range(1, points):
            change = random.uniform(-0.05, 0.05)
            new_value = data[-1] * (1 + change)
            data.append(new_value)
        return data
    
    def set_chart_title(self, title):
        """Set the chart title"""
        self.chart.setTitle(title)