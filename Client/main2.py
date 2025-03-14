from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

# Import the view class (assuming it's in a file named stock_market_view.py)
from stock_view2 import StockView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Market Dashboard")
        self.setGeometry(100, 100, 1200, 700)  # Set window size

        # Initialize main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add the stock market view
        self.stock_view = StockView()
        layout.addWidget(self.stock_view)

        self.show()  # Show the main window


if __name__ == "__main__":
    import sys

    print("df")
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
