import logging
import pathlib

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
    send_single_mode = QtCore.pyqtSignal()
    send_mode = QtCore.pyqtSignal(str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Main Window constructor"""
        self.setupUi(self)
        self.input_types_analyzer = ["USB0::2733::205::101274::0"]
        self.input_types_generator = ["TCPIP::169.254.2.20::hislip0::INSTR"]

        self.init_plot()
        self.init_input_types()

        self.analyzerConnectButton.clicked.connect(self.get_type_analyzer)
        self.generatorConnectButton.clicked.connect(self.get_type_generator)
        self.fsetButton.clicked.connect(self.get_frequencies)
        self.fsetButton_2.clicked.connect(self.get_freq_sweep)
        self.fsetButton_3.clicked.connect(self.get_power_sweep)

        self.refButton.clicked.connect(self.get_ref)
        self.dbButton.clicked.connect(self.get_db)

        self.actionLoad.triggered.connect(self.load_data_csv)


    def load_data_csv(self):
        """
        Opens QFileDialog and sends chosen file directory as pathlib.Path object
        """
        csv_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose csv File", "", "File (" "*.csv)"
        )
        self.send_path_csv.emit(pathlib.Path(csv_path))

    def init_plot(self):
        """
        Initializes plot with specific properties.
        """
        self.graphWidget.setBackground('w')
        self.graphWidget.plot([0], [0], pen='r')

        # Add Axis Labels
        self.graphWidget.setTitle("ref_TL", color="b", size="30pt")
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel('left', 'Spectral power [dBm]', **styles)
        self.graphWidget.setLabel('bottom', 'Siggen freq [GHz]', **styles)

    def init_input_types(self):
        """
        Initializes types of device
        """
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

    def create_plot(self, xaxis, yaxis):
        """
        Creates new plot with given x and y axis.
        :param xaxis: list of values on x axis
        :param yaxis: list of values on y axis
        """
        self.graphWidget.clear()
        self.graphWidget.plot(xaxis, yaxis)

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

