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
        # view to model
        self.analyzer_widget.send_frequencies.connect(self.model.set_frequencies)
        self.analyzer_widget.send_ref.connect(self.model.set_ref)
        self.analyzer_widget.send_db.connect(self.model.set_db)

        # view to main

        # view to view

        # model to view

        # model to main



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