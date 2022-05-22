from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QBitmap, QPainter, QColor


class ImagePlus:
    @staticmethod
    def PixmapToRound(src: QPixmap, radius: int) -> QPixmap:
        if src.isNull():
            return QPixmap()
        size = QSize(2 * radius, 2 * radius)
        mask = QBitmap(size)
        painter = QPainter()
        painter.begin(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.fillRect(0, 0, size.width(), size.height(), QtCore.Qt.white)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRoundedRect(0, 0, size.width(), size.height(), 99, 99)
        painter.end()
        image = QPixmap(src.scaled(size))
        image.setMask(mask)
        return image
