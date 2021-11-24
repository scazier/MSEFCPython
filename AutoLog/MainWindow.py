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
        
        #Create a Pandas DF bases on logAnalisys output
        df = pd.DataFrame(logAnalysis(fname[0]).parseLog())
        
        #Set the columns Names
        df.set_axis(logAnalysis(fname[0]).getHeader(),  axis=1, inplace=True)

        # Create a specific model for the table (MVC)
        model = pandasModel(df)
        
        # Apply the model to the QTableView        
        self.table.setModel(model)
        
        # self.table.setSortingEnabled(True)
        self.table.show()


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
