"""
Contains the python code folding mode
"""
from pyqode.core.api import IndentFoldDetector, TextBlockHelper, TextHelper


class PythonFoldDetector(IndentFoldDetector):
    def detect_fold_level(self, prev_block, block):
        # Python is an indent based language so use indentation for folding
        # makes sense but we restrict new regions to indentation after a ':',
        # that way only the real logical blocks are displayed.
        lvl = super().detect_fold_level(prev_block, block)
        prev_lvl = TextBlockHelper.get_fold_lvl(prev_block)
        # strip end of line comments
        txt = prev_block.text().strip() if prev_block else ''
        if txt.find('#') != -1:
            txt = txt[:txt.find('#')].strip()
        # cancel false indentation, indentation can only happen if there is
        # ':' on the previous line
        if prev_block and lvl > prev_lvl and not (txt.endswith(':')):
            lvl = prev_lvl
        th = TextHelper(self.editor)
        fmts = ['docstring']
        wasdocstring = th.is_comment_or_string(prev_block, formats=fmts)
        if block.docstring:
            if wasdocstring:
                # find block that starts the docstring
                p = prev_block.previous()
                wasdocstring = th.is_comment_or_string(p, formats=fmts)
                while wasdocstring or p.text().strip() == '':
                    p = p.previous()
                    wasdocstring = th.is_comment_or_string(p, formats=fmts)
                lvl = TextBlockHelper.get_fold_lvl(p.next()) + 1
        return lvl
