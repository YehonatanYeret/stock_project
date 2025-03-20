from PySide6.QtCore import QObject, Slot
from PySide6.QtCore import QRunnable, QThreadPool, Signal


class WorkerSignals(QObject):
    result = Signal(object)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(result)


class ChatbotPresenter(QObject):
    def __init__(self, model, view, user_id=None):
        super().__init__()
        self.view = view
        self.model = model
        if user_id:
            self.model.set_user_id(user_id)
        self.view.send_message_signal.connect(self.handle_user_message)

    @Slot(str)
    def handle_user_message(self, message_content: str):
        # Add wait indicator before starting the async task.
        self.view.add_wait_indicator()
        worker = Worker(self.model.generate_ai_response, message_content)
        worker.signals.result.connect(self._handle_response)
        QThreadPool.globalInstance().start(worker)

    @Slot(object)
    def _handle_response(self, result):
        self.view.add_response(result)
