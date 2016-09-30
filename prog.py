#!/usr/bin/env python
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
import math
import calc
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    def compute_initial_figure(self):
        x, y = calc.calc(400)
        self.axes.plot(x, y, 'ro')
    def update_compute(self, n=400):
        x, y = calc.calc(n)
        self.axes.plot(x, y, 'ro')
        self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        self.sc = MyStaticMplCanvas(self.main_widget, width=10, height=8, dpi=100)
        l.addWidget(self.sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Please put in grid frequency", 5000)

        self.button = QtWidgets.QPushButton('Calculate!', self)
        self.input = QtWidgets.QLineEdit(self)
        self.button.clicked.connect(self.handleButton)
        l.addWidget(self.input)
        l.addWidget(self.button)

    def handleButton(self):
        number = self.input.text()
        try:
            number = int(number)
            x,y = calc.calc(number)
            self.sc.update_compute(number)
        except Exception:
            print(Exception)
            QtWidgets.QMessageBox.about(self, 'Error', 'Input can only be a number')
            pass

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """Dobrovolsky & Krivosheyeva
Summer Practice Project
IMEM ONU 2016

This program calculates approximation of DE.
Check out source code and description at
https://github.com/KrivosheyevaMarina/SummerPractic"""
                                )


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % "PracticeProject")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
