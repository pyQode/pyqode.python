from pyqode.core import CodeCompletionMode, logger
from pyqode.qt import QtCore


class PreloadWorker(object):
    def __init__(self, modules):
        self.modules = modules

    def __call__(self, *args, **kwargs):
        import jedi
        logger.debug("Boostrapper.preload started: %r" % self.modules)
        jedi.api.preload_module(*self.modules)
        logger.debug("Boostrapper.preload finished")


class Bootstrapper(QtCore.QObject):
    """
    Utility class to help you bootstrap the code completion (if you don't want
    to use the lazy bootstrap).

    The bootstrap consists of launching the code completion server and running
    a worker that will pre-load a list of modules.
    """
    #: Signal emitted when the preload worker has finished.
    preLoadFinished = QtCore.Signal()

    def __init__(self, modules):
        """
        :param modules: List of modules (strings) to preload.
        """
        super(Bootstrapper, self).__init__()
        self.modules = modules

    def bootstrap(self):
        """
        Bootstraps code completion.
        """
        server = CodeCompletionMode.startCompletionServer()
        server.signals.workCompleted.connect(self._onWorkFinished)
        if self.modules:
            server.requestWork(self, PreloadWorker(self.modules))

    def _onWorkFinished(self, caller_id, worker):
        if caller_id == id(self) and isinstance(worker, PreloadWorker):
            self.preLoadFinished.emit()
