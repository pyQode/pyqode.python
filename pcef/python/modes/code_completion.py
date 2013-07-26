"""
Contains the JediCompletionProvider class implementation
"""
import logging
from pcef.core import CompletionProvider, Completion


ICONS = {'Class': ':/pcef_python_icons/rc/class.png',
         'class': ':/pcef_python_icons/rc/class.png',
         'Import': ':/pcef_python_icons/rc/namespace.png',
         'import': ':/pcef_python_icons/rc/namespace.png',
         'Statement': ':/pcef_python_icons/rc/var.png',
         'statement': ':/pcef_python_icons/rc/var.png',
         'ForFlow': ':/pcef_python_icons/rc/var.png',
         'forflow': ':/pcef_python_icons/rc/var.png',
         'Module': ':/pcef_python_icons/rc/keyword.png',
         'module': ':/pcef_python_icons/rc/keyword.png',
         'Param': ':/pcef_python_icons/rc/var.png',
         'param': ':/pcef_python_icons/rc/var.png',
         'Function': ':/pcef_python_icons/rc/func.png',
         'function': ':/pcef_python_icons/rc/func.png'}


class JediCompletionProvider(CompletionProvider):

    def run(self, code, line, column, completionPrefix,
            filePath, fileEncoding):
        try:
            import jedi
        except ImportError:
            logging.getLogger("pcef").warning(
                "Code completion not working, jedi not found")
            return []
        try:
            retVal = []
            script = jedi.Script(code, line, column,
                                 filePath, fileEncoding)
            # print("Jedi run", line, column)
            completions = script.completions()
            # print(len(completions))
            for completion in completions:
                    # get type from description
                    desc = completion.description
                    suggestionType = desc.split(':')[0]
                    # get the associated icon if any
                    icon = None
                    if suggestionType in ICONS:
                        icon = ICONS[suggestionType]
                    else:
                        logging.getLogger("pcef").warning(
                            "Unimplemented completion type: %s" % suggestionType)
                    retVal.append(Completion(completion.name, icon=icon,
                                             tooltip=desc.split(':')[1]))
        except Exception:
            pass
        # print("Finished")
        return retVal