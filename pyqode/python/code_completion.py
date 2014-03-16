"""
This module contains the python code completion provider based on Jedi.

"""
from pyqode.core import logger
from pyqode.core.api import code_completion


#: associate types to icons
# todo clean the types list for jedi 0.8.0
ICONS = {'CLASS': ':/pyqode_python_icons/rc/class.png',
         'IMPORT': ':/pyqode_python_icons/rc/namespace.png',
         'STATEMENT': ':/pyqode_python_icons/rc/var.png',
         'FORFLOW': ':/pyqode_python_icons/rc/var.png',
         'MODULE': ':/pyqode_python_icons/rc/namespace.png',
         'KEYWORD': ':/pyqode_python_icons/rc/keyword.png',
         'PARAM': ':/pyqode_python_icons/rc/var.png',
         'PARAM-PRIV': ':/pyqode_python_icons/rc/var.png',
         'PARAM-PROT': ':/pyqode_python_icons/rc/var.png',
         'FUNCTION': ':/pyqode_python_icons/rc/func.png',
         'DEF': ':/pyqode_python_icons/rc/func.png',
         'FUNCTION-PRIV': ':/pyqode_python_icons/rc/func_priv.png',
         'FUNCTION-PROT': ':/pyqode_python_icons/rc/func_prot.png'}


def icon_from_typename(name, type):
    """
    Returns the icon resource filename that corresponds to the given typename.

    :param name: name of the completion. Use to make the distinction between
        public and private completions (using the count of starting '_')
    :pram typename: the typename reported by jedi

    :returns: The associate icon resource filename or None.
    """
    retVal = None
    type = type.upper()
    # jedi 0.8 introduced NamedPart class, which have a string instead of being
    # one
    if hasattr(name, "string"):
        name = name.string
    if type == "FORFLOW" or type == "STATEMENT":
        type = "PARAM"
    if type == "PARAM" or type == "FUNCTION":
        if name.startswith("__"):
            type += "-PRIV"
        elif name.startswith("_"):
            type += "-PROT"
    if type in ICONS:
        retVal = ICONS[type]
    elif type:
        logger.warning("Unimplemented completion type: %s" %
                       type)
    return retVal


class JediProvider(code_completion.Provider):
    """
    Provides code completion using the awesome `jedi`_  library

    .. _`jedi`: https://github.com/davidhalter/jedi
    """

    def complete(self, code, line, column, prefix, path, encoding):
        """
        Completes python code using `jedi`_.

        :returns: a list of completion.
        """
        retVal = []
        try:
            import jedi
        except ImportError:
            logger.error("Failed to import jedi. Check your jedi "
                         "installation")
        else:
            try:
                script = jedi.Script(code, line, column, path,
                                     encoding)

                completions = script.completions()
            except jedi.NotFoundError:
                completions = []
            for completion in completions:
                name = completion.name
                # desc = completion.description
                # deduce type from description
                type = completion.type
                if "getset_descriptor" in completion.description:
                    type = 'STATEMENT'
                if type.lower() == 'import':
                    try:
                        definition = completion.follow_definition()[0]
                        type = definition.type
                    except (IndexError, AttributeError):
                        # no definition
                        # AttributeError is raised for GlobalNamespace
                        pass
                desc = completion.full_name
                icon = icon_from_typename(name, type)
                retVal.append({'name': name, 'icon': icon, 'tooltip': desc})
        return retVal
