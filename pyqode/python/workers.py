"""
Contains the worker classes/functions executed on the server side.
"""
import os
from pyqode.core import logger
from pyqode.core.api.constants import CheckerMessages
from pyqode.python.code_completion import icon_from_typename
from pyqode.python.pep8utils import CustomChecker, CustomReport


def calltips(request_data):
    """
    Worker that returns a list of calltips.

    A calltips is a tuple made of the following parts:
      - module_name: name of the module of the function invoked
      - call_name: name of the function that is being called
      - params: the list of parameter names.
      - index: index of the current parameter
      - bracket_start

    :returns tuple(module_name, call_name, params)
    """
    def param_name(p):
        try:
            return p.get_name()
        except AttributeError:
            return p.name

    try:
        import jedi
    except ImportError:
        logger.error("Failed to import jedi. Check your jedi "
                     "installation")
    else:
        code = request_data['code']
        line = request_data['line']
        column = request_data['column']
        path = request_data['path']
        # encoding = request_data['encoding']
        encoding = 'utf-8'
        # use jedi to get call signatures
        script = jedi.Script(code, line, column, path, encoding)
        signatures = script.call_signatures()
        for c in signatures:
            for par in c.params:
                print(dir(par))
            results = (str(c.module.name), str(c.call_name),
                       [param_name(p) for p in c.params], c.index,
                       c.bracket_start, column)
            # todo: add support for multiple signatures
            return True, results
        return False, []


def goto_assignments(request_data):
    try:
        import jedi
    except ImportError:
        logger.error("Failed to import jedi. Check your jedi "
                     "installation")
    else:
        code = request_data['code']
        line = request_data['line']
        column = request_data['column']
        path = request_data['path']
        # encoding = request_data['encoding']
        encoding = 'utf-8'
        script = jedi.Script(code, line, column, path, encoding)
        try:
            definitions = script.goto_assignments()
        except jedi.NotFoundError:
            return []
        else:
            ret_val = [(d.module_path, d.line, d.column, d.full_name)
                       for d in definitions]
            return True, ret_val
    return False, None

_old_definitions = {}


class Definition(object):
    """
    Represents a defined name in a python source code (import, function, class,
    method). Definition usually form a tree limited to 2 levels (we stop at the
    method level).
    """
    def __init__(self, name='', icon='', line=1, column=0, full_name=''):
        #: Icon resource name associated with the definition, can be None
        self.icon = icon
        #: Definition name (name of the class, method, variable)
        if hasattr(name, "string"):
            name = name.string
        self.name = name
        #: The line of the definition in the current editor text
        self.line = line
        #: The column of the definition in the current editor text
        self.column = column
        #: Symbol name + parent name (for methods and class variables)
        self.full_name = full_name
        #: Possible list of children (only classes have children)
        self.children = []
        if self.full_name == "":
            self.full_name = self.name

    def add_child(self, definition):
        """
        Adds a child definition
        """
        self.children.append(definition)

    def to_dict(self):
        """
        Serialises a definition to a dictionary, ready for json.

        Children are serialised recursively.
        """
        ddict = {'name': self.name, 'icon': self.icon,
                 'line': self.line, 'column': self.column,
                 'full_name': self.full_name, 'children': []}
        for child in self.children:
            ddict['children'].append(child.to_dict())
        return ddict

    def from_dict(self, ddict):
        """
        Deserialise the definition from a simple dict.
        """
        self.name = ddict['name']
        self.icon = ddict['icon']
        self.line = ddict['line']
        self.column = ddict['column']
        self.full_name = ddict['full_name']
        self.children[:] = []
        for child_dict in ddict['children']:
            self.children.append(Definition().from_dict(child_dict))
        return self

    def __repr__(self):
        return 'Definition(%r, %r, %r, %r)' % (self.name, self.icon,
                                               self.line, self.column)

    def __eq__(self, other):
        if len(self.children) != len(other.children):
            return False
        for self_child, other_child in zip(self.children, other.children):
            if self_child != other_child:
                return False
        return (self.name == other.name and self.full_name == other.full_name
                and self.line == other.line and self.column == other.column)


