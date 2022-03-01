from PyQt5.QtWidgets import QTableView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate,QWidget,QHBoxLayout,QVBoxLayout,QAbstractItemView,QMenu,QLineEdit,QPushButton
from qgis.gui import QgsFieldComboBox


class fieldTextTable(QTableView):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(0,2,self))

        
        self.delegate = fieldBoxDelegate(self)
        self.setItemDelegateForColumn(0,self.delegate)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        #dataChanged
        
    def setBox(self,box):
        self.delegate.setWidget(box)
        field = box.currentField()
        for i in range(0,self.model().rowCount()):
            self.model().setData(self.model().index(i,0),field)


#dict of field:text. Lowest row used when field is duplicated.
    def toDict(self):
        r = {}
        for i in range(0,self.model().rowCount()):
            field = self.model().index(i,0).data()
            text = self.model().index(i,1).data()
            r[field] = text
        return r
    
class fieldBoxDelegate(QStyledItemDelegate):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        #self.widget = None
        self.fields = None
    
    def createEditor(self,parent,option,index):
        if self.widget:
            w = QgsFieldComboBox(parent)
            w.setFields(self.widget.fields())
            w.setField(index.data())
            return w
    
    def setEditorData(self, editor, index):
        editor.setField(index.data()) 
    
    
    def setModelData(self,editor,model,index):
        model.setData(index,editor.currentField ())

    #will make copy of this when making widget
    def setWidget(self,widget):
        self.widget = widget
        #self.fields=widget.fields()
    
    




class fieldTextMapper(QWidget):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.box = QgsFieldComboBox(self)
        self.edit = QLineEdit(self)
        
        self.table = fieldTextTable(self)
        self.table.setBox(self.box)
        
        self.addButton = QPushButton('Add',self)
        self.addButton.clicked.connect(self.add)
        
        self.setLayout(QVBoxLayout(self))
        row = QHBoxLayout(self)
        row.addWidget(self.box)
        row.addWidget(self.edit)

        row.addWidget(self.addButton)

        self.layout().addLayout(row)
        self.layout().addWidget(self.table)
        
        
        self.menu = QMenu(self)
        dropAct = self.menu.addAction('Drop selected rows.')
        dropAct.triggered.connect(self.drop)
        
        self.table.setContextMenuPolicy(Qt.CustomContextMenu);
        self.table.customContextMenuRequested.connect(lambda pt:self.menu.exec_(self.table.mapToGlobal(pt)))
        
        
    def add(self):
        self.table.model().appendRow([makeItem(self.box.currentField()),makeItem(self.edit.text())])
        
    def drop(self):
        rows = sorted([i.row() for i in self.table.selectionModel().selectedRows()],reverse=True)
        for r in rows:
            self.table.model().takeRow(r)
        
    def removeRow(self):
        pass
    
        
    def toDict(self):
        return self.table.toDict()
        
        

def makeItem(data):
    item = QStandardItem()
    item.setData(data,role=Qt.EditRole )
    return item
    
    

from processing.gui.wrappers import WidgetWrapper

class fieldToTextWrapper(WidgetWrapper):
    """
    """

    def createWidget(self):
        self.box = fieldTextMapper()
        return self.box

    def value(self):
        return self.box.toDict()


from qgis.core import QgsProcessingParameterField



class fieldsToTextParameter(QgsProcessingParameterField):
    pass



def testTable():
    m = fieldTable()
    
    box1 = QgsFieldComboBox(m)
    box1.setLayer(layer1)
    
    box2 = QgsFieldComboBox(m)
    box2.setLayer(layer2)
    m.setBoxes(box1,box2)
    
    m.show()


def testFieldTextMapper():
    m = fieldTextMapper()
    m.box.setLayer(layer1)

    m.show()
    return m
    
    
if __name__=='__console__':
    layer1 = QgsProject.instance().mapLayersByName('split')[0]
    layer2 = QgsProject.instance().mapLayersByName('data')[0]
    m = testFieldTextMapper()

    
