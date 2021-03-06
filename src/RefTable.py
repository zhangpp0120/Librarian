import sys
import os
import string
from random import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
import sqlite3
from sqlite3 import Error

class RefTable(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.mainTable = QTableWidget(100, 8, self)  # create 100x8 table  rowNum, colNum
        self.mainTable.setHorizontalHeaderLabels(('Year', 'Title', 'Published In', 'Authors', 'Type', 'Added', 'Labels', 'RefID'))
        '''
        header = self.mainTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Year
        header.setSectionResizeMode(1, QHeaderView.Fixed) # Title
        header.setSectionResizeMode(2, QHeaderView.Stretch) # Published In
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Authors
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Type
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Added Date
        header.setSectionResizeMode(6, QHeaderView.Stretch) # Labels
        '''
        self.mainTable.setColumnWidth(0,  60) # Year
        self.mainTable.setColumnWidth(1, 240) # Title
        self.mainTable.setColumnWidth(2, 240) # Published In
        self.mainTable.setColumnWidth(3, 240) # Authors
        self.mainTable.setColumnWidth(4, 120) # Type
        self.mainTable.setColumnWidth(5, 120) # Added Date
        self.mainTable.setColumnWidth(6, 240) # Labels
        self.mainTable.setColumnWidth(7, 120) # RefAbsID
        # Load refs from database
        database = "Data.db"
        refs = []
        try:
            self.conn = self.createConnectionToDB(database)
            refs = self.getRefsData()
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Initialize Reference Table: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)
        self.setRefsTable(refs)
        #self.reftable_widget.setGeometry(self.width/5, 0, self.width*7/15, self.height)
        #self.mainTable.itemClicked.connect(self.parent().reftableClicked)
        self.mainTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.mainTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.mainTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Connect sorting signal
        self.mainTable.setSortingEnabled(True)
        self.mainTable.horizontalHeader().sortIndicatorChanged.connect(self.sortingTable)

        # Add tabs to widget
        self.layout.addWidget(self.mainTable)
        self.setLayout(self.layout)
        self.appearance = True

    def sortingTable(self, colIndex, order):
        #print("Column:" + str(colIndex))
        if order == Qt.AscendingOrder:
            pass
            #print("Ascending")
        elif order == Qt.DescendingOrder:
            pass
            #print("Descending")

    def createConnectionToDB(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None

    def getRefsData(self):
        refRows = self.readRefsFromDB(self.conn)
        return refRows

    def readRefsFromDB(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM ReferencesData")
        rows = cur.fetchall()
        return rows

    def setRefsTable(self, refs):
        for rowInd in range(len(refs)):
            self.mainTable.setItem(rowInd, 0, QTableWidgetItem(str(refs[rowInd][5]))) # Year
            self.mainTable.setItem(rowInd, 1, QTableWidgetItem(refs[rowInd][1])) # Title
            self.mainTable.setItem(rowInd, 2, QTableWidgetItem(refs[rowInd][4])) # PubIn
            self.mainTable.setItem(rowInd, 3, QTableWidgetItem(refs[rowInd][2])) # Authors
            self.mainTable.setItem(rowInd, 4, QTableWidgetItem(refs[rowInd][3])) # Type
            self.mainTable.setItem(rowInd, 5, QTableWidgetItem(str(refs[rowInd][5]))) # Add Date, change to real field later
            self.mainTable.setItem(rowInd, 6, QTableWidgetItem(refs[rowInd][6])) # Labels
            self.mainTable.setItem(rowInd, 7, QTableWidgetItem(str(refs[rowInd][0]).zfill(10))) # RefAbsID

    def updateRefsTable(self):
        refs = []
        try:
            refs = self.getRefsData()
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Update Reference Table: Database is missing.", QMessageBox.Ok, QMessageBox.Ok)
        self.setRefsTable(refs)

    def onUpdateRequest(self):
        self.updateRefsTable()
