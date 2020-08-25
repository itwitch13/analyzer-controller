import sys
import unittest
from unittest.mock import patch
from unittest.mock import Mock

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from src.analyzer_controller.DeviceConfigurator import DevicesConfigurator
from src.analyzer_controller.AppView import ControllerWindowWidget


class DeviceConfiguratorTest(unittest.TestCase):

    def setUp(self):
        widget = QtWidgets.QApplication(sys.argv)
        widgetView = QWidget
        ui = Mock()
        self.deviceMock = DevicesConfigurator()
        self.view = ControllerWindowWidget()

    def test_init(self):
        self.type = "Rohde&Schwarz"
        self.dev = "device"

    def test_connect_analyzer(self):
        self.view.send_type_analyzer.connect(self.deviceMock.connect_analyzer)
        self.view.get_type_analyzer()
        self.view.assertSignalArrived("send_type_analyzer")
        self.deviceMock.connect_analyzer_mock(self.dev, self.type)

    @patch('src.analyzer_controller.DeviceConfigurator.update_configuration')
    def test_set_freq(self):
        freqs_example = {'fstop': 10, 'fstep': 2, 'fstart': 0}
        self.deviceMock.set_frequencies(freqs_example)

    @patch('src.analyzer_controller.DeviceConfigurator.set_gen_power')
    @patch('src.analyzer_controller.DeviceCommunicator.set_parameters_power')
    def test_set_freq_sweep(self, mock_set_parameters_power, mock_set_gen_power):
        pwer = 1000

        mock_set_gen_power.side_effects = pwer

        mock_set_parameters_power.assert_callled_once()

