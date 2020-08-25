import logging
import pathlib

from PyQt5.QtWidgets import QWidget, QMenuBar
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui.main_window import Ui_MainWindow

log = logging.getLogger(__name__)


class ControllerWindowWidget(QWidget, Ui_MainWindow):
    # device's signals
    send_gen_frequency = QtCore.pyqtSignal(float)
    send_gen_power = QtCore.pyqtSignal(float)
    send_frequencies = QtCore.pyqtSignal(dict)
    send_freq_sweep = QtCore.pyqtSignal(dict)
    send_power_sweep = QtCore.pyqtSignal(dict)
    send_type_analyzer = QtCore.pyqtSignal(str, str)
    send_type_generator = QtCore.pyqtSignal(str, str)
    send_gen_mode = QtCore.pyqtSignal()

    # chart signals
    send_ref = QtCore.pyqtSignal(int)
    send_db = QtCore.pyqtSignal(int)
    # data signals
    save_chart = QtCore.pyqtSignal(str)
    save_conf = QtCore.pyqtSignal()
    send_path_csv = QtCore.pyqtSignal(object)
    update_freq = QtCore.pyqtSignal(dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Main Window constructor"""
        self.setupUi(self)
        self.input_types_analyzer = ["USB0::2733::205::101274::0"]
        self.input_types_generator = ["USB0::2733::110::104791::0::INSTR"]

        # SET FREQUENCIES, PLOT, INPUT
        self.init_frequencies()
        self.init_plot()
        self.init_input_types()

        # SET ANALYZER
        self.analyzerConnectButton.clicked.connect(self.get_type_analyzer)
        self.fsetButton.clicked.connect(self.get_frequencies)

        # SET GENERATOR
        self.generatorConnectButton.clicked.connect(self.get_type_generator)
        self.fsetFreqButton.clicked.connect(self.get_freq_sweep)
        self.fsetPowerButton.clicked.connect(self.get_power_sweep)
        self.genPowerButton.clicked.connect(self.get_generator_power)
        self.genFreqButton.clicked.connect(self.get_generator_frequency)

        self.fsweepCheckBox.toggled.connect(lambda: self.psweepCheckBox.setChecked(False))
        self.psweepCheckBox.toggled.connect(lambda: self.fsweepCheckBox.setChecked(False))
        self.genOnButton.clicked.connect(self.set_generator_mode)


        # HANDLE DATA MANIPULATION
        self.jpegChartButton.clicked.connect(lambda: self.save_chart.emit("jpeg"))
        self.csvChartButton.clicked.connect(lambda: self.save_chart.emit("csv"))
        self.openButton.clicked.connect(self.load_data_csv)
        self.saveButton.clicked.connect(lambda: self.save_conf.emit())

        # SET CHART
        self.refButton.clicked.connect(self.get_ref)
        self.dbButton.clicked.connect(self.get_db)

        self.actionLoad.triggered.connect(self.load_data_csv)

    def set_generator_mode(self):
        if self.fsweepCheckBox.isChecked():
            self.send_gen_mode.emit()

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

    def get_generator_frequency(self):
        frequency = float(self.genFreqLineEdit.text())
        self.send_gen_frequency.emit(frequency)

    def get_generator_power(self):
        power = float(self.genPowerLineEdit.text())
        self.send_gen_power.emit(power)

    def get_frequencies(self):
        freqs_dict = {}
        freqs_dict['fstart'] = float(self.fstartLineEdit.text())
        freqs_dict['fstop'] = float(self.fstopLineEdit.text())
        freqs_dict['fstep'] = float(self.fstepLineEdit.text())
        freqs_dict['rbw'] = float(self.rbwLineEdit.text())

        self.send_frequencies.emit(freqs_dict)

    def get_freq_sweep(self):
        freqs_dict = {}
        freqs_dict['fstart'] = float(self.fstartFreqLineEdit.text())
        freqs_dict['fstop'] = float(self.fstopFreqLineEdit.text())
        freqs_dict['fstep'] = float(self.fstepFreqLineEdit.text())
        freqs_dict['time'] = float(self.timeFreqLineEdit.text())

        self.send_freq_sweep.emit(freqs_dict)

    def get_power_sweep(self):
        power_dict = {}
        power_dict['fstart'] = float(self.fstartPowerLineEdit.text())
        power_dict['fstop'] = float(self.fstopPowerLineEdit.text())
        power_dict['fstep'] = float(self.fstepPowerLineEdit.text())
        power_dict['time'] = float(self.timePowerLineEdit.text())

        self.send_power_sweep.emit(power_dict)

    def get_ref(self):
        ref = int(self.refLineEdit.text())
        self.graphWidget.setYRange(0, ref)

    def get_db(self):
        db = int(self.dbLineEdit.text())

    def init_frequencies(self):
        self.fstartLineEdit.setText(str(0))
        self.fstopLineEdit.setText(str(20))
        self.fstepLineEdit.setText(str(1))
        self.rbwLineEdit.setText(str(0))

        self.fstartFreqLineEdit.setText(str(0))
        self.fstopFreqLineEdit.setText(str(20))
        self.fstepFreqLineEdit.setText(str(1))
        self.timeFreqLineEdit.setText(str(0))

        self.fstartPowerLineEdit.setText(str(0))
        self.fstopPowerLineEdit.setText(str(20))
        self.fstepPowerLineEdit.setText(str(1))
        self.timePowerLineEdit.setText(str(0))
