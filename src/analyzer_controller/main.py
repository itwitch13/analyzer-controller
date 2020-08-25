import sys
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from .AppView import ControllerWindowWidget
from .DeviceConfigurator import DevicesConfigurator
from .DataManipulator import DataManipulator


log = logging.getLogger(__name__)


class DevController(QtWidgets.QMainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("DevController")
        # self.setStyleSheet()

        # View
        self.devWidget = ControllerWindowWidget()
        self.setCentralWidget(self.devWidget)
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

        # models
        self.deviceModel = DevicesConfigurator()
        self.dataModel = DataManipulator()

        # Connections
        self.devWidget.captureCheckBox.toggled.connect(lambda: self.devWidget.continuousCheckBox.setChecked(False))
        self.devWidget.continuousCheckBox.toggled.connect(lambda: self.devWidget.captureCheckBox.setChecked(False))

        self.devWidget.onButton.clicked.connect(self.set_mode)
        self.devWidget.offButton.clicked.connect(self.turn_off)

        # view to model
        # -------- DeviceModel --------
        self.devWidget.send_type_analyzer.connect(self.deviceModel.connect_analyzer)
        self.devWidget.send_type_generator.connect(self.deviceModel.connect_generator)

        self.devWidget.send_gen_mode.connect(self.deviceModel.set_sweep_mode)
        self.devWidget.send_gen_frequency.connect(self.deviceModel.set_gen_frequency)
        self.devWidget.send_gen_power.connect(self.deviceModel.set_gen_power)
        self.devWidget.send_frequencies.connect(self.deviceModel.set_frequencies)
        self.devWidget.send_freq_sweep.connect(self.deviceModel.set_freq_sweep)
        self.devWidget.send_power_sweep.connect(self.deviceModel.set_power_sweep)
        self.devWidget.send_path_csv.connect(self.deviceModel.load_data)

        # -------- DataModel --------
        self.devWidget.save_chart.connect(self.dataModel.save_chart)
        self.devWidget.send_path_csv.connect(self.dataModel.open_file)
        self.devWidget.save_conf.connect(self.dataModel.save_configuration)

        # model to view
        # -------- DeviceModel --------
        self.deviceModel.send_axis.connect(self.devWidget.create_plot)
        self.deviceModel.send_analyzer_name.connect(self.devWidget.set_analyzer_name)
        self.deviceModel.send_generator_name.connect(self.devWidget.set_generator_name)

        # -------- DataModel --------
        self.dataModel.send_axis.connect(self.devWidget.create_plot)

        # DeviceModel to DataModel
        self.deviceModel.send_conf.connect(self.dataModel.update_configuration)
        self.deviceModel.send_plot_param.connect(self.dataModel.update_plot_param)

        # view to main

        # view to view

        # deviceModel to main

    def turn_off(self):
        self.devWidget.continuousCheckBox.setChecked(False)
        self.devWidget.captureCheckBox.setChecked(False)
        self.set_mode()

    def set_mode(self):
        """
        Sets continuous mode that updates plot every ... ms or single mode.
        """
        if self.devWidget.captureCheckBox.isChecked():
            self.deviceModel.update_plot()

        else:
            self.timer = QtCore.QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.deviceModel.update_plot)
            self.timer.start()
            if not self.devWidget.continuousCheckBox.isChecked():
                self.timer.stop()


def myExceptionhook(exc_type, exc_value, exc_traceback):
    log.critical("Unexpected exception occurred!",
                 exc_info=(exc_type, exc_value, exc_traceback))


def main(argv=sys.argv):
    sys.excepthook = myExceptionhook
    app = QApplication(argv)
    gui = DevController()

    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()