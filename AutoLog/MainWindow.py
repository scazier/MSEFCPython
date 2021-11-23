import sys
from datetime import time
from pathlib import Path

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
                             QTableView, QTableWidget, QTextEdit)

from main import logAnalysis
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
        self.show()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/var/log')

        
        df = pd.DataFrame(logAnalysis(fname[0]).parseLog())
        print(df)
        # self.textEdit.setText(df.to_string())
        model = pandasModel(df)
        view = QTableView()
        self.table.setModel(model)
        self.table.resize(800, 600)
        self.table.show()
        
        

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
