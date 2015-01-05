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
        csvDeviceMap = {}
        for csvDevice in csvDevices:
            if not csvDeviceMap.has_key(csvDevice.getClassName()):
                csvDeviceMap[csvDevice.getClassName()] = [csvDevice]
            else:
                csvDeviceMap[csvDevice.getClassName()].append(csvDevice)



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

        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        boldFont.setWeight(75)


        self.devicesLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)


        for className in csvDeviceMap.keys():
            #print className

            classWidget = QtGui.QWidget()
            classLayout = QtGui.QVBoxLayout(classWidget)
            classHeader = ShowHideButton(classWidget, className)
            classHeader.setStyleSheet("font-weight: bold;")



            devCounter = 0
            for csvDevice in csvDeviceMap[className]:

                deviceHeader = QtGui.QHBoxLayout()
                attributeLayout = QtGui.QGridLayout()



                attCounter = 0
                for attributeName in attributeNames:
                    attributeInfo = csvDevice.getAttributeInfo(attributeName)
                    if attributeInfo:
                        attributeNameLabel = QtGui.QLabel(Dialog)
                        attributeNameLabel.setText(_translate("Dialog", attributeName + ":", None))
                        attributeLayout.addWidget(attributeNameLabel, attCounter, 0, 1, 1)

                        if attributeInfo.data_format == PyTango.AttrDataFormat.SCALAR:
                            attributeValue = TaurusLabel(Dialog)
                            attributeValue.setModel(csvDevice.getDeviceName() + "/" + attributeName)
                            attributeLayout.addWidget(attributeValue, attCounter, 1, 1, 1)

                            units = QtGui.QLabel(Dialog)
                            units.setText("N/A")
                            try:
                                units.setText(PyTango.AttributeProxy(csvDevice.getDeviceName() + "/" + attributeName).get_config().unit)
                            except PyTango.DevFailed:
                                pass
                            units.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
                            attributeLayout.addWidget(units, attCounter, 2, 1, 1)

                        elif attributeInfo.data_format == PyTango.AttrDataFormat.SPECTRUM:
                            widget = Extra.TaurusCurveDialog()
                            widget.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
                            widget.setModel(csvDevice.getDeviceName() + "/" + attributeName)
                            widget.setWindowTitle(csvDevice.getDeviceName() + "/" + attributeName)
                            attributeValue = ShowPanelButton(QtGui.QIcon(':/designer/qwtplot.png'), "Show")
                            attributeValue.setWidget(widget)
                            attributeLayout.addWidget(attributeValue, attCounter, 1, 1, 1)
                        else:
                            widget = Extra.TaurusImageDialog()
                            widget.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
                            widget.setModel(csvDevice.getDeviceName() + "/" + attributeName)
                            widget.setWindowTitle(csvDevice.getDeviceName() + "/" + attributeName)
                            attributeValue = ShowPanelButton(QtGui.QIcon(':/mimetypes/image-x-generic.svg'), "Show")
                            attributeValue.setWidget(widget)
                            attributeLayout.addWidget(attributeValue, attCounter, 1, 1, 1)

                        attCounter += 1

                if attCounter > 0:
                    deviceNameLabel = QtGui.QLabel(Dialog)
                    deviceNameLabel.setText(_translate("Dialog", csvDevice.getDeviceName(), None))
                    deviceNameLabel.setFont(boldFont)
                    deviceHeader.addWidget(deviceNameLabel)
                    stateLed = TaurusLed(Dialog)
                    stateLed.setModel(csvDevice.getDeviceName() + "/state")
                    deviceHeader.addWidget(stateLed)

                    line = QtGui.QFrame(Dialog)
                    line.setMinimumSize(QtCore.QSize(0, 10))
                    line.setFrameShape(QtGui.QFrame.HLine)
                    line.setFrameShadow(QtGui.QFrame.Sunken)
                    attributeLayout.addWidget(line, attCounter, 0, 1, 3)

                    classLayout.addLayout(deviceHeader)
                    classLayout.addLayout(attributeLayout)
                    devCounter += 1

            if devCounter > 0:
                self.devicesLayout.addWidget(classHeader)
                self.devicesLayout.addWidget(classWidget)

        self.devicesLayout.addStretch()

        #if counter == 0:
        #    gridLayout = QtGui.QGridLayout()
        #    noMatch = QtGui.QLabel(Dialog)
        #    noMatch.setText(_translate("Dialog", "None of the selected devices have any of the specified attributes!", None))
        #    gridLayout.addWidget(noMatch, 0, 0, 1, 1)
        #    self.formLayout.setLayout(counter, QtGui.QFormLayout.SpanningRole, gridLayout)
        #    Dialog.resize(500,300)


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

    def getGuiPos(self):
        if self.dialog:
            return [self.dialog.pos().x(), self.dialog.pos().y()]
        else:
            return [0,0]


    def setGuiPos(self, x,y):
        if self.dialog:
            self.dialog.move(x,y)




class ShowHideButton(QtGui.QPushButton):

    toHide = None
    tempText = None

    def __init__(self, toHide, text):
        self.toHide = toHide
        self.tempText = text
        super(ShowHideButton, self).__init__()
        self.setText(text)
        self.clicked.connect(self.showHide)


    def showHide(self):
        if self.toHide.isHidden():
            self.toHide.show()
            self.setText(self.tempText)
        else:
            self.toHide.hide()
            self.setText(u'\u25BC' + "  " + self.tempText + "  " + u'\u25BC')



class ShowPanelButton(QtGui.QPushButton):
    widget = None

    def setWidget(self, widget):
        self.widget = widget
        self.clicked.connect(self.showWidget)

    def showWidget(self):
        if self.widget:
            self.widget.show()
            self.widget.raise_()

