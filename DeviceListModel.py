"""DeviceListModel.py: File containing a Model and Item classes of a dedicated Device List.
Model displays devices in a list."""

import taurus.qt.qtcore.model.taurusdatabasemodel
from taurus.core import TaurusElementType
from taurus.qt import Qt
import PyTango
from PyQt4 import QtGui
from CsvManager import CsvManager
from DeviceTreeModel import TaurusTreeDeviceItem
from DeviceTreeModel import TaurusTreeRootItem

__author__ = "Cosylab"


# Model for the tree of devices
#
#------------------------------
class DeviceListModel(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusBaseModel):
    """Model Class for the Device List
    Model structures devices in a 1 level tree."""

    ColorMap = {    PyTango.DevState.ON : QtGui.QColor("green"),
                 PyTango.DevState.OFF : QtGui.QColor("black"),
               PyTango.DevState.CLOSE : QtGui.QColor("white"),
                PyTango.DevState.OPEN : QtGui.QColor("green"),
              PyTango.DevState.INSERT : QtGui.QColor("green"),
             PyTango.DevState.EXTRACT : QtGui.QColor("green"),
              PyTango.DevState.MOVING : QtGui.QColor("blue"),
             PyTango.DevState.STANDBY : QtGui.QColor("yellow"),
               PyTango.DevState.FAULT : QtGui.QColor("red"),
                PyTango.DevState.INIT : QtGui.QColor("yellow"),
             PyTango.DevState.RUNNING : QtGui.QColor("blue"),
               PyTango.DevState.ALARM : QtGui.QColor("orange"),
             PyTango.DevState.DISABLE : QtGui.QColor("magenta"),
             PyTango.DevState.UNKNOWN : QtGui.QColor("black")}


    csvManager = None
    filter = None
    main_ui = None


    # The columns in the tree view
    #-----------------------------
    ColumnNames = ["Device", "Description"]
    ColumnRoles = [(TaurusElementType.Device, TaurusElementType.Member, TaurusElementType.Member), 11]

    def __init__(self, mainWindowUi):
        super(DeviceListModel,self).__init__()
        self.main_ui = mainWindowUi
        for color in self.ColorMap.values():
            color.setAlpha(150)

    def setupModelData(self, data):
        """Sets up the model data
        :param data: Data (must be of type CvsManager)"""

        if data is None:
            return False
        elif isinstance(data, CsvManager):
            self.csvManager = data
        else:
            return False


        self._rootItem = TaurusTreeRootItem(self)
        rootItem = self._rootItem
        for csvDevice in sorted(self.csvManager.getCsvDevices(), key=lambda x: x.order_index):
            memberItem = TaurusTreeDeviceItem(self, csvDevice, self.main_ui, parent=rootItem)
            rootItem.appendChild(memberItem)


    def roleIcon(self, taurus_role):
        if taurus_role == 11:
            return None
        return taurus.qt.qtgui.resource.getElementTypeIcon(taurus_role)

    def roleSize(self, taurus_role):
        return taurus.qt.qtgui.resource.getElementTypeSize(taurus_role)

    def roleToolTip(self, taurus_role):
        return None

    def pyData(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()
        row, column, depth = index.row(), index.column(), item.depth()
        taurus_role = self.role(column, depth)

        ret = None
        if role == Qt.Qt.DisplayRole:
            ret = item.data(index)
        elif role == Qt.Qt.DecorationRole:
            if column == 0:
                ret = self.roleIcon(taurus_role)
        elif role == Qt.Qt.ToolTipRole:
            ret = item.toolTip(index)
        elif role == Qt.Qt.FontRole:
            ret = self.DftFont
        return ret



    def filterTree(self, tree_filter, view):
        """Method filters the tree, according to the provided filter.
        :param tree_filter: dict that maps 'section', 'subsystem' and 'class' to their filter values"""
        self.filter = tree_filter

        row = 0
        for deviceItem in self._rootItem._childItems:
            if deviceItem.dev_info.class_name.find(tree_filter['class']) is -1:
                view.setRowHidden(row, self.index(-1,0), True)
            elif deviceItem.dev_info.subsystem_name.find(tree_filter['subsystem']) is -1:
                view.setRowHidden(row, self.index(-1,0), True)
            elif deviceItem.dev_info.section_name.find(tree_filter['section']) is -1:
                view.setRowHidden(row, self.index(-1,0), True)
            else:
                view.setRowHidden(row, self.index(-1,0), False)
            row += 1

    def itemFromIndex(self, index):
        """Method return a model item that corresponds to the provided index.
        :param index: Index"""
        return self._rootItem.child(index.row())
