from random import randint

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
import numpy
import pandas as pd

from .DeviceCommunicator import DeviceCommunicator


class DevicesConfigurator(QWidget):
    send_axis = QtCore.pyqtSignal(list, list)
    send_analyzer_name = QtCore.pyqtSignal(str)
    send_generator_name = QtCore.pyqtSignal(str)
    send_plot_param = QtCore.pyqtSignal(list, list)
    send_conf = QtCore.pyqtSignal(dict, dict, dict)

    def __init__(self):
        super().__init__()
        self.xaxis = []
        self.yaxis = []
        self.freq_sweep = {}
        self.power_sweep = {}
        self.freq = {}
        self.device = DeviceCommunicator()

    def connect_analyzer(self, device, type):
        type = "Rohde&Schwarz,SMC100A,1411.4002k02/104791,3.1.18.2-3.01.134.22"
        self.send_analyzer_name.emit(type)

    def connect_generator(self, device, type):
        type = "Rohde&Schwarz,SMC100A,1411.4002k02/104791,3.1.18.2-3.01.134.22"
        self.send_generator_name.emit(type)
        self.device.connect_generator()

    def update_plot(self):
        """
        Send signal to updates plot.
        """
        self.yaxis = self.generate_y(len(self.xaxis))
        self.send_axis.emit(self.xaxis, self.yaxis)

    def load_data(self, path):
        """
        Gets data from csv file and  creates plot.
        :param path: path to csv file with data
        """
        if path.suffix == ".csv":
            self.df_dbm = pd.read_csv(str(path))
            xaxis = list(self.df_dbm.columns.values)
            self.xaxis = [float(i) for i in xaxis]
            self.yaxis = self.df_dbm.values.tolist()[0]

        self.send_axis.emit(self.xaxis, self.yaxis)

    def set_frequencies(self, freqs):
        """
        Creates xaxis from dictionary of given frequencies.
        :param freqs: dictionary of given frequencies
        """
        self.freq = freqs
        self.xaxis = [i for i in numpy.arange(freqs['fstart'], freqs['fstop'], freqs['fstep'])]
        self.update_configuration()

    def generate_y(self, num):
        """
        Gets yaxis from device
        """
        #TODO: zaimplementowanie pod urządzenie -> narazie bierze losowo
        y = []
        for i in range(0, num):
            y.append(randint(0, 100))
        return y

    def set_freq_sweep(self, freqs):
        self.freq_sweep = freqs
        print("freq sweep ", freqs)
        self.device.set_frequencies_sweep(freqs)
        # self.update_configuration()

    def set_power_sweep(self, powers):
        self.power_sweep = powers
        print("power sweep ", powers)
        # self.update_configuration()

    def set_gen_frequency(self, freq):
        self.device.set_parameters_freq(freq)
        self.freq = freq
        print("freq ", freq)
        # self.update_configuration()

    def set_gen_power(self, power):
        self.device.set_parameters_power(power)
        self.power = power
        print("power ", power)
        # self.update_configuration()

    def update_configuration(self):
        self.send_plot_param.emit(self.xaxis, self.yaxis)
        self.send_conf.emit(self.freq, self.freq_sweep, self.power_sweep)

    def set_sweep_mode(self):
        self.device.set_sweep_mode()
        # else:
        #     self.device.
