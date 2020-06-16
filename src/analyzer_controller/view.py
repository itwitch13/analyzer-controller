import logging
import pathlib
from random import randint

from PyQt5.QtWidgets import QWidget, QMenuBar
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.main_window2 import Ui_MainWindow

log = logging.getLogger(__name__)


class AnalyzerWindowWidget(QWidget, Ui_MainWindow):
    send_frequencies = QtCore.pyqtSignal(dict)
    send_freq_sweep = QtCore.pyqtSignal(dict)
    send_power_sweep = QtCore.pyqtSignal(dict)
    send_ref = QtCore.pyqtSignal(int)
    send_db = QtCore.pyqtSignal(int)
    send_path_csv = QtCore.pyqtSignal(object)
    send_type_analyzer = QtCore.pyqtSignal(str, str)
    send_type_generator = QtCore.pyqtSignal(str, str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Main Window constructor"""
        self.setupUi(self)
        self.input_types_analyzer = ["USB0::2733::205::101274::0"]
        self.input_types_generator = ["TCPIP::169.254.2.20::hislip0::INSTR"]

        self.init_plot()
        self.init_input_types()
        self.singleCheckBox.setChecked(True)

        self.analyzerConnectButton.clicked.connect(self.get_type_analyzer)
        self.generatorConnectButton.clicked.connect(self.get_type_generator)
        self.fsetButton.clicked.connect(self.get_frequencies)
        self.fsetButton_2.clicked.connect(self.get_freq_sweep)
        self.fsetButton_3.clicked.connect(self.get_power_sweep)

        self.refButton.clicked.connect(self.get_ref)
        self.dbButton.clicked.connect(self.get_db)

        self.actionLoad.triggered.connect(self.load_data_csv)
        # self.continouseCheckBox.isChecked.connect(self.)
        # self.singleCheckBox.isChecked.connect(self.)


        # hours = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # self.graphWidget.plot(hours, temperature)

        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(50)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

    def load_data_csv(self):
        """
        Opens QFileDialog and sends chosen file directory as pathlib.Path object
        """
        csv_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose csv File", "", "Video File (" "*.csv)"
        )
        self.send_path_csv.emit(pathlib.Path(csv_path))

    def init_plot(self):

        self.graphWidget.setBackground('w')
        self.graphWidget.plot([0], [0], pen='r')
        # self.graphWidget.setTitle("ref_TL", color='blue', size=30)
        # Add Axis Labels
        self.graphWidget.setLabel('left', 'Spectral power [dBm]', color='black', size=2000)
        self.graphWidget.setLabel('bottom', 'Siggen freq [GHz]', color='black', size=80)

    def init_input_types(self):
        self.analyzerComboBox.addItems(self.input_types_analyzer)
        self.generatorComboBox.addItems(self.input_types_generator)

    def get_type_analyzer(self):
        type = str(self.analyzerComboBox.currentText())
        self.send_type_analyzer.emit("analyzer", type)

    def get_type_generator(self):
        type = str(self.generatorComboBox.currentText())
        self.send_type_generator.emit("generator", type)

    def set_analyzer_name(self, device_name):
        self.analyzerLineEdit.setText(device_name)

    def set_generator_name(self, device_name):
        self.generatorLineEdit.setText(device_name)

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.graphWidget.setData(self.x, self.y)  # Update the data.

    def create_plot(self, xaxis):

        # plot data: x, y values
        self.graphWidget.plot(xaxis, xaxis)

    def get_frequencies(self):
        freqs_dict = {}
        freqs_dict['fstart'] = float(self.fstartLineEdit.text())
        freqs_dict['fstop'] = float(self.fstopLineEdit.text())
        freqs_dict['fstep'] = float(self.fstepLineEdit.text())
        freqs_dict['rbw'] = float(self.fbwLineEdit.text())

        self.send_frequencies.emit(freqs_dict)

    def get_freq_sweep(self):
        freqs_dict = {}
        freqs_dict['fstart'] = float(self.fstartLineEdit_2.text())
        freqs_dict['fstop'] = float(self.fstopLineEdit_2.text())
        freqs_dict['fstep'] = float(self.fstepLineEdit_2.text())
        freqs_dict['rbw'] = float(self.fbwLineEdit_2.text())

        self.send_freq_sweep.emit(freqs_dict)

    def get_power_sweep(self):
        power_dict = {}
        power_dict['fstart'] = float(self.fstartLineEdit_3.text())
        power_dict['fstop'] = float(self.fstopLineEdit_3.text())
        power_dict['fstep'] = float(self.fstepLineEdit_3.text())
        power_dict['rbw'] = float(self.fbwLineEdit_3.text())

        self.send_power_sweep.emit(power_dict)

    def get_ref(self):
        ref = int(self.refLineEdit.text())
        self.graphWidget.setYRange(0, ref)

    def get_db(self):
        db = int(self.dbLineEdit.text())

