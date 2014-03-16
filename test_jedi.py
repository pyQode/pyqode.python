import jedi

from PyQt5.QtWidgets import QWidget

print(jedi.Script('from PyQt5.QtWigets import Q').completions())
