from benchmark import *
from test_scenarios import *
from data_plotting import *

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Worker(QThread):
    finished = pyqtSignal(list)

    def __init__(self, func, **kwargs):
        super(Worker, self).__init__()
        self.func = func
        self.kwargs = kwargs

    def run(self):
        # Setting up the asyncio event loop for the thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(self.func(**self.kwargs))
        loop.close()
        self.finished.emit(results)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Web Server Benchmark Tool')
        self.setGeometry(100, 100, 1200, 900)  # Adjust size as needed

        layout = QGridLayout()

        # Control elements
        self.test_type_combo = QComboBox()
        self.test_type_combo.addItems(['constant', 'ramp_up', 'spike', 'stress'])
        layout.addWidget(QLabel('Test Type:'), 0, 0, 1, 1)
        layout.addWidget(self.test_type_combo, 0, 1, 1, 1)

        self.url_input = QLineEdit("https://www.wikipedia.org/")
        layout.addWidget(QLabel('URL:'), 1, 0)
        layout.addWidget(self.url_input, 1, 1)

        self.requests_input = QLineEdit("100")
        layout.addWidget(QLabel('Number of Requests:'), 2, 0)
        layout.addWidget(self.requests_input, 2, 1)

        # Buttons
        self.import_button = QPushButton('Import Old Data')
        self.import_button.clicked.connect(self.import_data)
        layout.addWidget(self.import_button, 3, 0)  # Aligns with the label on the left

        self.run_button = QPushButton('Run Benchmark')
        self.run_button.clicked.connect(self.run_benchmark)
        layout.addWidget(self.run_button, 3, 1)  # Aligns with the inputs on the right

        # Text area for displaying results
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)  # Make the text area read-only
        layout.addWidget(self.results_text, 4, 0, 1, 2)  # Span across the grid below buttons

        # Setup for multiple plots
        self.figures = [Figure() for _ in range(4)]
        self.canvases = [FigureCanvas(fig) for fig in self.figures]
        positions = [(5, 0), (5, 1), (6, 0), (6, 1)]
        for canvas, pos in zip(self.canvases, positions):
            layout.addWidget(canvas, pos[0], pos[1])

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def import_data(self):
        df = load_data("response_data_import.csv")  # Make sure this path is correctly set
        display_metrics(self.results_text, df)
        plot_response_time_distribution(self.figures[0], df)
        plot_response_time_percentiles(self.figures[1], df)
        plot_throughput(self.figures[2], df)
        plot_error_rate(self.figures[3], df)

    def run_benchmark(self):
        url = self.url_input.text()
        num_requests = int(self.requests_input.text()) if self.requests_input.text().isdigit() else 100
        test_type = self.test_type_combo.currentText()

        # Map GUI text to the function in your test scenarios
        test_func = self.get_test_function(test_type)
        if test_func:
            if test_type == 'spike':
              self.worker = Worker(test_func, url=url, peak_load=num_requests)
            elif test_type == 'stress':
              self.worker = Worker(test_func, url=url, start_requests=50, max_requests=num_requests, step=50, threshold_errors=20)
            else:
              self.worker = Worker(test_func, url=url, num_requests=num_requests)

            #self.worker = Worker(test_func, url=url, num_requests=num_requests)
            self.worker.finished.connect(self.handle_results)
            self.worker.start()

    def get_test_function(self, test_type):
        # This function should correctly map to your async test functions
        if test_type == 'constant':
            return run_constant_load_test
        elif test_type == 'ramp_up':
            return run_ramp_up_test
        elif test_type == 'spike':
            return run_spike_test
        elif test_type == 'stress':
            return run_stress_test

    def handle_results(self, results):
        write_results_to_csv(results)
        self.display_results(results)

    def display_results(self, results):
        df = load_data("response_data.csv")  # Make sure this path is correctly set
        display_metrics(self.results_text, df)
        plot_response_time_distribution(self.figures[0], df)
        plot_response_time_percentiles(self.figures[1], df)
        plot_throughput(self.figures[2], df)
        plot_error_rate(self.figures[3], df)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())