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
                             QWidget)

from main import logAnalysis
from numpyArrayModel import NumpyArrayModel
from PandasModel import pandasModel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        self.table = QTableView()
        self.setCentralWidget(self.table)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open log File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 550, 450)
        self.setWindowTitle('File dialog')
        self.centralwidget = QWidget(self)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.comboBox = QComboBox(self.centralwidget)
        self.label = QLabel(self.centralwidget)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.label.setText("Regex Filter")

        self.horizontalHeader = self.table.horizontalHeader()
        # self.horizontalHeader.sectionClicked.connect(
        #     self.on_view_horizontalHeader_sectionClicked)
        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(
            self.on_comboBox_currentIndexChanged)

        self.show()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/var/log')

        # Create a Pandas DF bases on logAnalisys output
        df = pd.DataFrame(logAnalysis(fname[0]).parseLog())

        # Set the columns Names
        df.set_axis(logAnalysis(fname[0]).getHeader(),  axis=1, inplace=True)

        # Create a specific model for the table (MVC)
        model = pandasModel(df)
        # model = NumpyArrayModel(df,logAnalysis(fname[0]).getHeader())
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
        self.comboBox.addItems([logAnalysis(fname[0]).getHeader()[x]
                               for x in range(model.columnCount())])

    # def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
    #     self.logicalIndex = logicalIndex
    #     self.menuValues = QMenu(self)
    #     self.signalMapper = QSignalMapper(self)

    #     self.comboBox.blockSignals(True)
    #     self.comboBox.setCurrentIndex(self.logicalIndex)
    #     self.comboBox.blockSignals(True)

    #     valuesUnique = [self._model.item(row, self.logicalIndex).text()
    #                     for row in range(self._model.rowCount())
    #                     ]

    #     actionAll = QAction("All", self)
    #     actionAll.triggered.connect(self.on_actionAll_triggered)
    #     self.menuValues.addAction(actionAll)
    #     self.menuValues.addSeparator()

    #     for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
    #         action = QAction(actionName, self)
    #         self.signalMapper.setMapping(action, actionNumber)
    #         action.triggered.connect(self.signalMapper.map)
    #         self.menuValues.addAction(action)

    #     self.signalMapper.mapped.connect(self.on_signalMapper_mapped)

    #     headerPos = self.view.mapToGlobal(self.horizontalHeader.pos())

    #     posY = headerPos.y() + self.horizontalHeader.height()
    #     posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

    #     self.menuValues.exec_(QPoint(posX, posY))
    def on_lineEdit_textChanged(self, text):
        search = QRegExp(text,
                         Qt.CaseInsensitive,
                         QtCore.QRegExp.RegExp
                         )
        self.proxy.setFilterRegExp(search)

    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
