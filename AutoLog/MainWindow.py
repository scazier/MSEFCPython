# -*- coding: utf-8 -*-
import base64
import io
import os
import re
import sys
from datetime import time
from pathlib import Path

import exiftool
import folium
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWebEngineWidgets, QtWidgets
from PyQt5.QtCore import (QPoint, QRegExp, QSignalMapper,
                          QSortFilterProxyModel, Qt)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QGridLayout, QHBoxLayout, QHeaderView, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QMainWindow, QMenu, QMessageBox, QProgressBar,
                             QPushButton, QSizePolicy, QTableView,
                             QTableWidget, QTabWidget, QTextEdit, QVBoxLayout,
                             QWidget)

from main import logAnalysis
# from numpyArrayModel import NumpyArrayModel
from PandasModel import pandasModel

ROOT_PATH = "/".join(os.path.abspath(__file__).split('/')[:-2])

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
        self.tab2.HSecondBottomLayout = QGridLayout()

        self.metaTable = QTableView()
        self.linePath = QLineEdit()
        self.linePath.isReadOnly()
        self.linePath.dragEnabled()
        self.linePath.textChanged.connect(self.listFiles)
        self.labelPath = QLabel("Path:")
        self.openButton = QPushButton("", self)
        self.openButton.setText("...")
        self.openButton.setIcon(QIcon("../imgs/folder.png"))
        self.openButton.clicked.connect(self.setMetadataPath)
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.displayMetadata)
        self.labelNumFiles = QLabel()
        self.visualizeButton = QPushButton("Visualize")
        self.visualizeButton.clicked.connect(self.visualizeGPSMetadata)
        self.visualizeButton.setDisabled(True)

        self.tab2.HUpLayout.addWidget(self.labelPath)
        self.tab2.HUpLayout.addWidget(self.linePath)
        self.tab2.HUpLayout.addWidget(self.openButton)
        self.tab2.HBottomLayout.addWidget(self.listWidget)
        self.tab2.HBottomLayout.addWidget(self.metaTable)
        self.tab2.HSecondBottomLayout.addWidget(self.labelNumFiles, 0, 0)
        self.tab2.HSecondBottomLayout.addWidget(self.visualizeButton, 0, 3, alignment=QtCore.Qt.AlignRight)
        self.tab2.HSecondBottomLayout.setColumnStretch(0, 1)
        self.tab2.HSecondBottomLayout.setColumnStretch(1, 3)
        self.tab2.HSecondBottomLayout.setColumnStretch(2, 1)

        self.tab2.layout.addLayout(self.tab2.HUpLayout)
        self.tab2.layout.addLayout(self.tab2.HBottomLayout)
        self.tab2.layout.addLayout(self.tab2.HSecondBottomLayout)
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
        self.browseRegex.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
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
        with open(ROOT_PATH+"/AutoLog/URLRegex.conf") as regexConf:
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
        with open(ROOT_PATH+"/AutoLog/URLRegex.conf") as regexConf:
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
                item = QListWidgetItem(os.path.join(root,i), self.listWidget)
                if self.hasGpsMetadata(os.path.join(root,i)):
                    item.setForeground(Qt.green)
                self.labelNumFiles.setText("%s files" % self.listWidget.count())
                self.labelNumFiles.show() 

    def hasGpsMetadata(self, path):
        self.fileMetadata = {}
        with exiftool.ExifTool() as et:
            return 'EXIF:GPSLatitude' in dict(et.get_metadata(path)) and 'EXIF:GPSLongitude' in dict(et.get_metadata(path))
        



    def displayMetadata(self):
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
            self.metaTable.horizontalHeader().setStretchLastSection(True)
            self.metaTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            if 'EXIF:GPSLatitude' and 'EXIF:GPSLongitude' in self.fileMetadata : self.visualizeButton.setDisabled(False)
            else: self.visualizeButton.setDisabled(True)

    def visualizeGPSMetadata(self):
        listLength = self.listWidget.count()

        if listLength < 1:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setInformativeText("No files to parse")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        map = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)

        self.pbar = QProgressBar()
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(listLength)
        self.pbar.setFormat("Parsing GPS metadata... (0 %)")
        self.tab2.HSecondBottomLayout.addWidget(self.pbar, 0, 1)
        self.pbar.show()

        marker_counter = 0
        for index in range(listLength):
            metadata = {}
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(self.listWidget.item(index).text())
            if "EXIF:GPSLatitude" in metadata.keys():

                # try:
                #     encoded = base64.b64encode(open(metadata["SourceFile"],'rb').read()).decode()
                #     svg = '<img src="data:{};base64,{}" width="200" height="100">'.format(metadta["File:MIMEType"],encoded)
                # except:
                #     encoded = "No preview"

                htmlPopup = """
                    <div>
                        <p>Filename: {}</p>
                        <p>Creation date: {}<p>
                    </div>""".format(metadata["SourceFile"],metadata["EXIF:CreateDate"])
                iframe = folium.IFrame(
                            html=htmlPopup,
                            width=600,
                            height=100
                )

                iconFactor = 0.02
                iconSize = (int(iconFactor*metadata["File:ImageWidth"]), int(iconFactor*metadata["File:ImageHeight"]))
                icon = folium.features.CustomIcon(metadata["SourceFile"], icon_size=iconSize)

                folium.Marker(
                    location=[metadata["EXIF:GPSLatitude"], metadata["EXIF:GPSLongitude"]],
                    popup=folium.Popup(iframe, parse_html=True, max_width=1000),
                    icon=icon
                ).add_to(map)
                marker_counter += 1

            self.pbar.setValue(index+1)
            percentage = round((float(index+1)/(listLength)) * 100, 1)
            self.pbar.setFormat("Parsing GPS metadata... ({} %)".format(percentage))

        if marker_counter == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setInformativeText("No GPS metadata found")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        map.save(os.path.split(os.path.abspath(__file__))[0]+r"/.tmp.html")
        # self.dataMap = io.BytesIO()
        # self.map.save(self.dataMap, close_file=False)
        webView = QWebEngineView()
        # webView.setHtml(self.dataMap.getvalue().decode())
        webView.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r"/.tmp.html"))
        self.webMap = metadataMap(webView)
        self.webMap.show()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/var/log')
        mylog = logAnalysis(fname[0])

        # Create a Pandas DF bases on logAnalisys output
        df = pd.DataFrame(mylog.parseLog())

        # Set the columns Names
        df.set_axis(mylog.getHeader(), axis=1, inplace=True)

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
        print(model)
        if model == None or model.rowCount() == 0:
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

class metadataMap(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.resize(1000,600)
        self.setWindowTitle("Metadata map")
        layout = QVBoxLayout()
        layout.addWidget(widget)
        self.saveMapButton = QPushButton("Save")
        self.saveMapButton.clicked.connect(self.saveMap)
        layout.addWidget(self.saveMapButton, alignment=Qt.AlignLeft)
        self.setLayout(layout)

    def saveMap(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save map", "", "html")
        if filepath == "":
            return

        with open(filepath+".html",'wb') as outputFile:
            outputFile.write(open(os.path.split(os.path.abspath(__file__))[0]+r"/.tmp.html",'rb').read())

        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setInformativeText("Map saved successfully")
        msg.setIcon(QMessageBox.Success)
        msg.exec_()


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    #mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
