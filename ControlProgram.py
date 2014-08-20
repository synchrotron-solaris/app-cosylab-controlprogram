"""ControlProgram.py: File containing script for running the ControlProgram application.
Application takes 3 arguments:
--CSV = Path to CSV file
--GUI = Path to GUI directory
--TITLE = Title of the main window"""

import sys
import MainWindow
import DeviceTreeModel
import DeviceListModel
from PyQt4 import QtGui
from taurus.qt.qtgui.application import TaurusApplication
import taurus
import argparse
from CsvManager import CsvManager
from AggSystemTreeModel import AggSystemTreeModel

__author__ = "Cosylab"

parser = argparse.ArgumentParser()
parser.add_argument('--CSV', help='Path to CSV file', required=True)
parser.add_argument('--GUI', help='Path to GUI directory', required=True)
parser.add_argument('--TITLE', help='Title of the main window', required=False)
args = parser.parse_args()
sys.argv = []


app = TaurusApplication([])
app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))

mainWindow = MainWindow.MainWindow()
ui = MainWindow.Ui_MainWindow()
csvManager = CsvManager(args.CSV, args.GUI, ui)
ui.setupUi(mainWindow,csvManager)
if args.TITLE:
    mainWindow.setWindowTitle(args.TITLE)

taurusDb = taurus.Database()

device_model = DeviceTreeModel.DeviceTreeModel(ui)
device_model.setDataSource(csvManager)
ui.taurusTreeWidget.setModel(device_model)

device_list_model = DeviceListModel.DeviceListModel(ui)
device_list_model.setDataSource(csvManager)
ui.taurusTreeWidget2.setModel(device_list_model)

agg_system_model = AggSystemTreeModel()
agg_system_model.setDataSource(csvManager)
ui.taurusTreeWidget3.setModel(agg_system_model)

ui.taurusTreeWidget.resizeColumnToContents(0)
ui.taurusTreeWidget.setColumnWidth(0, ui.taurusTreeWidget.columnWidth(0) + 100)

ui.taurusTreeWidget2.resizeColumnToContents(0)
ui.taurusTreeWidget2.setColumnWidth(0, ui.taurusTreeWidget2.columnWidth(0) + 100)

mainWindow.show()
ret = app.exec_()

csvManager.destroy()
sys.exit(ret)