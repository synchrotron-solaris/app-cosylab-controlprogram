"""ColorWidget.py: File containing a Controller Class dedicated to the ColorWidget.
ColorWidget a an extended QWidget, intended to simply display a color legend for device states.
"""

from PyQt4 import QtCore, QtGui

__author__ = "Cosylab"

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(574, 58)
        self.gridLayout = QtGui.QGridLayout(Form)
        #self.gridLayout.setMargin(0)
        self.gridLayout.setContentsMargins(2, 0, 2, 0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")

        self.ON = QtGui.QLabel(Form)
        self.ON.setAlignment(QtCore.Qt.AlignCenter)
        self.ON.setObjectName("ON")
        self.gridLayout.addWidget(self.ON, 0, 0, 1, 1)

        self.OPEN = QtGui.QLabel(Form)
        self.OPEN.setAlignment(QtCore.Qt.AlignCenter)
        self.OPEN.setObjectName("OPEN")
        self.gridLayout.addWidget(self.OPEN, 0, 1, 1, 1)

        self.INSERT = QtGui.QLabel(Form)
        self.INSERT.setAlignment(QtCore.Qt.AlignCenter)
        self.INSERT.setObjectName("INSERT")
        self.gridLayout.addWidget(self.INSERT, 0, 2, 1, 1)

        self.INIT = QtGui.QLabel(Form)
        self.INIT.setAlignment(QtCore.Qt.AlignCenter)
        self.INIT.setObjectName("INIT")
        self.gridLayout.addWidget(self.INIT, 0, 3, 1, 1)

        self.MOVING = QtGui.QLabel(Form)
        self.MOVING.setAlignment(QtCore.Qt.AlignCenter)
        self.MOVING.setObjectName("MOVING")
        self.gridLayout.addWidget(self.MOVING, 0, 4, 1, 1)

        self.ALARM = QtGui.QLabel(Form)
        self.ALARM.setAlignment(QtCore.Qt.AlignCenter)
        self.ALARM.setObjectName("ALARM")
        self.gridLayout.addWidget(self.ALARM, 0, 5, 1, 1)

        self.DISABLE = QtGui.QLabel(Form)
        self.DISABLE.setAlignment(QtCore.Qt.AlignCenter)
        self.DISABLE.setObjectName("DISABLE")
        self.gridLayout.addWidget(self.DISABLE, 0, 6, 1, 1)

        self.OFF = QtGui.QLabel(Form)
        self.OFF.setAlignment(QtCore.Qt.AlignCenter)
        self.OFF.setObjectName("OFF")
        self.gridLayout.addWidget(self.OFF, 1, 0, 1, 1)

        self.CLOSE = QtGui.QLabel(Form)
        self.CLOSE.setAlignment(QtCore.Qt.AlignCenter)
        self.CLOSE.setObjectName("CLOSE")
        self.gridLayout.addWidget(self.CLOSE, 1, 1, 1, 1)

        self.EXTRACT = QtGui.QLabel(Form)
        self.EXTRACT.setAlignment(QtCore.Qt.AlignCenter)
        self.EXTRACT.setObjectName("EXTRACT")
        self.gridLayout.addWidget(self.EXTRACT, 1, 2, 1, 1)

        self.STANDBY = QtGui.QLabel(Form)
        self.STANDBY.setAlignment(QtCore.Qt.AlignCenter)
        self.STANDBY.setObjectName("STANDBY")
        self.gridLayout.addWidget(self.STANDBY, 1, 3, 1, 1)

        self.RUNNING = QtGui.QLabel(Form)
        self.RUNNING.setAlignment(QtCore.Qt.AlignCenter)
        self.RUNNING.setObjectName("RUNNING")
        self.gridLayout.addWidget(self.RUNNING, 1, 4, 1, 1)

        self.FAULT = QtGui.QLabel(Form)
        self.FAULT.setAlignment(QtCore.Qt.AlignCenter)
        self.FAULT.setObjectName("FAULT")
        self.gridLayout.addWidget(self.FAULT, 1, 5, 1, 1)

        self.UNKNOWN = QtGui.QLabel(Form)
        self.UNKNOWN.setAlignment(QtCore.Qt.AlignCenter)
        self.UNKNOWN.setObjectName("UNKNOWN")
        self.gridLayout.addWidget(self.UNKNOWN, 1, 6, 1, 1)


        self.ON.setStyleSheet("QLabel { background-color:rgba(0,128,0,150); border : 1px solid black;}")
        self.OFF.setStyleSheet("QLabel { background-color:rgba(0,0,0,150); color : white; border : 1px solid black;}")
        #self.CLOSE.setStyleSheet("QLabel { background-color:rgba(255,255,255,150); border : 1px solid black;}")
        self.CLOSE.setStyleSheet("QLabel { background-color:rgba(255,165,0,150); border : 1px solid black;}")
        self.OPEN.setStyleSheet("QLabel { background-color:rgba(0,128,0,150); border : 1px solid black;}")
        self.INSERT.setStyleSheet("QLabel { background-color:rgba(0,128,0,150); border : 1px solid black;}")
        self.EXTRACT.setStyleSheet("QLabel { background-color:rgba(0,128,0,150); border : 1px solid black;}")
        self.MOVING.setStyleSheet("QLabel { background-color:rgba(0,0,255,150); color : white; border : 1px solid black;}")
        self.STANDBY.setStyleSheet("QLabel { background-color:rgba(255,255,0,150); border : 1px solid black;}")
        self.FAULT.setStyleSheet("QLabel { background-color:rgba(255,0,0,150); border : 1px solid black;}")
        self.INIT.setStyleSheet("QLabel { background-color:rgba(255,255,0,150); border : 1px solid black;}")
        self.RUNNING.setStyleSheet("QLabel { background-color:rgba(0,0,255,150); color : white; border : 1px solid black;}")
        self.ALARM.setStyleSheet("QLabel { background-color:rgba(255,165,0,150); border : 1px solid black;}")
        self.DISABLE.setStyleSheet("QLabel { background-color:rgba(255,0,255,150); border : 1px solid black;}")
        self.UNKNOWN.setStyleSheet("QLabel { background-color:rgba(0,0,0,150); color : white; border : 1px solid black;}")


        font = self.ON.font()
        font.setPointSize(9)
        self.ON.setFont(font)
        self.OFF.setFont(font)
        self.CLOSE.setFont(font)
        self.OPEN.setFont(font)
        self.INSERT.setFont(font)
        self.EXTRACT.setFont(font)
        self.MOVING.setFont(font)
        self.STANDBY.setFont(font)
        self.FAULT.setFont(font)
        self.INIT.setFont(font)
        self.RUNNING.setFont(font)
        self.ALARM.setFont(font)
        self.DISABLE.setFont(font)
        self.UNKNOWN.setFont(font)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.ON.setText(QtGui.QApplication.translate("Form", "ON", None, QtGui.QApplication.UnicodeUTF8))
        self.OFF.setText(QtGui.QApplication.translate("Form", "OFF", None, QtGui.QApplication.UnicodeUTF8))
        self.CLOSE.setText(QtGui.QApplication.translate("Form", "CLOSE", None, QtGui.QApplication.UnicodeUTF8))
        self.OPEN.setText(QtGui.QApplication.translate("Form", "OPEN", None, QtGui.QApplication.UnicodeUTF8))
        self.INSERT.setText(QtGui.QApplication.translate("Form", "INSERT", None, QtGui.QApplication.UnicodeUTF8))
        self.EXTRACT.setText(QtGui.QApplication.translate("Form", "EXTRACT", None, QtGui.QApplication.UnicodeUTF8))
        self.MOVING.setText(QtGui.QApplication.translate("Form", "MOVING", None, QtGui.QApplication.UnicodeUTF8))
        self.STANDBY.setText(QtGui.QApplication.translate("Form", "STANDBY", None, QtGui.QApplication.UnicodeUTF8))
        self.FAULT.setText(QtGui.QApplication.translate("Form", "FAULT", None, QtGui.QApplication.UnicodeUTF8))
        self.INIT.setText(QtGui.QApplication.translate("Form", "INIT", None, QtGui.QApplication.UnicodeUTF8))
        self.RUNNING.setText(QtGui.QApplication.translate("Form", "RUNNING", None, QtGui.QApplication.UnicodeUTF8))
        self.ALARM.setText(QtGui.QApplication.translate("Form", "ALARM", None, QtGui.QApplication.UnicodeUTF8))
        self.DISABLE.setText(QtGui.QApplication.translate("Form", "DISABLE", None, QtGui.QApplication.UnicodeUTF8))
        self.UNKNOWN.setText(QtGui.QApplication.translate("Form", "UNKNOWN", None, QtGui.QApplication.UnicodeUTF8))


