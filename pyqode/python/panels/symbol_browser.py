"""
SymbolBrowserPanel
"""
import pyqode.core
from pyqode.core import logger
from pyqode.python.modes.code_completion import iconFromType
from pyqode.qt import QtGui


class Definition(object):
    def __init__(self, name, icon, line, column):
        self.icon = icon
        self.name = name
        self.line = line
        self.column = column
        # symbol name with parent name (for function and class variables)
        self.full_name = ""
        self.children = []

    def add_child(self, definition):
        definition.full_name = "%s.%s" % (self.name, definition.name)
        self.children.append(definition)

    def __repr__(self):
        return 'Definition(%r, %r, %r, %r)' % (self.name, self.icon,
                                               self.line, self.column)


class DefinedNamesWorker(object):
    def __init__(self, code, path, encoding):
        self.code = code
        self.path = path
        self.encoding = encoding

    def __call__(self, *args, **kwargs):
        import jedi
        ret_val = []
        toplvl_definitions = jedi.defined_names(self.core, self.path, self.encoding)
        for d in toplvl_definitions:
            icon = ""
            definition = Definition(d.name, iconFromType(d.type),
                                    d.line, d.column)
            if d.type == "class":
                sub_definitions = d.defined_names()
                for sub_d in sub_definitions:
                    sub_definition = Definition(sub_d.name,
                                                iconFromType(sub_d.type),
                                                sub_d.line, sub_d.column)
                    definition.add_child(sub_definition)
            ret_val.append(definition)
        logger.debug(ret_val)
        return ret_val


class SymbolBrowserPanel(pyqode.core.Panel):
    def __init__(self):
        super(SymbolBrowserPanel, self).__init__()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QtGui.QComboBox()
        layout.addWidget(self.comboBox)
        self.setLayout(layout)
        self.comboBox.addItem("<Select a symbol>")

    def _onInstall(self, editor):
        super(SymbolBrowserPanel, self)._onInstall(editor)
        self.comboBox.setFont(self.editor.font())
