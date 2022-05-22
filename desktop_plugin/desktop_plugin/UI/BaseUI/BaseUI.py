from abc import abstractmethod, ABC

from PyQt5 import QtWidgets, QtCore


class BaseUI(ABC):
    def setupUi(self, widget: QtWidgets.QWidget):
        widget.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint)
        widget.setFixedSize(widget.width(), widget.height())
        self._setGeometry(widget)
        self._BindEvent(widget)

    @abstractmethod
    def _setGeometry(self, widget: QtWidgets.QWidget):
        pass

    @abstractmethod
    def _BindEvent(self, widget: QtWidgets.QWidget):
        pass
