#!/usr/bin/env python

import sys

from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.initUI(self)

    def initUI(self):
        
        self.resize(1200, 800)
        self.setWindowTitle("AutoLog")

        combobox = QComboBox(self)
        combobox.addItem('Syslog')
        combobox.addItem('Apache')
        combobox.addItem('User')

        styleLabel = QLabel("&Type de log:")
        styleLabel.setBuddy(combobox)

        self.createBottomLeftTabWidget()

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(combobox)
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 1, 0)

        self.setLayout(mainLayout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                               QSizePolicy.Ignored)

        tableLog = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tableLog.setLayout(tab1hbox)

        self.bottomLeftTabWidget.addTab(tableLog, "&Table")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    app.exec_()
