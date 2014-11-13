"""AttChooserWidget.py: File containing a Controller Class dedicated to the AttChooserWidget.
AttChooserWidget is an extended QDialog.
Its purpose is to acquire a set of attributes for selected devices from the user."""

from PyQt4 import QtCore, QtGui

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
    mainWindowUi = None

    selectedDevices = None
    allAttList = None
    selAttList = None
    widget = None

    def setupUi(self, Form, mainWindowUi, devices):
        self.mainWindowUi = mainWindowUi
        self.selectedDevices = devices
        self.allAttList = []
        self.selAttList = []
        self.widget = Form

        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(650, 650)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.label_5 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_5)


        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.selectedDevList = QtGui.QTextEdit(Form)
        self.selectedDevList.setObjectName(_fromUtf8("selectedDevList"))
        self.selectedDevList.setReadOnly(True)
        self.verticalLayout.addWidget(self.selectedDevList)

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)


        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.listAll = QtGui.QListWidget(Form)
        self.listAll.setObjectName(_fromUtf8("listAll"))
        self.verticalLayout_3.addWidget(self.listAll)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.addButton = QtGui.QPushButton(Form)
        self.addButton.setMinimumSize(QtCore.QSize(30, 30))
        self.addButton.setMaximumSize(QtCore.QSize(30, 30))
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridLayout.addWidget(self.addButton, 0, 0, 1, 1)
        self.removeButton = QtGui.QPushButton(Form)
        self.removeButton.setMinimumSize(QtCore.QSize(30, 30))
        self.removeButton.setMaximumSize(QtCore.QSize(30, 30))
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.gridLayout.addWidget(self.removeButton, 1, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.listSelected = QtGui.QListWidget(Form)
        self.listSelected.setObjectName(_fromUtf8("listSelected"))
        self.verticalLayout_2.addWidget(self.listSelected)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.okButton = QtGui.QPushButton(Form)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.verticalLayout.addWidget(self.okButton)


        # Additional
        for device in self.selectedDevices:
            self.allAttList = self.allAttList + list(set(device.getAttributesNames()) - set(self.allAttList))
        self.listAll.addItems(self.allAttList)

        for device in self.selectedDevices:
            self.selectedDevList.append(device.getDeviceName())

        self.okButton.clicked.connect(self.completed)
        self.addButton.clicked.connect(self.addAttribute)
        self.removeButton.clicked.connect(self.removeAttribute)

        self.listAll.doubleClicked.connect(self.addAttribute)
        self.listSelected.doubleClicked.connect(self.removeAttribute)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Custom Panel Generator", None))
        self.label_3.setText(_translate("Form", "Select Attributes :", None))
        self.label_5.setText(_translate("Form", "Selected Devices :", None))
        self.label_2.setText(_translate("Form", "Available Attributes:", None))
        self.addButton.setText(_translate("Form", ">", None))
        self.removeButton.setText(_translate("Form", "<", None))
        self.label.setText(_translate("Form", "Selected Attributes:", None))
        self.okButton.setText(_translate("Form", "Open Custom Panel", None))
        self.label_4.setText(_translate("Form", "Selected Devices:", None))



    def completed(self):
        if self.listSelected.count() == 0:
            QtGui.QMessageBox.question(None, 'Info', "No attributes selected!", QtGui.QMessageBox.Ok)
            return
        self.selAttList = []
        for row in range(0, self.listSelected.count(), 1):
            self.selAttList.append(str(self.listSelected.item(row).text()))
        self.widget.done(2)



    def addAttribute(self):
        """Moves selected attribute from the left list to the right one."""
        if self.listAll.currentRow() < 0:
            self.listAll.setCurrentRow(0)
            return
        for selectedAtt in self.listAll.selectedItems():
            self.listSelected.addItem(selectedAtt.text())
            self.listAll.takeItem(self.listAll.row(selectedAtt))

    def removeAttribute(self):
        """Moves selected attribute from the right list to the left one."""
        if self.listSelected.currentRow() < 0:
            self.listSelected.setCurrentRow(0)
            return
        for selectedAtt in self.listSelected.selectedItems():
            self.listAll.addItem(selectedAtt.text())
            self.listSelected.takeItem(self.listSelected.row(selectedAtt))