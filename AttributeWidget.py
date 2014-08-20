"""AttributeWidget.py: File containing a Controller Class dedicated to the AttributeWidget.
AttributeWidget is a dynamically generated View, extending QDialog, for displaying specified
Tango devices and their specified attributes."""

from PyQt4 import QtCore, QtGui, Qt
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
import PyTango
import taurus.qt.qtgui.extra_guiqwt as Extra

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

class Ui_Dialog(object):
    """Ui Controller Class for AttributeWidget"""
    panels = None

    def setupUi(self, Dialog, csvDevices, attributeNames):
        """Sets up the AttributeWidget Dialog
        :param Dialog: AttributeWidget Dialog
        :param csvDevices: list of CsvDevice instances, used in this view
        :param attributeNames: list of attribute names, used in this view"""

        self.dialog = Dialog
        self.panels = []
        self.devNames = []
        for csvDevice in csvDevices:
            self.devNames.append(csvDevice.getDeviceName())
        self.attNames = attributeNames

        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 500)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 530, 397))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.formLayout = QtGui.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))

        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        boldFont.setWeight(75)

        counter = 0
        for csvDevice in csvDevices:
            gridLayout = QtGui.QGridLayout()

            attCounter = 1
            for attributeName in attributeNames:
                attributeInfo = csvDevice.getAttributeInfo(attributeName)
                if attributeInfo:
                    attributeNameLabel = QtGui.QLabel(Dialog)
                    attributeNameLabel.setText(_translate("Dialog", attributeName + ":", None))
                    gridLayout.addWidget(attributeNameLabel, attCounter, 0, 1, 1)

                    if attributeInfo.data_format == PyTango.AttrDataFormat.SCALAR:
                        attributeValue = TaurusLabel(Dialog)
                        attributeValue.setModel(csvDevice.getDeviceName() + "/" + attributeName)
                    elif attributeInfo.data_format == PyTango.AttrDataFormat.SPECTRUM:
                        widget = Extra.TaurusCurveDialog()
                        widget.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
                        widget.setModel(csvDevice.getDeviceName() + "/" + attributeName)
                        widget.setWindowTitle(csvDevice.getDeviceName() + "/" + attributeName)
                        attributeValue = ShowPanelButton(QtGui.QIcon(':/designer/qwtplot.png'), "Show")
                        attributeValue.setWidget(widget)
                    else:
                        widget = Extra.TaurusImageDialog()
                        widget.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
                        widget.setModel(csvDevice.getDeviceName() + "/" + attributeName)
                        widget.setWindowTitle(csvDevice.getDeviceName() + "/" + attributeName)
                        attributeValue = ShowPanelButton(QtGui.QIcon(':/mimetypes/image-x-generic.svg'), "Show")
                        attributeValue.setWidget(widget)




                    gridLayout.addWidget(attributeValue, attCounter, 1, 1, 1)
                    attCounter += 1

            if attCounter > 1:
                deviceNameLabel = QtGui.QLabel(Dialog)
                deviceNameLabel.setText(_translate("Dialog", csvDevice.getDeviceName(), None))
                deviceNameLabel.setFont(boldFont)
                gridLayout.addWidget(deviceNameLabel, 0, 0, 1, 1)
                stateLed = TaurusLed(Dialog)
                stateLed.setModel(csvDevice.getDeviceName() + "/state")
                gridLayout.addWidget(stateLed, 0, 1, 1, 1)
                self.formLayout.setLayout(counter, QtGui.QFormLayout.SpanningRole, gridLayout)
                line = QtGui.QFrame(Dialog)
                line.setMinimumSize(QtCore.QSize(0, 10))
                line.setFrameShape(QtGui.QFrame.HLine)
                line.setFrameShadow(QtGui.QFrame.Sunken)
                gridLayout.addWidget(line, attCounter, 0, 1, 2)
                counter += 1

        if counter == 0:
            gridLayout = QtGui.QGridLayout()
            noMatch = QtGui.QLabel(Dialog)
            noMatch.setText(_translate("Dialog", "None of the selected devices have any of the specified attributes!", None))
            gridLayout.addWidget(noMatch, 0, 0, 1, 1)
            self.formLayout.setLayout(counter, QtGui.QFormLayout.SpanningRole, gridLayout)
            Dialog.resize(500,300)


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Custom Panel", None))

    def result(self):
        """Forwards the result of the dialog.
        Used to check if the dialog is opened/closed"""
        return self.dialog.result()


class ShowPanelButton(QtGui.QPushButton):
    widget = None

    def setWidget(self, widget):
        self.widget = widget
        self.clicked.connect(self.showWidget)

    def showWidget(self):
        if self.widget:
            self.widget.show()
            self.widget.raise_()