def defined_names(request_data):
    def _compare_definitions(a, b):
        """
        Compare two definition lists.

        Returns True if they are different.
        """
        if len(a) != len(b):
            return True
        else:
            # compare every definition. If one is different, break
            for def_a, def_b in zip(a, b):
                if def_a != def_b:
                    return True
            return False

    global _old_definitions
    try:
        import jedi
    except ImportError:
        logger.error("Failed to import jedi. Check your jedi "
                     "installation")
    else:
        code = request_data['code']
        path = request_data['path']
        # encoding = request_data['encoding']
        encoding = 'utf-8'
        ret_val = []
        toplvl_definitions = jedi.defined_names(code, path, encoding)
        for d in toplvl_definitions:
            d_line, d_column = d.start_pos
            # use full name for import type
            definition = Definition(d.name, icon_from_typename(d.name, d.type),
                                    d_line, d_column, d.full_name)
            # check for methods in class
            if d.type == "class":
                sub_definitions = d.defined_names()
                for sub_d in sub_definitions:
                    icon = icon_from_typename(sub_d.name, sub_d.type)
                    line, column = sub_d.start_pos
                    if sub_d.full_name == "":
                        sub_d.full_name = sub_d.name
                    sub_definition = Definition(sub_d.name, icon, line, column,
                                                sub_d.full_name)
                    definition.add_child(sub_definition)
            ret_val.append(definition)
        try:
            old_definitions = _old_definitions["%s_definitions" % path]
        except KeyError:
            old_definitions = []
        status = False
        if ret_val:
            if not _compare_definitions(ret_val, old_definitions):
                ret_val = None
                logger.debug("No changes detected")
            else:
                _old_definitions["%s_definitions" % path] = ret_val
                logger.debug("Document structure changed")
                status = True
                ret_val = [d.to_dict() for d in ret_val]
        return status, ret_val
    return False, None


def quick_doc(request_data):
    code = request_data['code']
    line = request_data['line']
    column = request_data['column']
    path = request_data['path']
    # encoding = 'utf-8'
    encoding = 'utf-8'
    try:
        import jedi
    except ImportError:
        logger.error("Failed to import jedi. Check your jedi "
                     "installation")
    else:
        script = jedi.Script(code, line, column, path, encoding)
        try:
            definitions = script.goto_definitions()
        except jedi.NotFoundError:
            return []
        else:
            ret_val = [d.doc for d in definitions]
            return True, ret_val
    return False, []


def run_pep8(request_data):
    """
    Worker that run the pep8 tool on the current editor text.

    :returns a list of tuples (msg, msg_type, line_number)
    """
    import pep8

    code = request_data['code']
    filePath = request_data['path']
    # setup our custom style guide with our custom checker which returns a list
    # of strings instread of spitting the results at stdout
    pep8style = pep8.StyleGuide(parse_argv=False, config_file=True,
                                checker_class=CustomChecker)
    results = pep8style.input_file(filePath, lines=code.splitlines(True))
    messages = []
    for line_number, offset, code, text, doc in results:
        messages.append((text, CheckerMessages.WARNING, line_number))
    return True, messages


def run_frosted(request_data):
    """
    Worker that run a frosted (the fork of pyflakes) code analysis on the
    current editor text.
    """
    import _ast
    ret_val = []
    code = request_data['code']
    path = request_data['path']
    encoding = request_data['encoding']
    # First, compile into an AST and handle syntax errors.
    if not code or not encoding:
        return
    try:
        tree = compile(code.encode(encoding), path, "exec",
                       _ast.PyCF_ONLY_AST)
    except SyntaxError as value:
        msg = value.args[0]
        (lineno, offset, text) = value.lineno, value.offset, value.text
        # If there's an encoding problem with the file, the text is None
        if text is None:
            # Avoid using msg, since for the only known case, it
            # contains a bogus message that claims the encoding the
            # file declared was unknown.s
            logger.warning("%s: problem decoding source" % path)
        else:
            ret_val.append((msg, CheckerMessages.ERROR, lineno))
    else:
        # Okay, it's syntactically valid.  Now check it.
        from frosted import checker
        w = checker.Checker(tree, os.path.split(path)[1])
        w.messages.sort(key=lambda m: m.lineno)
        for warning in w.messages:
            msg = "%s: %s" % (warning.type.error_code, warning.message)
            line = warning.lineno
            status = (CheckerMessages.WARNING
                      if warning.type.error_code.startswith('W')
                      else CheckerMessages.ERROR)
            ret_val.append((msg, status, line))
    return True, ret_val
