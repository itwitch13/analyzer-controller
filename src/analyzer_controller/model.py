from random import randint

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
import numpy
import pandas as pd


class MainModel(QWidget):
    send_axis = QtCore.pyqtSignal(list, list)
    send_analyzer_name = QtCore.pyqtSignal(str)
    send_generator_name = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.xaxis = []
        self.yaxis = []

    def connect_analyzer(self, device, type):
        self.send_analyzer_name.emit(device)

    def connect_generator(self, device, type):
        self.send_generator_name.emit(device)

    def update_plot(self):
        self.yaxis = self.generate_y(len(self.xaxis))
        self.send_axis.emit(self.xaxis, self.yaxis)

    def load_data(self, path):
        if path.suffix == ".csv":
            self.df_dbm = pd.read_csv(str(path))
            self.xaxis = list(self.df_dbm.columns.values)
            self.yaxis = self.df_dbm.values.tolist()[0]
        print(self.xaxis)
        print(self.yaxis)
        self.send_axis.emit(self.xaxis, self.yaxis)

    def set_frequencies(self, freqs):
        self.xaxis = [i for i in numpy.arange(freqs['fstart'], freqs['fstop'], freqs['fstep'])]

    def generate_y(self, num):
        y = []
        for i in range(0, num):
            y.append(randint(0, 100))
        return y

    def set_freq_sweep(self, freqs):
        print("freq sweep ", freqs)

    def set_power_sweep(self, freqs):
        print("power sweep ", freqs)
