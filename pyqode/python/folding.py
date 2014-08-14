"""
Contains the python code folding mode
"""
import re
from pyqode.core.api import IndentFoldDetector, TextBlockHelper, TextHelper


class PythonFoldDetector(IndentFoldDetector):
    single_line_docstring = re.compile(r'""".*"""')

    def _strip_comments(self, prev_block):
        txt = prev_block.text().strip() if prev_block else ''
        if txt.find('#') != -1:
            txt = txt[:txt.find('#')].strip()
        return txt

    def _handle_docstrings(self, block, lvl, prev_block):
        if block.docstring:
            is_start = block.text().strip().startswith('"""')
            if is_start:
                TextBlockHelper.get_fold_lvl(prev_block) + 1
            else:
                pblock = block
                while not is_start and pblock.isValid():
                    pblock = pblock.previous()
                    is_start = pblock.text().strip().startswith('"""')
                return TextBlockHelper.get_fold_lvl(pblock) + 1
        # fix end of docstring
        elif prev_block and prev_block.text().strip().endswith('"""'):
            single_line = self.single_line_docstring.match(
                prev_block.text().strip())
            if single_line:
                TextBlockHelper.set_fold_lvl(prev_block, lvl)
            else:
                TextBlockHelper.set_fold_lvl(
                    prev_block, TextBlockHelper.get_fold_lvl(
                        prev_block.previous()))
        return lvl

    def detect_fold_level(self, prev_block, block):
        if block.blockNumber() == 23:
            pass
        # Python is an indent based language so use indentation for folding
        # makes sense but we restrict new regions to indentation after a ':',
        # that way only the real logical blocks are displayed.
        lvl = super().detect_fold_level(prev_block, block)
        # cancel false indentation, indentation can only happen if there is
        # ':' on the previous line
        prev_lvl = TextBlockHelper.get_fold_lvl(prev_block)
        if prev_block and lvl > prev_lvl and not (
                self._strip_comments(prev_block).endswith(':')):
            lvl = prev_lvl
        lvl = self._handle_docstrings(block, lvl, prev_block)
        return lvl
