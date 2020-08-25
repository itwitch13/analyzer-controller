from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
import numpy
import pandas as pd
import pyqtgraph as pg
import pyqtgraph.exporters


class DataManipulator(QWidget):
    send_axis = QtCore.pyqtSignal(list, list)

    def __init__(self):
        super().__init__()
        self.freq_sweep = {}
        self.power_sweep = {}
        self.freq = {}
        self.xaxis = []
        self.yaxis = []

    def update_plot_param(self, x, y):
        self.xaxis = x
        self.yaxis = y

    def save_chart(self, type):
        print("saved", type)
        if type == "jpeg":
            chart = pg.plot(self.xaxis, self.yaxis)
            # the item you wish to export
            exporter = pg.exporters.ImageExporter(chart.plotItem)

            # set export parameters if needed
            exporter.parameters()['width'] = 100  # (note this also affects height parameter)

            # save to file
            exporter.export('plot.png')
        if type == "csv":
            pass

    def open_file(self, path):
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

    def update_configuration(self, freq, freq_sweep, power_sweep):
        self.freq = freq
        self.freq_sweep = freq_sweep
        self.power_sweep = power_sweep
        print("Updated!")

    def save_configuration(self):
        """
        Creates txt file with device configurations.
        """
        freqs_list = [self.freq, self.freq_sweep, self.power_sweep]
        config_list = ["Spectrum Analyzer\nFrequencies:\n",
                       "Signal Generator\nFrequencies sweep:\n",
                       "Power sweep:\n"]

        path = "/Users/blania/Desktop/analyzer_controller/adds/"
        file = open(path + "configuration.txt", "w+")
        for config, freqs in zip(config_list, freqs_list):
            file.write(config)

            for key in freqs:
                file.write("{}: {}\n".format(key, freqs[key]))
            file.write("\n")
        file.close()



