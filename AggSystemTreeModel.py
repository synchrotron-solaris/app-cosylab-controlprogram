"""AggSystemTreeModel.py: File containing a Model and Item classes of an dedicated Aggregate Tree.
Model structures elements in a 2 level tree:
        <Aggregate>
            <Device>"""

import taurus.qt.qtcore.model.taurusdatabasemodel
from taurus.core import TaurusElementType
from CsvManager import CsvManager


__author__ = "Cosylab"


class AggSystemTreeModel(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusDbBaseModel):
    """Model Class for the Aggregate Tree
    Model structures elements in a 2 level tree:
        <Aggregate>
            <Device>"""


    ColumnNames = ["Device Group"]
    ColumnRoles = [(TaurusElementType.Device, TaurusElementType.Member, TaurusElementType.Member)]

    csvManager = None

    def setupModelData(self, data):
        """Sets up the model data
        :param data: Data (must be of type CvsManager)"""
        if data is None:
            return False
        elif isinstance(data, CsvManager):
            self.csvManager = data
        else:
            return False

        rootItem = self._rootItem
        csvAggSystems = self.csvManager.getCsvAggSystems()
        for csvAggSystem in sorted(sorted(csvAggSystems.itervalues(), key=lambda y: y.agg_system_name), key=lambda x: x.order_index):
        #for csvAggSystemKey in sorted(csvAggSystems.keys()):
            #csvAggSystem = csvAggSystems[csvAggSystemKey]
            aggSystemItem = TaurusTreeAggSystemItem(self, csvAggSystem, rootItem)
            rootItem.appendChild(aggSystemItem)


    def itemFromIndex(self, index):
        """Returns Tree Model Item for a given index
        :param index: Index"""
        trace = []
        node = index
        while node.parent().isValid():
            trace.append(node.row())
            node = node.parent()
        trace.append(node.row())
        trace = reversed(trace)

        item = self._rootItem
        for t in trace:
            pass
            item = item._childItems[t]
        return item



class TaurusTreeAggSystemItem(taurus.qt.qtcore.model.taurusdatabasemodel.TaurusBaseTreeItem):
    """Model Item Class of the Aggregate Tree"""

    csvAggSystem = None

    def __init__(self, model, data, parent):
        self.csvAggSystem = data
        super(TaurusTreeAggSystemItem, self).__init__(model, data.agg_system_name, parent)

    def data(self, index):
        return self._itemData

    def getCsvAggSystem(self):
        """Returns Data instance corresponding to this Model Item"""
        return self.csvAggSystem
