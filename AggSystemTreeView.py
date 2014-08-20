"""AggSystemTreeView.py: File containing a View class of an dedicated Aggregate Tree"""

from PyQt4 import QtGui

__author__ = "Cosylab"


class AggSystemTreeView(QtGui.QTreeView):
    """View Class for the Aggregate Tree"""

    mainController = None

    def __init__(self, parent, mainController):
        super(AggSystemTreeView, self).__init__(parent)
        self.mainController = mainController
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def mouseDoubleClickEvent(self, event):
        super(AggSystemTreeView, self).mouseDoubleClickEvent(event)
        self.mainController.openGui()

