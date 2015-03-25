"""DeviceTreeModel.py: File containing a Model and Item classes of a dedicated Device Tree.
Model structures elements in a 3 level tree:
        <Section>
            <Subsystem>
                <Device>"""

import taurus.qt.qtcore.model.taurusdatabasemodel
from taurus.core import TaurusElementType
from taurus.qt import Qt
import PyTango
from PyQt4 import QtGui
from CsvManager import CsvManager

__author__ = "Cosylab"


# Model for the tree of devices
#
#------------------------------
class DeviceTreeModel(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusBaseModel):
    """Model Class for the Device Tree
    Model structures elements in a 3 level tree:
        <Section>
            <Subsystem>
                <Device>"""

    ColorMap = {    PyTango.DevState.ON : QtGui.QColor("green"),
                 PyTango.DevState.OFF : QtGui.QColor("black"),
               PyTango.DevState.CLOSE : QtGui.QColor("orange"),
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
    dev_items = None
    main_ui = None


    # The columns in the tree view
    #-----------------------------
    ColumnNames = ["Device", "Description"]
    ColumnRoles = [(TaurusElementType.Device, TaurusElementType.Domain, TaurusElementType.Family, TaurusElementType.Member), 11]

    def __init__(self, mainWindowUi):
        super(DeviceTreeModel,self).__init__()
        self.dev_items = []
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
        csvSections = self.csvManager.getCsvSections()
        for csvSection in sorted(csvSections.values(), key=lambda x: x.order_index):
            sectionItem = TaurusTreeSectionItem(self, csvSection, rootItem)
            for csvSubsystem in sorted(csvSection.csvSubsystems.values(), key=lambda x: x.order_index):
                subsystemItem = TaurusTreeSubsystemItem(self, csvSubsystem, sectionItem)
                for csvDevice in sorted(csvSubsystem.csvDevices.values(), key=lambda x: x.order_index):
                    memberItem = TaurusTreeDeviceItem(self, csvDevice, self.main_ui, parent=subsystemItem)
                    self.dev_items.append(memberItem)
                    subsystemItem.appendChild(memberItem)
                sectionItem.appendChild(subsystemItem)
            rootItem.appendChild(sectionItem)


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

        row1 = 0
        for sectionItem in self._rootItem._childItems:
            row2 = 0
            allHidden1 = True
            for subsystemItem in sectionItem._childItems:
                row3 = 0
                allHidden2 = True
                for deviceItem in subsystemItem._childItems:
                    if deviceItem.dev_info.class_name.lower() != tree_filter['class'].toLower():
                        view.setRowHidden(row3, self.index(row2,0, self.index(row1,0)), True)
                    else:
                        view.setRowHidden(row3, self.index(row2,0, self.index(row1,0)), False)
                        allHidden2 = False
                    row3 += 1

                if subsystemItem.csvSubsystem.subsystem_name.find(tree_filter['subsystem']) is -1 or allHidden2:
                    view.setRowHidden(row2, self.index(row1,0), True)
                else:
                    view.setRowHidden(row2, self.index(row1,0), False)
                    allHidden1 = False
                row2 += 1

            if sectionItem.csvSection.section_name.find(tree_filter['section']) is -1 or allHidden1:
                view.setRowHidden(row1, self.index(-1,0), True)
            else:
                view.setRowHidden(row1, self.index(-1,0), False)
            row1 += 1

    def itemFromIndex(self, index):
        """Method return a model item that corresponds to the provided index.
        :param index: Index"""
        trace = []
        node = index

        item = self._rootItem
        if not node.parent().isValid():
            return item._childItems[node.row()]
        lastRow = node.row()
        node = node.parent()

        while node.parent().isValid():
            trace.append(node.row())
            node = node.parent()
        trace.append(node.row())
        trace = reversed(trace)

        for t in trace:
            pass
            item = item._childItems[t]
        item = item.child(lastRow)
        return item



class TaurusTreeDeviceItem(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusTreeDeviceItem):
    """Model Item Class of the Device Tree representing Device"""

    device_name = None
    short_device_name = None
    dev_state = None
    dev_info = None
    event_id = None
    main_ui = None
    device_proxy = None
    state_attribute = None
    state_listener = None


    def __init__(self, model, data, mainUi, parent = None):
        taurus.qt.qtcore.model.taurusdatabasemodel.TaurusTreeDeviceItem.__init__(self, model, data, parent)

        self.main_ui = mainUi
        self.device_name = data.getDeviceName()
        self.short_device_name = self.device_name[self.device_name.find("/") + 1:]
        self.dev_info = data
        self.dev_state = PyTango.DevState.UNKNOWN


    def data(self, index):
        column, model = index.column(), index.model()
        role = model.role(column, self.depth())
        obj = self.itemData()
        if role == TaurusElementType.Member:
            return obj.getDeviceName()
        elif role == 11:
            return obj.getDescription()

    def hasChildren(self):
        return False

    def childCount(self):
        return 0

    def getColor(self):
        """Method returns an instance of QColor that corresponds to the current state of this item."""
        state = self.dev_info.getState()
        if state is not None:
            return DeviceTreeModel.ColorMap[state]
        else:
            return QtGui.QColor("transparent")

    def changeState(self, state):
        """Method changes the state of this item.
        It is used under the subscription to the device state.
        :param state: New state"""
        self.dev_state = state
        self._model.layoutChanged.emit()

    def getCsvDevice(self):
        """Getter for the CsvDevice instance of this item."""
        return self.dev_info





class TaurusTreeRootItem(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusTreeDbBaseItem):
    """Root Model Item Class of the Device Tree"""

    def __init__(self, model, data=None, parent=None):
        super(TaurusTreeRootItem, self).__init__(model, data, parent)



class TaurusTreeSectionItem(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusTreeDeviceDomainItem):
    """Model Item Class of the Device Tree representing Section"""

    csvSection = None

    def __init__(self, model, data, parent):
        self.csvSection = data
        super(TaurusTreeSectionItem, self).__init__(model, data.section_name, parent)


class TaurusTreeSubsystemItem(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusTreeDeviceFamilyItem):
    """Model Item Class of the Device Tree representing Subsystem"""

    csvSubsystem = None

    def __init__(self, model, data, parent):
        self.csvSubsystem = data
        super(TaurusTreeSubsystemItem, self).__init__(model, data.subsystem_name, parent)
