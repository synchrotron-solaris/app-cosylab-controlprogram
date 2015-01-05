"""FilterWidget.py: File containing a Controller Class dedicated to the FilterWidget.
FilterWidget is an extended QWidget, presenting options for filtering a dedicated Device Tree to the user."""

from PyQt4 import QtCore, QtGui, Qt

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
    """Ui Controller Class for FilterWidget"""

    mainWindowUi = None

    def setupUi(self, Form, csvManager, mainWindowUi):
        """Sets up the FilterWidget Form.
        :param Form: FilterWidget Form
        :param csvManager: instance of CsvManager used throughout the application
        :param mainWindowUi: Ui Controller of the Main Window"""

        self.mainWindowUi = mainWindowUi

        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(509, 83)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(5, 0, 5, 5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.loc_filter_cob = QtGui.QComboBox(self.groupBox)
        self.loc_filter_cob.setEditable(True)
        self.loc_filter_cob.setObjectName(_fromUtf8("loc_filter_cob"))
        self.horizontalLayout.addWidget(self.loc_filter_cob)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.sub_filter_cob = QtGui.QComboBox(self.groupBox)
        self.sub_filter_cob.setEditable(True)
        self.sub_filter_cob.setObjectName(_fromUtf8("sub_filter_cob"))
        self.horizontalLayout.addWidget(self.sub_filter_cob)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.class_filter_cob = QtGui.QComboBox(self.groupBox)
        self.class_filter_cob.setEditable(True)
        self.class_filter_cob.setObjectName(_fromUtf8("class_filter_cob"))
        self.horizontalLayout.addWidget(self.class_filter_cob)

        self.remove_filters_b = QtGui.QPushButton(self.groupBox)
        self.remove_filters_b.setIcon(QtGui.QIcon(':/designer/editdelete.png'))
        self.remove_filters_b.setIconSize(Qt.QSize(15,15))
        self.remove_filters_b.setFixedSize(27,27)
        self.remove_filters_b.setStyleSheet("text-align: center;")
        self.horizontalLayout.addWidget(self.remove_filters_b)

        self.verticalLayout.addWidget(self.groupBox)

        # Additional
        self.setSectionOptions(csvManager.getCsvSectionNames())
        self.setSubsystemOptions(csvManager.getCsvSubsystemNames())
        self.setClassOptions(csvManager.getCsvClassNames())

        #self.filter_clear.clicked.connect(self.clearFilters)

        self.loc_filter_cob.editTextChanged.connect(self.filterChanged)
        self.sub_filter_cob.editTextChanged.connect(self.filterChanged)
        self.class_filter_cob.editTextChanged.connect(self.filterChanged)
        self.remove_filters_b.clicked.connect(self.removeFilters)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Device Filtering", None))
        self.label_2.setText(_translate("Form", "Section:", None))
        self.label_3.setText(_translate("Form", "Subsystem:", None))
        self.label_4.setText(_translate("Form", "Class:", None))


    def removeFilters(self):
        self.loc_filter_cob.setCurrentIndex(0)
        self.sub_filter_cob.setCurrentIndex(0)
        self.class_filter_cob.setCurrentIndex(0)
        self.applyFilters()

    def filterChanged(self):
        """Signal handler of a filter-change event."""
        self.applyFilters()

    def setSectionOptions(self, locOptions):
        """Sets provided strings as options of a section filter.
        :param locOptions: list of strings"""
        self.loc_filter_cob.clear()
        self.loc_filter_cob.addItem("")
        self.loc_filter_cob.addItems(sorted(locOptions))

    def setSubsystemOptions(self, subOptions):
        """Sets provided strings as options of a subsystem filter.
        :param subOptions: list of strings"""
        self.sub_filter_cob.clear()
        self.sub_filter_cob.addItem("")
        self.sub_filter_cob.addItems(sorted(subOptions))

    def setClassOptions(self, classOptions):
        """Sets provided strings as options of a class filter.
        :param classOptions: list of strings"""
        self.class_filter_cob.clear()
        self.class_filter_cob.addItem("")
        self.class_filter_cob.addItems(sorted(classOptions))

    def applyFilters(self):
        """Applies selected filters."""
        tree_filter = {"section" : "", "subsystem" : "", "class" : ""}
        tree_filter["section"] = self.loc_filter_cob.currentText()
        tree_filter["subsystem"] = self.sub_filter_cob.currentText()
        tree_filter["class"] = self.class_filter_cob.currentText()
        self.mainWindowUi.deselectAllDevices()
        self.mainWindowUi.filterDeviceTree(tree_filter)

    def clearFilters(self):
        """Clears all the filters and applies the change."""
        self.loc_filter_cob.setCurrentIndex(0)
        self.sub_filter_cob.setCurrentIndex(0)
        self.class_filter_cob.setCurrentIndex(0)
        self.applyFilters()

    def setFunctionality(self, index):
        """Disables or enables the elements of the widget according to the index.
        Index must reflect the index of the currently opened tree.
        :param index: Index (0 = DeviceTreeTab, 1 = DeviceListTab, 2 = AggregateTreeTab)"""
        if index == 2:
            self.loc_filter_cob.setEnabled(False)
            self.sub_filter_cob.setEnabled(False)
            self.class_filter_cob.setEnabled(False)
            self.remove_filters_b.setEnabled(False)
        else:
            self.loc_filter_cob.setEnabled(True)
            self.sub_filter_cob.setEnabled(True)
            self.class_filter_cob.setEnabled(True)
            self.remove_filters_b.setEnabled(True)



