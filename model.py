from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget


class MainModel(QWidget):

    def __init__(self):
        super().__init__()

    def set_frequencies(self, freq_list):
        print(freq_list)

    def set_ref(self, ref):
        print(ref)

    def set_db(self, db):
        print(db)