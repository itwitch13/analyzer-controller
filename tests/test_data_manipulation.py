import unittest
import pandas as pd
from unittest.mock import patch
from unittest.mock import Mock
from PyQt5.QtWidgets import QWidget
from src.analyzer_controller.DataManipulator import DataManipulator
import pathlib


class DataExample(object):
    def __init__(self):
        self.freqs = []
        self.freq_sweep = []
        self.power_sweep = []

    def open_example(self, path):
        if path.suffix == ".csv":
            df_dbm = pd.read_csv(str(path))
            xaxis = list(df_dbm.columns.values)
            xaxis = [float(i) for i in xaxis]
            yaxis = [df_dbm.values.tolist()[0]]

        return xaxis, yaxis

    def update_example(self, freq, freq_sweep, power_sweep):
        freq = freq
        freq_sweep = freq_sweep
        power_sweep = power_sweep

        return freq, freq_sweep, power_sweep


class DataManipulatorTest(unittest.TestCase):

    def setUp(self):
        self.data_example = DataExample()
        self.data_manipulator = DataManipulator()

    def test_open_file(self):
        path = pathlib.Path("/Users/blania/Desktop/analyzer_controller/tests/data/sample.csv")
        param1, param2 = self.data_example.open_example(path)

        self.assertEqual(type(param1), list)
        self.assertEqual(type(param2), list)

    def test_update_example(self):
        p1, p2, p3 = 10, 20, 30

        param1, param2, param3 = self.data_example.update_example(p1,p2,p3)

        self.assertEqual(type(param1), int)
        self.assertEqual(type(param2), int)
        self.assertEqual(type(param3), int)


    def test_save_configuration(self):
        self.data_example.freqs = [0, 1, 2, 3,]
        self.data_example.freq_sweep = [0, 1, 2, 3, 4]
        self.data_example.power_sweep = [0, 1, 2, 3, 4]

        self.assertTrue(self.data_example.freqs, [0, 1, 2, 3])