import pathlib
import logging

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
from .ui.main_window import Ui_MainWindow

log = logging.getLogger(__name__)


class AnalyzerWindowWidget(QWidget, Ui_MainWindow):
    send_frequencies = QtCore.pyqtSignal(list)
    send_ref = QtCore.pyqtSignal(int)
    send_db = QtCore.pyqtSignal(int)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Main Window constructor"""
        self.setupUi(self)

        self.fsetButton.clicked.connect(self.get_frequencies)
        self.refButton.clicked.connect(self.get_ref)
        self.dbButton.clicked.connect(self.get_db)

        self.onlyInt = QtGui.QIntValidator()
        self.fstartLineEdit.setValidator(self.onlyInt)
        self.fstopLineEdit.setValidator(self.onlyInt)
        self.fstepLineEdit.setValidator(self.onlyInt)
        self.fbwLineEdit.setValidator(self.onlyInt)
        self.refLineEdit.setValidator(self.onlyInt)
        self.dbLineEdit.setValidator(self.onlyInt)

        self.graphWidget.setBackground('w')
        self.graphWidget.plot([0], [0])

    def create_plot(self):
        # self.graphWidget = pg.PlotWidget()
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        print(self.graphWidget.plot(hour, temperature))
        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)

    def get_frequencies(self):
        fstart = int(self.fstartLineEdit.text())
        fstop = int(self.fstopLineEdit.text())
        fstep = int(self.fstepLineEdit.text())
        fbw = int(self.fbwLineEdit.text())

        freqs = [fstart, fstop, fstep, fbw]
        self.send_frequencies.emit(freqs)

    def get_ref(self):
        ref = int(self.refLineEdit.text())
        self.send_ref.emit(ref)

    def get_db(self):
        db = int(self.dbLineEdit.text())
        self.send_db.emit(db)

