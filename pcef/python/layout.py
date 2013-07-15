#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pcef-python
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This module provides classes and function to do a quick analysis of a python
document layout.

It returns a tree of DocumentNode which includes the following informations:
    - imports
    - globals
    - functions
    - classes
    - methods
"""
import weakref


class DocumentLayoutNode(object):
    """
    Represents a node in the document layout.

    A node is defined by an identifier (class or function name), a start and
    end line number, a type (DocumentNodeType) and a list of children.
    """

    class Type:
        """
        Enumerates the possible document nodes types
        """
        #: Root of the document. This is the node returned by the parse method.
        ROOT = 0
        #: Function/method node
        FUNCTION = 1
        #: Class node
        CLASS = 2
        #: Imports (all imports are stored in this zone)
        IMPORTS = 3
        #: Global variable
        GLOBAL_VAR = 4

        @classmethod
        def toString(cls, t):
            if t == cls.ROOT:
                return "ROOT"
            elif t == cls.FUNCTION:
                return "FUNCTION"
            elif t == cls.CLASS:
                return "CLASS"
            elif t == cls.IMPORTS:
                return "IMPORTS"
            elif t == cls.GLOBAL_VAR:
                return "GLOBAL_VAR"
            else:
                return "UNKNWON TYPE"

    def __init__(self, identifier, nodeType=0):
        """
        :param identifier: The node identifier.

        :param nodeType: The node type
        """
        #: Identifier (used for class names, function names, and global
        #: variable names
        self.identifier = identifier
        #: Start line
        self.start = None
        #: End line
        self.end = None
        #: Type: class, function , global, imports, root
        self.type = nodeType
        #: The node indentation level (number of spaces)
        self.indentationLevel = 0
        #: The list of child nodes
        self.children = []
        #: Weakref to the parent node
        self.__parent = None

    @property
    def parent(self):
        """
        Returns the reference to the parent node
        """
        return self.__parent()

    def addChild(self, child):
        """
        Adds a child node
        """
        child.__parent = weakref.ref(self)
        self.children.append(child)

    def finalize(self, lines):
        """
        Closes nodes
        """
        starts = []
        for c in self.children:
            starts.append(c.start)
        starts.append(self.end)
        for i in range(len(starts) - 1):
            self.children[i].end = starts[i + 1] - 1
        for c in self.children:
            c.finalize(lines)
        ch = []
        for c in self.children:
            finish = False
            while not finish:
                l = lines[c.end - 1].strip()
                if c.identifier == "on_actionOpen_triggered":
                    pass
                empty_line = l.isspace() or l == "" or "@" in l
                if c.end <= 0 or not empty_line:
                    finish = True
                else:
                    c.end -= 1
            ch.append(c)
        self.children[:] = ch


    def debugPrint(self, indent=0):
        """
        Prints the node tree hierarchy.
        """
        print(" " * indent, self.identifier, self.start, self.end,
            self.indentationLevel, DocumentLayoutNode.Type.toString(self.type))
        for c in self.children:
            c.debugPrint(indent + 4)


def getLineIndentationLevel(line):
    """
    Returns the indentation level of a line

    :param line: Line to analyse

    :return: Nbr of indentation spaces.
    """
    return len(line) - len(line.lstrip())


def analyseLayout(source_code):
    """
    Analyse the layout of a python source code.

    :param source_code: The source code to analyse

    :return: The document layout root node.
    """
    lines = source_code.splitlines()
    imports = DocumentLayoutNode("Imports", DocumentLayoutNode.Type.IMPORTS)
    root = DocumentLayoutNode("Root")
    root.start = 1
    root.end = len(lines) + 1
    root.addChild(imports)
    last_node = root
    prev_indent_level = 0
    for i, line in enumerate(lines):
        indent_lvl = getLineIndentationLevel(line)
        # imports
        if line.strip().startswith('import') or \
                line.strip().startswith("from"):
            if not imports.start:
                imports.start = i + 1
            imports.end = i + 1
        if "=" in line and not "==" in line and indent_lvl == 0:
            name = line.split("=")[0]
            varNode = DocumentLayoutNode(name,
                                         DocumentLayoutNode.Type.GLOBAL_VAR)
            varNode.start = varNode.end = i
            root.addChild(varNode)
        # function or class
        if line.strip().startswith("def") or line.strip().startswith("class"):
            node_type = DocumentLayoutNode.Type.CLASS
            if line.strip().startswith("def"):
                node_type = DocumentLayoutNode.Type.FUNCTION
            try:
                n = DocumentLayoutNode(line.lstrip().split(" ")[1].split("(")[0],
                                 node_type)
                n.indentationLevel = indent_lvl
                n.start = i + 1
                if indent_lvl < prev_indent_level:
                    last_node = last_node.parent
                    if not last_node:
                        last_node = root
                    last_node.addChild(n)
                elif indent_lvl > prev_indent_level:
                    last_node = last_node.children[len(last_node.children)-1]
                    last_node.addChild(n)
                else:
                    last_node.addChild(n)
                prev_indent_level = indent_lvl
            except IndexError:
                pass
    root.finalize(lines)
    return root


if __name__ == "__main__":
    with open(__file__, "r") as f:
        result = analyseLayout(f.read())
        result.debugPrint(indent=0)