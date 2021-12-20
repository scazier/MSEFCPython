import sys
from datetime import time
from pathlib import Path

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import (QPoint, QRegExp, QSignalMapper,
                          QSortFilterProxyModel, Qt)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QGridLayout, QLabel, QLineEdit, QMainWindow,
                             QMenu, QTableView, QTableWidget, QTextEdit,
                             QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QListWidgetItem)

from main import logAnalysis
# from numpyArrayModel import NumpyArrayModel
from PandasModel import pandasModel


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super().__init__()
        self.resize(1200,800)

        self.tabWidget = TableWidget(self)
        self.setCentralWidget(self.tabWidget)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open log File')
        openFile.triggered.connect(self.tabWidget.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.show()

class TableWidget(QWidget):
    def __init__(self,parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(400,300)

        self.tabs.addTab(self.tab1,"Analog")
        self.tabs.addTab(self.tab2,"Crawler")
        self.tabs.addTab(self.tab3,"Stat")

        self.analogUI()
        self.metadataUI()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def analogUI(self):
        self.tab1.layout = QVBoxLayout()
        self.tab1.Hlayout = QHBoxLayout()

        self.table = QTableView()

        self.centralwidget = QWidget(self)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.comboBox = QComboBox(self.centralwidget)
        self.labelRegex = QLabel(self.centralwidget)
        self.labelNumLines = QLabel(self)


        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.labelRegex, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.labelNumLines,2,0,1,1)

        self.labelRegex.setText("Regex Filter")

        self.horizontalHeader = self.table.horizontalHeader()

        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(
             self.on_comboBox_currentIndexChanged)

        self.tab1.Hlayout.addWidget(self.labelRegex)
        self.tab1.Hlayout.addWidget(self.lineEdit)
        self.tab1.Hlayout.addWidget(self.comboBox)
        self.tab1.layout.addLayout(self.gridLayout)
        self.tab1.layout.addLayout(self.tab1.Hlayout)
        self.tab1.layout.addWidget(self.table)
        self.tab1.layout.addWidget(self.labelNumLines)

        self.tab1.setLayout(self.tab1.layout)

    def metadataUI(self):
        self.tab2.layout = QHBoxLayout(
        self.metaTable = QTableView()
        )

        self.listWidget = QListWidget()
        QListWidgetItem("Geeks", self.listWidget)
        QListWidgetItem("For", self.listWidget)
        QListWidgetItem("Geeks", self.listWidget)

        self.tab2.layout.addWidget(self.listWidget)
        self.tab2.setLayout(self.tab2.layout)


    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/var/log')
        mylog = logAnalysis(fname[0])

        # Create a Pandas DF bases on logAnalisys output
        df = pd.DataFrame(mylog.parseLog())

        # Set the columns Names
        df.set_axis(mylog.getHeader(),  axis=1, inplace=True)

        # Create a specific model for the table (MVC)
        model = pandasModel(df)
        self._model = model
        # Apply the model to the QTableView
        self.table.setModel(model)

        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(model)
        self.table.setModel(self.proxy)
        self.comboBox.clear()
        self.comboBox.addItems([mylog.getHeader()[x]
                               for x in range(model.columnCount())])

        self.labelNumLines.setText("%s lines" % str(model.rowCount()))

    def on_lineEdit_textChanged(self, text):
        search = QRegExp(text, Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxy.setFilterRegExp(search)

    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    #mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
