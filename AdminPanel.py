__author__ = 'root'

from PyQt4 import Qt, QtCore, QtGui
import os




class Ui_AdminPanel(object):
    """Ui Controller Class for the AdminPanel"""

    opened = False

    def setupUi(self, AdminPanel, MainPanel):
        self.adminPanel = AdminPanel
        self.MainPanel = MainPanel

        self.adminPanel.setWindowFlags(self.adminPanel.windowFlags() | QtCore.Qt.FramelessWindowHint )
        self.adminPanel.setObjectName("adminPanel")
        self.adminPanel.setFixedWidth(0)
        self.adminPanelLayout = QtGui.QVBoxLayout(self.adminPanel)

        #self.testButton = QtGui.QPushButton(self.adminPanel)
        #self.adminPanelLayout.addWidget(self.testButton)

        self.adminPanel.setStyleSheet("#adminPanel{"
                                      "border: 1px solid black; "
                                      "border-radius: 3px;"
                                      "}")

        self.title = QtGui.QLabel()
        self.title.setText("In development ...")
        self.title.setFixedHeight(20)
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.adminPanelLayout.addWidget(self.title)

        self.renderArea = QtGui.QWidget()
        self.renderArea.setFixedSize(QtCore.QSize(300,365))
        self.renderArea.setObjectName("renderArea")
        self.adminPanelLayout.addWidget(self.renderArea)

        self.renderArea.setStyleSheet("#renderArea{"
                                      "background-image: url(" + os.path.dirname(os.path.abspath(__file__)) + "/OverviewAll.png)"
                                      "}")

    def moveShow(self):
        self.adminPanel.setFixedWidth(324)
        self.opened = True

        #self.animation = Qt.QPropertyAnimation(self.adminPanel, "pos")
        #self.animation.setDuration(500)
        #self.animation.setStartValue(self.adminPanel.pos())
        #self.animation.setEndValue(self.getRightPosition())
        #self.animation.start()


    def moveHide(self):
        #self.animation = Qt.QPropertyAnimation(self.adminPanel, "pos")
        #self.animation.setDuration(500)
        #self.animation.setStartValue(self.adminPanel.pos())
        #self.animation.setEndValue(self.getLeftPosition())
        #self.animation.finished.connect(self.hideFinished)
        #self.animation.start()

        self.adminPanel.setFixedWidth(0)
        self.opened = False

    def isOpened(self):
        return self.opened

    def hideFinished(self):
        self.adminPanel.setFixedWidth(0)


    def getLeftPosition(self):
        return Qt.QPoint(self.MainPanel.pos().x() + self.MainPanel.size().width() -300,
                self.MainPanel.pos().y() + (self.MainPanel.height())/2 - self.adminPanel.height()/2 + 5)

    def getRightPosition(self):
        return Qt.QPoint(self.MainPanel.pos().x() + self.MainPanel.size().width() +5,
                self.MainPanel.pos().y() + (self.MainPanel.height())/2 - self.adminPanel.height()/2 + 5)


    def updatePosition(self):
        self.adminPanel.setFixedHeight(self.MainPanel.height() - 90)

        self.adminPanel.move(self.getRightPosition())
        #if self.isOpened():
        #    self.adminPanel.move(self.getRightPosition())
        #else:
        #    self.adminPanel.move(self.getLeftPosition())


