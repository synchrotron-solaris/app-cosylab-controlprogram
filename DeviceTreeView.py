"""DeviceTreeView.py: File containing a View class of a dedicated Device Tree."""

from PyQt4 import QtGui, QtCore
from DeviceTreeModel import TaurusTreeDeviceItem

__author__ = "Cosylab"

class DeviceTreeView(QtGui.QTreeView):
    """View Class for the Device Tree"""

    mainController = None

    def __init__(self, parent, mainController):
        super(DeviceTreeView, self).__init__(parent)
        self.mainController = mainController
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self.actionMonitorState = QtGui.QAction(self)
        self.actionMonitorState.setText("Monitor State")
        self.actionMonitorState.triggered.connect(mainController.monitorState)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)


    def drawBranches(self, QPainter, QRect, QModelIndex):
        item = self.model().itemFromIndex(QModelIndex)
        if isinstance(item, TaurusTreeDeviceItem):
            QPainter.fillRect(QRect, item.getColor())
        super(DeviceTreeView, self).drawBranches(QPainter, QRect, QModelIndex)

    def mouseDoubleClickEvent(self, event):
        super(DeviceTreeView, self).mouseDoubleClickEvent(event)
        if not len(self.selectedIndexes()) == 0:
            self.mainController.openGui()

    def showContextMenu(self, pos):
        pos = self.mapToGlobal(pos)
        menu = QtGui.QMenu(None)
        menu.addAction(self.actionMonitorState)
        menu.exec_(pos)

