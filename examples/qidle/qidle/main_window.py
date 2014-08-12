"""
This module contains the main window implementation.
"""
import os
import platform
import sys
from pyqode.core.api import TextHelper
from pyqode.core.api.syntax_highlighter import PYGMENTS_STYLES, ColorScheme
from pyqode.qt import QtCore
from pyqode.qt import QtWidgets
from pyqode.core import widgets
from pyqode.python.backend import server
from pyqode.python.widgets.code_edit import PyCodeEdit
from pyqode.python import modes
from .utils import get_interpreters
from .settings import Settings
from .forms.main_window_ui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Load our UI (made in Qt Designer)
        self.setupUi(self)
        self.dockWidget.hide()
        self.setup_recent_files_menu()
        self.setup_actions()
        self.setup_status_bar_widgets()
        self.on_current_tab_changed()
        self.interactiveConsole.open_file_requested.connect(self.open_file)
        self.styles_group = None

    def setup_status_bar_widgets(self):
        self.lbl_interpreter = QtWidgets.QLabel()
        self.lbl_filename = QtWidgets.QLabel()
        self.lbl_encoding = QtWidgets.QLabel()
        self.lbl_cursor_pos = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.lbl_filename, 200)
        self.statusbar.addPermanentWidget(self.lbl_interpreter, 100)
        self.statusbar.addPermanentWidget(self.lbl_encoding, 20)
        self.statusbar.addPermanentWidget(self.lbl_cursor_pos, 20)

    def setup_actions(self):
        """ Connects slots to signals """
        self.actionOpen.triggered.connect(self.on_open)
        self.actionNew.triggered.connect(self.on_new)
        self.actionSave.triggered.connect(self.on_save)
        self.actionSave_as.triggered.connect(self.on_save_as)
        self.actionClose_tab.triggered.connect(self.tabWidget.close)
        self.actionClose_other_tabs.triggered.connect(
            self.tabWidget.close_others)
        self.actionClose_all_tabs.triggered.connect(self.tabWidget.close_all)
        self.actionQuit.triggered.connect(
            QtWidgets.QApplication.instance().quit)
        self.tabWidget.currentChanged.connect(self.on_current_tab_changed)
        self.actionAbout.triggered.connect(self.on_about)
        self.actionRun.triggered.connect(self.on_run)
        self.interactiveConsole.process_finished.connect(
            self.on_process_finished)
        self.actionConfigure_run.triggered.connect(self.on_configure_run)

    def _enable_run(self):
        self.actionRun.setEnabled(self.tabWidget.currentWidget().file.path != '')
        self.actionConfigure_run.setEnabled(self.tabWidget.currentWidget().file.path != '')

    def setup_recent_files_menu(self):
        """ Setup the recent files menu and manager """
        self.recent_files_manager = widgets.RecentFilesManager(
            'pyqode', 'qidle')
        self.menu_recents = widgets.MenuRecentFiles(
            self.menuFile, title='Recents',
            recent_files_manager=self.recent_files_manager)
        self.menu_recents.open_requested.connect(self.open_file)
        self.menuFile.insertMenu(self.actionSave, self.menu_recents)
        self.menuFile.insertSeparator(self.actionSave)

    def setup_menu_interpreters(self):
        mnu = QtWidgets.QMenu('Select Python interpreter', self.menuEdit)
        group = QtWidgets.QActionGroup(self)
        group.triggered.connect(self.on_interpreter_changed)
        for interpreter in get_interpreters():
            a = QtWidgets.QAction(mnu)
            a.setText(interpreter)
            a.setCheckable(True)
            if interpreter == Settings().interpreter:
                a.setChecked(True)
            group.addAction(a)
            mnu.addAction(a)
        self.menuEdit.addSeparator()
        self.menuEdit.addMenu(mnu)

    def closeEvent(self, QCloseEvent):
        """
        Delegates the close event to the tabWidget to be sure we do not quit
        the application while there are some still some unsaved tabs.
        """
        self.tabWidget.closeEvent(QCloseEvent)

    def setup_editor(self, editor):
        """
        Setup the python editor, run the server and connect a few signals.

        :param editor: editor to setup.
        """
        editor.cursorPositionChanged.connect(self.on_cursor_pos_changed)
        zip_path = os.path.join(os.getcwd(), 'libraries.zip')
        if not os.path.exists(zip_path):
            if platform.system().lower() == 'linux':
                zip_path = '/usr/share/qidle/libraries.zip'
        if hasattr(sys, "frozen"):
            server_path = os.path.join(os.getcwd(), 'server.py')
            editor.backend.start(server_path,
                                 interpreter=Settings().interpreter,
                                 args=['-s', zip_path])
        else:
            editor.backend.start(
                server.__file__, interpreter=Settings().interpreter,
                args=['-s',
                      zip_path if 'python2' in Settings().interpreter else ''])
        m = editor.modes.get(modes.GoToAssignmentsMode)
        assert isinstance(m, modes.GoToAssignmentsMode)
        m.out_of_doc.connect(self.on_goto_out_of_doc)

    @QtCore.Slot(str)
    def open_file(self, path):
        """
        Creates a new GenericCodeEdit, opens the requested file and adds it
        to the tab widget.

        :param path: Path of the file to open

        :return The opened editor if open succeeded.
        """
        editor = None
        if path:
            index = self.tabWidget.index_from_filename(path)
            if index == -1:
                editor = PyCodeEdit(self)
                self.setup_editor(editor)
                editor.file.open(path)
                self.tabWidget.add_code_edit(editor)
                self.recent_files_manager.open_file(path)
                self.menu_recents.update_actions()
            else:
                self.tabWidget.setCurrentIndex(index)
        return editor

    @QtCore.Slot()
    def on_new(self):
        """
        Add a new empty code editor to the tab widget
        """
        editor = PyCodeEdit(self)
        self.setup_editor(editor)
        self.tabWidget.add_code_edit(editor, 'New document %d.py')
        self.actionRun.setDisabled(True)
        self.actionConfigure_run.setDisabled(True)

    @QtCore.Slot()
    def on_open(self):
        """
        Shows an open file dialog and open the file if the dialog was
        accepted.

        """
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open')
        if filename:
            self.open_file(filename)
        self.actionRun.setEnabled(True)
        self.actionConfigure_run.setEnabled(True)

    @QtCore.Slot()
    def on_save(self):
        self.tabWidget.save_current()
        self._enable_run()
        self._update_status_bar(self.tabWidget.currentWidget())

    @QtCore.Slot()
    def on_save_as(self):
        """
        Save the current editor document as.
        """
        path = self.tabWidget.currentWidget().file.path
        path = os.path.dirname(path) if path else ''
        filename, filter = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save', path)
        if filename:
            self.tabWidget.save_current(filename)
            self.recent_files_manager.open_file(filename)
            self.menu_recents.update_actions()
            self.actionRun.setEnabled(True)
            self.actionConfigure_run.setEnabled(True)
            self._update_status_bar(self.tabWidget.currentWidget())

    def setup_mnu_edit(self, editor):
        """
        Setup the edit menu for the current editor. We show the current editor
        context menu and a menu to change the python interpreter.

        :param editor: new editor
        """
        self.menuEdit.addActions(editor.actions())
        self.menuEdit.addSeparator()
        self.setup_menu_interpreters()
        self.setup_mnu_style(editor)

    def setup_mnu_style(self, editor):
        """ setup the style menu for an editor tab """
        menu = QtWidgets.QMenu('Styles', self.menuEdit)
        group = QtWidgets.QActionGroup(self)
        self.styles_group = group
        current_style = editor.syntax_highlighter.color_scheme.name
        group.triggered.connect(self.on_style_changed)
        for s in sorted(PYGMENTS_STYLES):
            a = QtWidgets.QAction(menu)
            a.setText(s)
            a.setCheckable(True)
            if s == current_style:
                a.setChecked(True)
            group.addAction(a)
            menu.addAction(a)
        self.menuEdit.addMenu(menu)

    def setup_mnu_modes(self, editor):
        for mode in editor.modes:
            a = QtWidgets.QAction(self.menuModes)
            a.setText(mode.name)
            a.setCheckable(True)
            a.setChecked(mode.enabled)
            a.changed.connect(self.on_mode_state_changed)
            a.mode = mode
            self.menuModes.addAction(a)

    def setup_mnu_panels(self, editor):
        """
        Setup the panels menu for the current editor.
        :param editor:
        """
        for panel in editor.panels:
            a = QtWidgets.QAction(self.menuModes)
            a.setText(panel.name)
            a.setCheckable(True)
            a.setChecked(panel.enabled)
            a.changed.connect(self.on_panel_state_changed)
            a.panel = panel
            self.menuPanels.addAction(a)

    @QtCore.Slot()
    def on_current_tab_changed(self):
        """
        Update action states when the current tab changed.
        """
        self.menuEdit.clear()
        self.menuModes.clear()
        self.menuPanels.clear()
        editor = self.tabWidget.currentWidget()
        self.menuEdit.setEnabled(editor is not None)
        self.menuModes.setEnabled(editor is not None)
        self.menuPanels.setEnabled(editor is not None)
        self.actionSave.setEnabled(editor is not None)
        self.actionSave_as.setEnabled(editor is not None)
        self.actionClose_tab.setEnabled(editor is not None)
        self.actionClose_all_tabs.setEnabled(editor is not None)
        self.actionConfigure_run.setEnabled(editor is not None)
        self.actionRun.setEnabled(editor is not None)
        self.actionClose_other_tabs.setEnabled(
            editor is not None and self.tabWidget.count() > 1)
        if editor:
            self.setup_mnu_edit(editor)
            self.setup_mnu_modes(editor)
            self.setup_mnu_panels(editor)
        self._update_status_bar(editor)

    def _update_status_bar(self, editor):
        if editor:
            self.lbl_cursor_pos.setText(
                '%d:%d' % TextHelper(editor).cursor_position())
            self.lbl_encoding.setText(editor.file.encoding)
            self.lbl_filename.setText(editor.file.path)
            self.lbl_interpreter.setText(Settings().interpreter)
        else:
            self.lbl_encoding.clear()
            self.lbl_filename.clear()
            self.lbl_cursor_pos.clear()

    @QtCore.Slot(QtWidgets.QAction)
    def on_style_changed(self, action):
        self._style = action.text()
        self.refresh_color_scheme()

    def refresh_color_scheme(self):
        if self.styles_group and self.styles_group.checkedAction():
            style = self.styles_group.checkedAction().text()
            style = style.replace('&', '')  # qt5 bug on kde?
        else:
            style = 'qt'
        for i in range(self.tabWidget.count()):
            editor = self.tabWidget.widget(i)
            editor.syntax_highlighter.color_scheme = ColorScheme(style)

    @QtCore.Slot(QtWidgets.QAction)
    def on_interpreter_changed(self, action):
        """
        Change the selected interpreter and restart server of opened editor to
        use the new interpreter.

        :param action: interpreter action that has been triggered
        """
        interpreter = action.text()
        Settings().interpreter = interpreter
        # restart server with the new interpreter
        for i in range(self.tabWidget.count()):
            editor = self.tabWidget.widget(i)
            editor.backend.stop()
            self.setup_editor(editor)
            self.lbl_interpreter.setText(interpreter)
            m = editor.modes.get(modes.PEP8CheckerMode)
            m.request_analysis()
            m = editor.modes.get(modes.FrostedCheckerMode)
            m.request_analysis()

    def on_panel_state_changed(self):
        """
        Enable disable the selected panel.
        """
        action = self.sender()
        action.panel.enabled = action.isChecked()
        action.panel.setVisible(action.isChecked())

    def on_mode_state_changed(self):
        """
        Enable/Disable the selected mode
        """
        action = self.sender()
        action.mode.enabled = action.isChecked()

    def on_about(self):
        """
        Show about dialog
        """
        QtWidgets.QMessageBox.about(
            self, 'pyQode qidle',
            'This qidle application is an example of what you can do with '
            'pyqode.python.')

    def on_run(self):
        """
        Run the current current script
        """
        filename = self.tabWidget.currentWidget().file.path
        wd = os.path.dirname(filename)
        args = Settings().get_run_config_for_file(filename)
        self.interactiveConsole.start_process(
            Settings().interpreter, args=[filename] + args, cwd=wd)
        self.dockWidget.show()
        self.actionRun.setEnabled(False)
        self.actionConfigure_run.setEnabled(False)

    def on_goto_out_of_doc(self, assignment):
        """
        Open the a new tab when goto goes out of the current document.

        :param assignment: Destination
        """
        editor = self.open_file(assignment.module_path)
        if editor:
            TextHelper(editor).goto_line(assignment.line, assignment.column)

    def on_process_finished(self):
        self.actionRun.setEnabled(True)
        self.actionConfigure_run.setEnabled(True)

    def on_configure_run(self):
        path = self.tabWidget.currentWidget().file.path
        args = Settings().get_run_config_for_file(path)
        text, status = QtWidgets.QInputDialog.getText(
            self, 'Run configuration', 'Script arguments:',
            QtWidgets.QLineEdit.Normal, ' '.join(args))
        if status:
            args = text.split(' ')
            Settings().set_run_config_for_file(path, args)

    @QtCore.Slot()
    def on_cursor_pos_changed(self):
        editor = self.tabWidget.currentWidget()
        if editor:
            self.lbl_cursor_pos.setText(
                '%d:%d' % TextHelper(editor).cursor_position())
