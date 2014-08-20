"""DeviceListView.py: File containing a View class of a dedicated Device List."""

from PyQt4 import QtGui
from DeviceTreeModel import TaurusTreeDeviceItem

__author__ = "Cosylab"

class DeviceListView(QtGui.QTreeView):
    """View Class for the Device List"""

    mainController = None

    def __init__(self, parent, mainController):
        super(DeviceListView, self).__init__(parent)
        self.mainController = mainController
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


    def drawBranches(self, QPainter, QRect, QModelIndex):
        item = self.model().itemFromIndex(QModelIndex)
        if isinstance(item, TaurusTreeDeviceItem):
            QPainter.fillRect(QRect, item.getColor())
        super(DeviceListView, self).drawBranches(QPainter, QRect, QModelIndex)

    def mouseDoubleClickEvent(self, event):
        super(DeviceListView, self).mouseDoubleClickEvent(event)
        if not len(self.selectedIndexes()) == 0:
            self.mainController.openGui()

