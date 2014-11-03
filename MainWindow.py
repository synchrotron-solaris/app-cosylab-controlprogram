"""MainWindow.py: File containing a Controller Class dedicated to the MainWindow of the FacilityView application.
MainWindow extends QMainWindow. It combines all elements of the applications into one.
The controller also serves as a general functionality basis of the application."""

from PyQt4 import QtCore, QtGui, Qt
from DeviceTreeView import DeviceTreeView
from DeviceListView import DeviceListView
from AggSystemTreeView import AggSystemTreeView
from AdminPanel import Ui_AdminPanel
import FilterWidget
import ColorWidget
import ApplyWidget
import AttributeWidget
import os
import threading

__author__ = "Cosylab"



class MainWindow(QtGui.QMainWindow):

    moveTrigger = QtCore.pyqtSignal()
    closeTrigger = QtCore.pyqtSignal()

    def moveEvent(self, QMoveEvent):
        self.moveTrigger.emit()

    def resizeEvent(self, QResizeEvent):
        self.moveTrigger.emit()

    def closeEvent(self, QCloseEvent):
        self.closeTrigger.emit()





try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    """Ui Controller Class for the MainWindow"""

    csvManager = None
    dialogs = []
    initFinished = None

    def __init__(self):
        initFinished = False

    def setupUi(self, MainWindow, csvManager):
        """Sets up the MainWindow.
        :param MainWindow: Main Window
        :param csvManager: instance of CsvManager used throughout the application"""
        self.MainWindow = MainWindow

        self.csvManager = csvManager
        self.refreshLock = threading.Lock()

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(700, 900)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # Admin Panel
        #
        #----------------------
        self.adminPanel = QtGui.QDialog(self.MainWindow)
        self.adminPanelUi = Ui_AdminPanel()
        self.adminPanelUi.setupUi(self.adminPanel, self.MainWindow)
        self.adminPanel.show()
        self.MainWindow.closeTrigger.connect(self.closeAdminPanel)


        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))


        # Filter Widget
        #
        #----------------------
        self.filterWidget = QtGui.QWidget(self.centralwidget)
        self.filterWidget.setObjectName("filterWidget")
        self.filterWidgetUi = FilterWidget.Ui_Form()
        self.filterWidgetUi.setupUi(self.filterWidget, csvManager, self)
        self.verticalLayout.addWidget(self.filterWidget)

        self.treeBarLayout = QtGui.QHBoxLayout()
        self.treeBarLayout.setObjectName(_fromUtf8("treeBarLayout"))
        self.expandButton = QtGui.QPushButton(self.centralwidget)
        self.expandButton.setObjectName(_fromUtf8("expandButton"))
        self.treeBarLayout.addWidget(self.expandButton)
        self.collapseButton = QtGui.QPushButton(self.centralwidget)
        self.collapseButton.setObjectName(_fromUtf8("collapseButton"))
        self.treeBarLayout.addWidget(self.collapseButton)
        self.selectButton = QtGui.QPushButton(self.centralwidget)
        self.selectButton.setObjectName(_fromUtf8("selectButton"))
        self.treeBarLayout.addWidget(self.selectButton)
        self.verticalLayout.addLayout(self.treeBarLayout)
        self.devicesTabWidget = QtGui.QTabWidget(self.centralwidget)
        self.devicesTabWidget.setObjectName(_fromUtf8("devicesTabWidget"))
        self.devicesTab1 = QtGui.QWidget()
        self.devicesTab1.setObjectName(_fromUtf8("devicesTab1"))
        self.devicesTabWidget.addTab(self.devicesTab1, _fromUtf8(""))
        self.devicesTab2 = QtGui.QWidget()
        self.devicesTab2.setObjectName(_fromUtf8("devicesTab2"))
        self.devicesTabWidget.addTab(self.devicesTab2, _fromUtf8(""))
        self.devicesTab3 = QtGui.QWidget()
        self.devicesTab3.setObjectName(_fromUtf8("devicesTab3"))
        self.devicesTabWidget.addTab(self.devicesTab3, _fromUtf8(""))
        self.verticalLayout.addWidget(self.devicesTabWidget)

        self.devicesTabWidget.currentChanged.connect(self.tabChanged)
        self.devicesTabWidget.setMinimumSize(QtCore.QSize(400, 0))

        # Taurus Tree Widget
        #
        #-----------------------------------
        self.treeTab1Layout = QtGui.QVBoxLayout(self.devicesTab1)
        self.treeTab2Layout = QtGui.QVBoxLayout(self.devicesTab2)
        self.treeTab3Layout = QtGui.QVBoxLayout(self.devicesTab3)
        self.taurusTreeWidget = DeviceTreeView(None, self)
        self.taurusTreeWidget.setObjectName("taurusTreeWidget")
        self.treeTab1Layout.addWidget(self.taurusTreeWidget)
        self.taurusTreeWidget2 = DeviceListView(None, self)
        self.taurusTreeWidget2.setObjectName("taurusTreeWidget2")
        self.treeTab2Layout.addWidget(self.taurusTreeWidget2)
        self.taurusTreeWidget3 = AggSystemTreeView(None, self)
        self.taurusTreeWidget3.setObjectName("taurusTreeWidget3")
        self.treeTab3Layout.addWidget(self.taurusTreeWidget3)

        # Apply Widget
        #
        #-----------------------
        self.applyWidget = QtGui.QWidget(self.centralwidget)
        self.applyWidget.setObjectName("applyWidget")
        self.applyWidgetUi = ApplyWidget.Ui_Form()
        self.applyWidgetUi.setupUi(self.applyWidget, csvManager, self)
        self.verticalLayout.addWidget(self.applyWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 704, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_profile = QtGui.QAction(MainWindow)
        self.actionSave_profile.setObjectName(_fromUtf8("actionSave_profile"))
        self.actionLoad_Profile = QtGui.QAction(MainWindow)
        self.actionLoad_Profile.setObjectName(_fromUtf8("actionLoad_Profile"))
        self.menuFile.addAction(self.actionSave_profile)
        self.menuFile.addAction(self.actionLoad_Profile)
        self.menubar.addAction(self.menuFile.menuAction())


        # ColorWidget
        #
        #----------------------
        self.colorWidget = QtGui.QWidget(self.centralwidget)
        self.colorWidget.setObjectName("colorWidget")
        self.colorWidgetUi = ColorWidget.Ui_Form()
        self.colorWidgetUi.setupUi(self.colorWidget)
        self.verticalLayout.addWidget(self.colorWidget)

        # Additional
        self.expandButton.clicked.connect(self.expandTree)
        self.collapseButton.clicked.connect(self.collapseTree)
        self.selectButton.clicked.connect(self.selectAll)
        self.actionLoad_Profile.triggered.connect(self.loadProfile)
        self.actionSave_profile.triggered.connect(self.saveProfile)
        #self.taurusTreeWidget.header().close()
        #self.taurusTreeWidget2.header().close()
        #self.taurusTreeWidget3.header().close()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        self.adminButton = QtGui.QPushButton(self.MainWindow)
        self.adminButton.setText(">")
        self.adminButton.setFixedWidth(0)
        self.adminButton.setFixedSize(QtCore.QSize(20,200))
        self.adminButton.clicked.connect(self.openCloseAdminPanel)
        self.adminButton.show()


        self.MainWindow.move(0,0)
        self.MainWindow.moveTrigger.connect(self.updateRelatedPosition)
        self.updateRelatedPosition()

        self.initFinished = True



    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.expandButton.setText(_translate("MainWindow", "Expand", None))
        self.collapseButton.setText(_translate("MainWindow", "Collapse", None))
        self.selectButton.setText(_translate("MainWindow", "Select All", None))
        self.devicesTabWidget.setTabText(self.devicesTabWidget.indexOf(self.devicesTab1), _translate("MainWindow", "Device Tree", None))
        self.devicesTabWidget.setTabText(self.devicesTabWidget.indexOf(self.devicesTab2), _translate("MainWindow", "Device List", None))
        self.devicesTabWidget.setTabText(self.devicesTabWidget.indexOf(self.devicesTab3), _translate("MainWindow", "Device Groups", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSave_profile.setText(_translate("MainWindow", "Save Profile", None))
        self.actionLoad_Profile.setText(_translate("MainWindow", "Load Profile", None))


    def closeAdminPanel(self):
        self.adminPanelUi.moveHide()

    def openCloseAdminPanel(self):
        if self.adminPanelUi.isOpened():
            self.adminButton.setText(">")
            self.adminPanelUi.moveHide()
        else:
            self.adminButton.setText("<")
            self.adminPanelUi.moveShow()


    def updateRelatedPosition(self):
        self.adminButton.move(self.MainWindow.size().width() - 20,
            (self.MainWindow.height())/2 - self.adminButton.height()/2)
        self.adminPanelUi.updatePosition()

    def refreshRow(self):
        if self.initFinished:
            if self.taurusTreeWidget.model():
                self.taurusTreeWidget.model().layoutChanged.emit()

    def openGui(self):
        """Method for opening a GUI.
        It opens GUIs for all selected elements in a currently opened tree."""
        if self.devicesTabWidget.currentIndex() == 0 or self.devicesTabWidget.currentIndex() == 1:
            selectedDevices = self.getSelectedDevices()
            if len(selectedDevices) == 0:
                QtGui.QMessageBox.question(None, 'Info', "No devices selected!", QtGui.QMessageBox.Ok)
                return
            if len(selectedDevices) > 3:
                if QtGui.QMessageBox.question(None, 'Warning', "Are you sure you want to open " + str(len(selectedDevices)) + " panels?",
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No) != QtGui.QMessageBox.Yes:
                    return
            for selectedDevice in selectedDevices:
                index = selectedDevice.runGUI()
                if index == 1:
                    self.statusbar.showMessage("Opening GUI for device " + selectedDevice.getDeviceName().upper(), 1000)
                elif index == 2:
                    self.statusbar.showMessage("Opening GUI for device " + selectedDevice.getDeviceName().upper(), 1000)
                elif index == 0:
                    self.statusbar.showMessage("GUI for device " + selectedDevice.getDeviceName().upper() + " already running", 1000)
                elif index == -1:
                    QtGui.QMessageBox.question(None, 'Warning', "Device " + selectedDevice.getDeviceName().upper() + " not accessible!", QtGui.QMessageBox.Ok)
                elif index == -2:
                    QtGui.QMessageBox.question(None, 'Warning', "GUI script for device " + selectedDevice.getDeviceName().upper() + " not found!", QtGui.QMessageBox.Ok)
                elif index == -3:
                    QtGui.QMessageBox.question(None, 'Warning', "Error occurred whilst running GUI script for device " + selectedDevice.getDeviceName().upper(), QtGui.QMessageBox.Ok)
        elif self.devicesTabWidget.currentIndex() == 2:
            selectedAggs = self.getSelectedAggregates()
            if len(selectedAggs) == 0:
                QtGui.QMessageBox.question(None, 'Info', "No device groups selected!", QtGui.QMessageBox.Ok)
                return
            if len(selectedAggs) > 3:
                if QtGui.QMessageBox.question(None, 'Warning', "Are you sure you want to open " + str(len(selectedAggs)) + " panels?",
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No) != QtGui.QMessageBox.Yes:
                    return
            for selectedAgg in selectedAggs:
                index = selectedAgg.runGUI()
                if index == 1:
                    self.statusbar.showMessage("Opening GUI for device group " + selectedAgg.agg_system_name.upper(), 1000)
                elif index == 0:
                    self.statusbar.showMessage("GUI for device group " + selectedAgg.agg_system_name.upper() + " already running", 1000)
                elif index == -1:
                    QtGui.QMessageBox.question(None, 'Warning', "GUI script for device group " + selectedAgg.agg_system_name.upper() + " not found!", QtGui.QMessageBox.Ok)
                elif index == -2:
                    QtGui.QMessageBox.question(None, 'Warning', "Error occurred whilst running GUI script for device group " + selectedAgg.agg_system_name.upper(), QtGui.QMessageBox.Ok)

    def tabChanged(self, index):
        """Signal handler for when a tab is changed.
        Handles all necessary changes needed upon tab switch.
        :param index: Index (0 = DeviceTreeTab, 1 = DeviceListTab, 2 = AggregateTreeTab)"""
        self.applyWidgetUi.setFunctionality(index)
        self.filterWidgetUi.setFunctionality(index)
        if index == 2:
            self.expandButton.setEnabled(False)
            self.collapseButton.setEnabled(False)
        else:
            self.expandButton.setEnabled(True)
            self.collapseButton.setEnabled(True)

    def openAttView(self, devices, att_names):
        """Open a new Attribute View for given devices and attribute names.
        :param devices: list of CsvDevice instances
        :param att_names: list of attribute names"""
        self.statusbar.showMessage("Generating Custom Panel", 1000)
        self.refreshAttViewList()
        dialog = QtGui.QDialog()
        dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        ui = AttributeWidget.Ui_Dialog()
        ui.setupUi(dialog, devices, att_names)
        self.dialogs.append(ui)
        dialog.setResult(2)
        dialog.show()

    def refreshAttViewList(self):
        """Removes dead Attribute Views."""
        self.dialogs[:] = [x for x in self.dialogs if x.result() == 2]


    def closeAllAttViews(self):
        """Closes all Attribute Views."""
        self.dialogs[:] = []

    def loadProfile(self):
        """Loads a profile.
        Method prompts the user to provide a file path."""

        file_path = QtGui.QFileDialog.getOpenFileName(None, 'Load Profile', '/home')
        if not file_path:
            return

        errorsCheck = True
        errorMessage = "Profile loaded with errors:\n"

        if not os.path.isfile(file_path):
            QtGui.QMessageBox.question(None, 'Warning', "Invalid file path!", QtGui.QMessageBox.Ok)
            return False

        with open(file_path, 'r') as f:
            data = f.read().strip().split("\n")

        # When opening profile, close all opened GUIs
        self.closeAllAttViews()
        #self.csvManager.closeAllDeviceGUIs()
        #self.csvManager.closeAllAggregateGUIs()

        lineCounter = 0
        for line in data:
            lineCounter += 1
            if not line:
                continue

            info = line.split(":")
            if len(info) == 1:
                errorMessage += "Syntax error in line " + str(lineCounter) + "\n"
                errorsCheck = False
                continue

            # Device GUI
            if info[0] == "1":
                csvDevice = self.csvManager.getCsvDevice(info[1])
                if csvDevice:
                    csvDevice.runGUI()
                else:
                    errorMessage += "Device: " + info[1] + " does not exist!\n"
                    errorsCheck = False

            # Aggregate GUI
            elif info[0] == "2":
                csvAggSystem = self.csvManager.getCsvAggSystem(info[1])
                if csvAggSystem:
                    csvAggSystem.runGUI()
                else:
                    errorMessage += "Aggregate: " + info[1] + " does not exist!\n"
                    errorsCheck = False

            # Attribute View
            elif info[0] == "3":
                # Check Syntax
                info = info[1].split("*")
                if len(info) == 1:
                    errorMessage += "Syntax error in line " + str(lineCounter) + "\n"
                    errorsCheck = False
                    continue

                # Gathering devices
                device_names = info[0].split("|")
                spec_devices = []
                for index in range(0, len(device_names), 1):
                    csvDevice = self.csvManager.getCsvDevice(device_names[index])
                    if csvDevice:
                        spec_devices.append(csvDevice)
                    else:
                        errorMessage += "Device: " + device_names[index] + " does not exist!\n"
                        errorsCheck = False

                # Gathering attributes
                att_names = info[1].split("|")

                # Open View
                self.openAttView(spec_devices, att_names)

            # Comment
            elif info[0] == "#":
                continue
            # Error
            else:
                errorMessage += "Syntax error in line " + str(lineCounter) + "\n"
                errorsCheck = False

        if errorsCheck:
            #QtGui.QMessageBox.question(None, 'Info', "Profile loaded successfully!", QtGui.QMessageBox.Ok)
            pass
        else:
            QtGui.QMessageBox.question(None, 'Warning', errorMessage, QtGui.QMessageBox.Ok)


    def saveProfile(self):
        """Saves current profile.
        Method prompts the user to provide a file path.
        A profile determines opened GUIs"""
        file_path = QtGui.QFileDialog.getSaveFileName(None, 'Save Profile', '/home')
        if not file_path:
            return

        try:
            with open(file_path, 'w') as f:
                self.refreshAttViewList()

                csvNames = self.csvManager.getDeviceNamesGuiOn()
                aggNames = self.csvManager.getAggSystemNamesGuiOn()
                for csvName in csvNames:
                    f.write("1:" + csvName + "\n")
                for aggName in aggNames:
                    f.write("2:" + aggName + "\n")
                for dialog in self.dialogs:
                    line = "3:"
                    for devName in dialog.devNames:
                        line += devName + "|"
                    line = line.rstrip("|")
                    line += "*"
                    for attName in dialog.attNames:
                        line += attName + "|"
                    line = line.rstrip("|")
                    line += "\n"
                    f.write(line)
            #QtGui.QMessageBox.question(None, 'Info', "Profile saved successfully!", QtGui.QMessageBox.Ok)
        except:
            QtGui.QMessageBox.question(None, 'Warning', "Error occurred whilst saving profile!", QtGui.QMessageBox.Ok)


    def filterDeviceTree(self, tree_filter):
        """Filters the device tree, according to the filter.
        :param tree_filter: dict that maps 'section', 'subsystem' and 'class' to their filter values"""
        self.taurusTreeWidget.model().filterTree(tree_filter, self.taurusTreeWidget)
        self.taurusTreeWidget2.model().filterTree(tree_filter, self.taurusTreeWidget2)
        self.taurusTreeWidget.expandAll()

    def expandTree(self):
        """Expands the device tree."""
        self.taurusTreeWidget.expandAll()

    def collapseTree(self):
        """Collapses the device tree."""
        self.taurusTreeWidget.collapseAll()

    def selectAll(self):
        """Selects all elements in a currently opened tree."""
        if self.devicesTabWidget.currentIndex() == 2:
            self.taurusTreeWidget3.selectAll()
        elif self.devicesTabWidget.currentIndex() == 1:
            self.taurusTreeWidget2.selectAll()
        else:
            self.taurusTreeWidget.selectAll()


    def deselectAllDevices(self):
        """Deselects all elements in the device tree."""
        self.taurusTreeWidget.clearSelection()

    def getSelectedDevices(self):
        """Method for acquiring device instances of selected items in the device tree."""
        selectedDevices = []
        if self.devicesTabWidget.currentIndex() == 0:
            indexes = self.taurusTreeWidget.selectedIndexes()
            for index in indexes:
                selectedDevices.append(self.taurusTreeWidget.model().itemFromIndex(index).getCsvDevice())
        elif self.devicesTabWidget.currentIndex() == 1:
            indexes = self.taurusTreeWidget2.selectedIndexes()
            for index in indexes:
                selectedDevices.append(self.taurusTreeWidget2.model().itemFromIndex(index).getCsvDevice())

        return selectedDevices

    def getSelectedAggregates(self):
        """Method for acquiring aggregate instances of selected items in the aggregate tree."""
        selectedAggs = []
        indexes = self.taurusTreeWidget3.selectedIndexes()
        for index in indexes:
            selectedAggs.append(self.taurusTreeWidget3.model().itemFromIndex(index).getCsvAggSystem())
        return selectedAggs

    def getSelectedDevicesNames(self):
        """Method for acquiring device names of selected items in the device tree."""
        selectedDevicesNames = []
        if self.devicesTabWidget.currentIndex() == 0:
            indexes = self.taurusTreeWidget.selectedIndexes()
            for index in indexes:
                selectedDevicesNames.append(self.taurusTreeWidget.model().itemFromIndex(index).getCsvDevice().getDeviceName())
        elif self.devicesTabWidget.currentIndex() == 1:
            indexes = self.taurusTreeWidget2.selectedIndexes()
            for index in indexes:
                selectedDevicesNames.append(self.taurusTreeWidget2.model().itemFromIndex(index).getCsvDevice().getDeviceName())

        return selectedDevicesNames

