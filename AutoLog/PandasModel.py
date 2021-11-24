import sys
from operator import attrgetter

import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QApplication, QTableView


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):

        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            # if role == Qt.BackgroundRole:
            #     return QBrush(Qt.yellow)
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

        return None

    def sort(self, col, order):
        colname = self._data.columns.tolist()[col]
        self.layoutAboutToBeChanged.emit()
        # self._data.sort_values(colname, ascending=QtCore.Qt.AscendingOrder, inplace=True)
        self._data.sort_values(colname, ascending=order ==
                               QtCore.Qt.AscendingOrder, inplace=True)
        self._data.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def setHorizontalHeaderLabels():
        print('toto')
