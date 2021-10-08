#!/usr/bin/env python

from pyqt5 import *
from pyqt5 import QtWidgets
from pyqt5.QtCore import QDateTime, Qt, QTimer
from pyqt5.QtWidgets import *

import sys

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.resize(1200,800)
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

        tab1 = QWidget()
        tableWidget = QTableWidget(10,10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        
        self.bottomLeftTabWidget.addTab(tab1, "&Table")



if __name__ == '__main__':
    app= QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    data = [
          [4, 9, 2, 0],
          [1, 0, 0, 0],
          [3, 5, 0, 0],
          [3, 3, 2, 0],
          [7, 8, 9, 0]
        ]
    
    gallery = WidgetGallery()
    gallery.show()

    app.exec_()
