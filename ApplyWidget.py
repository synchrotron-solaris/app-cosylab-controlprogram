"""ApplyWidget.py: File containing a Controller Class dedicated to the ApplyWidget.
ApplyWidget is an extended QWidget, presenting options for opening and generating various GUI elements to the user."""

from PyQt4 import QtCore, QtGui
import AttChooserWidget

__author__ = "Cosylab"


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

class Ui_Form(object):
    """Ui Controller Class for ApplyWidget"""

    mainWindowUi = None
    csvManager = None
    attChooser = None

    def setupUi(self, Form, csvManager, mainWindowUi):
        """Sets up the ApplyWidget Form.
        :param Form: ApplyWidget Form
        :param csvManager: instance of CsvManager used throughout the application
        :param mainWindowUi: Ui Controller of the Main Window"""

        self.mainWindowUi = mainWindowUi
        self.csvManager = csvManager

        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(375, 85)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setMargin(9)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.standardGuiButton = QtGui.QPushButton(self.groupBox)
        self.standardGuiButton.setObjectName(_fromUtf8("standardGuiButton"))
        self.horizontalLayout.addWidget(self.standardGuiButton)
        self.customGuiButton = QtGui.QPushButton(self.groupBox)
        self.customGuiButton.setObjectName(_fromUtf8("customGuiButton"))
        self.horizontalLayout.addWidget(self.customGuiButton)
        self.verticalLayout.addWidget(self.groupBox)

        # Additional
        self.standardGuiButton.clicked.connect(self.openGuis)
        self.customGuiButton.clicked.connect(self.openAttributeChooser)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Device Controlling", None))
        self.standardGuiButton.setText(_translate("Form", "Open Standard Device Panel", None))
        self.customGuiButton.setText(_translate("Form", "Open Custom Panel", None))


    def openGuis(self):
        """Forwards the request to open GUIs of the selected elements to the MainWindow controller."""
        self.mainWindowUi.openGui()

    def setFunctionality(self, index):
        """Disables or enables the elements of the widget according to the index.
        Index must reflect the index of the currently opened tree.
        :param index: Index (0 = DeviceTreeTab, 1= DeviceListTab, 2 = AggregateTreeTab)"""
        if index == 2:
            self.customGuiButton.setEnabled(False)
            self.standardGuiButton.setText(_translate("Form", "Open Device Group Panel", None))
            self.groupBox.setTitle(_translate("Form", "Device Group Controlling", None))
        else:
            self.customGuiButton.setEnabled(True)
            self.standardGuiButton.setText(_translate("Form", "Open Standard Device Panel", None))
            self.groupBox.setTitle(_translate("Form", "Device Controlling", None))

    def openAttributeChooser(self):
        """Opens an AttributeChooser dialog for selected devices. AttributeChooser dialog is a required popup window
        for attribute selection, before generating an AttributeWidget. If AttributeChooser is successfully closed,
        a AttributeWidget for selected devices and selected attributes will generated and opened."""
        selectedDevices = self.mainWindowUi.getSelectedDevices()
        if len(selectedDevices) == 0:
            QtGui.QMessageBox.question(None, 'Info', "No devices selected!", QtGui.QMessageBox.Ok)
            return

        self.attChooser = QtGui.QDialog()
        self.attChooser.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        ui = AttChooserWidget.Ui_Form()
        ui.setupUi(self.attChooser, self.mainWindowUi, selectedDevices)
        if self.attChooser.exec_() == 2:
            self.mainWindowUi.openAttView(selectedDevices, ui.selAttList)

