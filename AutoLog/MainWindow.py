# -*- coding: utf-8 -*-
import os
import re
import sys
import requests
import exiftool
from datetime import time
from pathlib import Path
from bs4 import BeautifulSoup

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import (QPoint, QRegExp, QSignalMapper,
                          QSortFilterProxyModel, Qt)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QGridLayout, QLabel, QLineEdit, QMainWindow,
                             QMenu, QTableView, QTableWidget, QTextEdit,
                             QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QListWidgetItem, QPushButton,
                             QHeaderView, QSizePolicy, QMessageBox)

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
        self.tabs.addTab(self.tab2,"Metadata")
        self.tabs.addTab(self.tab3,"URL Regex")

        self.analogUI()
        self.metadataUI()
        self.websiteUI()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def analogUI(self):
        self.tab1.layout = QVBoxLayout()
        self.tab1.Hlayout = QHBoxLayout()
        self.tab1.HBottomLayout = QHBoxLayout()

        self.table = QTableView()

        self.centralwidget = QWidget(self)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.comboBox = QComboBox(self.centralwidget)
        self.labelRegex = QLabel(self.centralwidget)
        self.labelNumLines = QLabel(self)
        self.exportFilteredLogs = QPushButton("Export")
        self.exportFilteredLogs.clicked.connect(self.exportLogs)


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
        self.tab1.HBottomLayout.addWidget(self.labelNumLines, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.tab1.HBottomLayout.addWidget(self.exportFilteredLogs, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.tab1.layout.addLayout(self.tab1.HBottomLayout)

        self.tab1.setLayout(self.tab1.layout)

    def metadataUI(self):
        self.tab2.layout = QVBoxLayout()
        self.tab2.HUpLayout = QHBoxLayout()
        self.tab2.HBottomLayout = QHBoxLayout()
        self.metaTable = QTableView()

        self.linePath = QLineEdit()
        self.linePath.isReadOnly()
        self.linePath.dragEnabled()
        self.linePath.textChanged.connect(self.listFiles)
        self.labelPath = QLabel("Path:")
        self.openButton = QPushButton("", self)
        self.openButton.setIcon(QIcon("../imgs/folder.png"))
        self.openButton.clicked.connect(self.setMetadataPath)
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.displayMetadata)

        self.tab2.HUpLayout.addWidget(self.labelPath)
        self.tab2.HUpLayout.addWidget(self.linePath)
        self.tab2.HUpLayout.addWidget(self.openButton)
        self.tab2.HBottomLayout.addWidget(self.listWidget)
        self.tab2.HBottomLayout.addWidget(self.metaTable)

        self.tab2.layout.addLayout(self.tab2.HUpLayout)
        self.tab2.layout.addLayout(self.tab2.HBottomLayout)
        self.tab2.setLayout(self.tab2.layout)

    def websiteUI(self):
        self.tab3.layout = QVBoxLayout()
        self.tab3.HFirstLayout = QHBoxLayout()
        self.tab3.HSecondayout = QHBoxLayout()
        self.tab3.HMainLayout = QHBoxLayout()
        self.tab3.VSubmainLayout = QVBoxLayout()
        self.tab3.HBottomLayout = QHBoxLayout()

        self.labelURL = QLabel("URL:")
        self.lineURL = QLineEdit()
        self.labelURLRegex = QLabel("Regex:")
        self.lineRegex = QComboBox()
        self.lineRegex.edit = QLineEdit()
        self.lineRegex.setLineEdit(self.lineRegex.edit)
        self.lineRegex.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
        self.resultRegex = QListWidget()
        self.browseRegex = QPushButton("",self)
        self.browseRegex.setIcon(QIcon("../imgs/browsing.png"))
        self.browseRegex.clicked.connect(self.browseURL)
        self.exportRegex = QPushButton("Export")
        self.exportRegex.clicked.connect(self.exportMatchedRegex)
        self.regexMatches = QLabel()

        self.loadRegex()

        self.tab3.HFirstLayout.addWidget(self.labelURL)
        self.tab3.HFirstLayout.addWidget(self.lineURL)
        self.tab3.HSecondayout.addWidget(self.labelURLRegex)
        self.tab3.HSecondayout.addWidget(self.lineRegex)
        self.tab3.HBottomLayout.addWidget(self.regexMatches, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.tab3.HBottomLayout.addWidget(self.exportRegex, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.tab3.VSubmainLayout.addLayout(self.tab3.HFirstLayout)
        self.tab3.VSubmainLayout.addLayout(self.tab3.HSecondayout)
        self.tab3.HMainLayout.addLayout(self.tab3.VSubmainLayout)
        self.tab3.HMainLayout.addWidget(self.browseRegex)
        self.tab3.layout.addLayout(self.tab3.HMainLayout)
        self.tab3.layout.addWidget(self.resultRegex)
        self.tab3.layout.addLayout(self.tab3.HBottomLayout)
        self.tab3.setLayout(self.tab3.layout)

    def loadRegex(self):
        with open("URLRegex.conf") as regexConf:
            for line in regexConf:
                self.lineRegex.addItem(line.split(';')[0])

    def browseURL(self):
        if self.lineURL.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setInformativeText("No URL given")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        # Load basic regex (IP,emails,phone, ...)
        regex = ""
        with open("URLRegex.conf") as regexConf:
            for line in regexConf:
                line = line.split(';')
                if self.lineRegex.edit.text().lower() == line[0].lower():
                    regex = line[1]

        if regex == "":
            regex = self.lineRegex.edit.text()

        self.resultRegex.clear()
        response = requests.get(self.lineURL.text())
        soup = BeautifulSoup(response.text,'html.parser')

        if response.status_code != 200:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setInformativeText("An error occured, the URL return a status code: %" % response.status_code)
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        result = soup.find_all(text=re.compile(regex.strip()))

        if len(result) == 0:
            self.regexMatches.setText("0 match")

        for res in result:
            if re.fullmatch(re.compile(regex.strip()),res) is not None:
                QListWidgetItem(res,self.resultRegex)
            else:
                for _res in re.finditer(re.compile(regex.strip()),res):
                    QListWidgetItem(res[_res.start():_res.end()],self.resultRegex)

            self.regexMatches.setText("{} match".format(self.resultRegex.count()))

    def exportMatchedRegex(self):
        if self.resultRegex.count() == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setInformativeText("You cannot export an empty list")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Export regex", "", "csv")
        if filepath == "":
            return

        with open(filepath+'.csv','w') as file:
            for index in range(self.resultRegex.count()):
                file.write(self.resultRegex.item(index).text()+'\n')


    def setMetadataPath(self):
        path = QFileDialog.getExistingDirectory(self, 'Open file','/home/')
        if path != "":
            self.linePath.setText(path)

    def listFiles(self):
        if "file://" in self.linePath.text():
            tmpPath = self.linePath.text()[self.linePath.text().find("file://")+7:]
            self.linePath.clear()
            self.linePath.setText(tmpPath.strip())
            print(tmpPath.strip().encode('utf-8'))

        self.listWidget.clear()
        for root,directory,files in os.walk(self.linePath.text()):
            for i in files:
                QListWidgetItem(os.path.join(root,i), self.listWidget)

    def displayMetadata(self):
        #path = "/home/m0xy/Images/binary.png"
        path = self.listWidget.currentItem().text()
        if path[0] != "" and path[0] is not None:
            self.fileMetadata = {}
            with exiftool.ExifTool() as et:
                self.fileMetadata = dict(et.get_metadata(path))
            df = pd.DataFrame(self.fileMetadata.items())
            df.set_axis(["Property","Value"], axis=1, inplace=True)

            model = pandasModel(df)
            self.metaTable.setModel(model)
            self.metaTable.setAlternatingRowColors(True)
            self.metaTable.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.metaTable.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
            #self.metaTable.horizontalHeader().setStretchLastSection(True)
            self.metaTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

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
        self.labelNumLines.setText("%s lines" % self.table.model().rowCount())

    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)
        self.labelNumLines.setText("%s lines" % self.table.model().rowCount())

    def exportLogs(self):
        model = self.table.model()

        if model.rowCount() == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setInformativeText("You cannot export an empty list")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Export regex", "", "csv")
        if filepath == "":
            return

        with open(filepath+'.csv','w') as file:
            for row in range(model.rowCount()):
                line = []
                for column in range(model.columnCount()):
                    line.append(model.data(model.index(row,column)))
                file.write(";".join(line)+'\n')

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    #mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
