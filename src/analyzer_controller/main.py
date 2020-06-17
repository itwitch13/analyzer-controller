import sys
import logging

from PyQt5 import QtCore, QtGui, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from .view import AnalyzerWindowWidget
from .model import MainModel

log = logging.getLogger(__name__)


class AnalyzerController(QtWidgets.QMainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Analyzer Controller")
        # self.setStyleSheet()

        # View
        self.analyzer_widget = AnalyzerWindowWidget()
        self.setCentralWidget(self.analyzer_widget)
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

        # Model
        self.model = MainModel()

        # Connections

        self.analyzer_widget.singleCheckBox.toggled.connect(lambda: self.analyzer_widget.continuousCheckBox.setChecked(False))
        self.analyzer_widget.singleCheckBox.toggled.connect(self.set_single_mode)
        self.analyzer_widget.continuousCheckBox.toggled.connect(lambda: self.analyzer_widget.singleCheckBox.setChecked(False))
        self.analyzer_widget.continuousCheckBox.toggled.connect(self.set_contin_mode)


        # view to model
        self.analyzer_widget.send_type_analyzer.connect(self.model.connect_analyzer)
        self.analyzer_widget.send_type_generator.connect(self.model.connect_generator)

        self.analyzer_widget.send_frequencies.connect(self.model.set_frequencies)
        self.analyzer_widget.send_freq_sweep.connect(self.model.set_freq_sweep)
        self.analyzer_widget.send_power_sweep.connect(self.model.set_power_sweep)

        self.analyzer_widget.send_path_csv.connect(self.model.load_data)

        # view to main

        # view to view

        # model to view
        self.model.send_axis.connect(self.analyzer_widget.create_plot)
        self.model.send_analyzer_name.connect(self.analyzer_widget.set_analyzer_name)
        self.model.send_generator_name.connect(self.analyzer_widget.set_generator_name)

        # model to main

    def set_contin_mode(self):
        """
        Sets continuous mode that updates plot every 200ms.
        """
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.model.update_plot)
        self.timer.start()
        if not self.analyzer_widget.continuousCheckBox.isChecked():
            self.timer.stop()

    def set_single_mode(self):
        """
        Sets single mode that updates plot just once.
        """
        self.model.update_plot()
        self.analyzer_widget.singleCheckBox.setChecked(False)


def myExceptionhook(exc_type, exc_value, exc_traceback):
    log.critical("Unexpected exception occurred!",
                 exc_info=(exc_type, exc_value, exc_traceback))


def main(argv=sys.argv):
    sys.excepthook = myExceptionhook
    app = QApplication(argv)
    gui = AnalyzerController()

    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()