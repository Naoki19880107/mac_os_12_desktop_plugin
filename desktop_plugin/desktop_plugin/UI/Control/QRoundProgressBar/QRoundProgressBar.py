from typing import Iterable, Union

from PyQt5.QtCore import QRectF, Qt, QRect
from PyQt5.QtGui import QGradient, QColor, QPaintEvent, QImage, QPainter, QPen, QPainterPath, QFont, QConicalGradient, \
    QPalette, QBrush
from PyQt5.QtWidgets import QWidget

from desktop_plugin.UI.Control.QRoundProgressBar.BarStyle_Enum import BarStyle_Enum
from desktop_plugin.UI.Control.QRoundProgressBar.Position_Enum import Position_Enum
from desktop_plugin.UI.Control.QRoundProgressBar.UpdateFlags_Enum import UpdateFlags_Enum


class QRoundProgressBar(QWidget):
    def __init__(self, parent: QWidget = None):
        super(QRoundProgressBar, self).__init__(parent)
        self.__m_min: float = 0
        self.__m_max: float = 100
        self.__m_value: float = 25
        self.__m_position: Position_Enum = Position_Enum.PositionTop
        self.__m_bar_style: BarStyle_Enum = BarStyle_Enum.StyleDonut
        self.__m_outlinePenWidth: float = 1.0
        self.__m_dataPenWidth: float = 1.0
        self.__m_rebuildBrush: bool = False
        self.__m_format: str = "%p%"
        self.__m_decimals: int = 1
        self.__m_updateFlags: UpdateFlags_Enum = UpdateFlags_Enum.UF_PERCENT
        self.__m_gradientData: Iterable[tuple[float, Union[QColor, QGradient]]] = []
        self.__transparent_brush = QBrush(Qt.transparent)

    def setRange(self, min: float, max: float):
        self.__m_min = min
        self.__m_max = max
        if self.__m_min > self.__m_max:
            self.__m_min, self.__m_max = self.__m_max, self.__m_min
        if self.__m_value < self.__m_min:
            self.__m_value = self.__m_min
        elif self.__m_value > self.__m_max:
            self.__m_value = self.__m_max
        if self.__m_gradientData:
            self.__m_rebuildBrush = True
        self.update()

    def setMinimum(self, min: float):
        self.setRange(min, self.__m_max)

    def setMaximum(self, max: float):
        self.setRange(self.__m_min, max)

    def setValue(self, val: float):
        if self.__m_value != val:
            if val < self.__m_min:
                self.__m_value = self.__m_min
            elif val > self.__m_max:
                self.__m_value = self.__m_max
            else:
                self.__m_value = val
            self.update()

    def setValueInt(self, val: int):
        self.setValue(float(val))

    def setPosition(self, position: Position_Enum):
        if self.__m_position != position:
            self.__m_position = position
            if self.__m_gradientData:
                self.__m_rebuildBrush = True
            self.update()

    def setBarStyle(self, style: BarStyle_Enum):
        if self.__m_bar_style != style:
            self.__m_bar_style = style
            self.update()

    def setOutlinePenWidth(self, pen_width: float):
        if self.__m_outlinePenWidth != pen_width:
            self.__m_outlinePenWidth = pen_width
            self.update()

    def setDataPenWidth(self, pen_width: float):
        if self.__m_dataPenWidth != pen_width:
            self.__m_dataPenWidth = pen_width
            self.update()

    def setDataColors(self, stopPoints: Iterable[tuple[float, Union[QColor, QGradient]]]):
        if self.__m_gradientData != stopPoints:
            self.__m_gradientData = stopPoints
            self.__m_rebuildBrush = True
            self.update()

    def __valueFormatChanged(self):
        self.__m_updateFlags = UpdateFlags_Enum.UF_INIT
        if "%v" in self.__m_format:
            self.__m_updateFlags |= UpdateFlags_Enum.UF_VALUE
        if "%p" in self.__m_format:
            self.__m_updateFlags |= UpdateFlags_Enum.UF_PERCENT
        if "%m" in self.__m_format:
            self.__m_updateFlags |= UpdateFlags_Enum.UF_MAX
        self.update()

    def setFormat(self, format: str):
        if self.__m_format != format:
            self.__m_format = format
            self.__valueFormatChanged()

    def resetFormat(self):
        self.__m_format: str = ''
        self.__valueFormatChanged()

    def setDecimals(self, count: int):
        if count > 0 and count != self.__m_decimals:
            self.__m_decimals = count
            self.__valueFormatChanged()

    def paintEvent(self, event: QPaintEvent):
        if self.width() < self.height():
            outerRadius: int = self.width()
        else:
            outerRadius: int = self.height()
        baseRect: QRectF = QRectF(1, 1, outerRadius - 2, outerRadius - 2)
        buffer_rect = QRect(1, 1, outerRadius, outerRadius)
        p: QPainter = QPainter(self)
        '''
        data brush
        '''
        self.__rebuildDataBrushIfNeeded()
        '''
        background
        '''
        self.__drawBackground(p, buffer_rect)
        '''
        base circle
        '''
        self.__drawBase(p, baseRect)
        '''
        data circle
        '''
        arcStep: float = 360.0 / (self.__m_max - self.__m_min) * self.__m_value
        self.__drawValue(p, baseRect, self.__m_value, arcStep)
        '''
        center circle
        '''
        innerRadius, innerRect = self.__calculateInnerRect(outerRadius)
        self.__drawInnerBackground(p, innerRect)
        '''
        text
        '''
        self.__drawText(p, innerRect, innerRadius, self.__m_value)
        '''
        finally draw the bar
        '''
        p.end()

    def __drawBackground(self, p: QPainter, baseRect: QRectF):
        p.fillRect(baseRect, self.__transparent_brush)

    def __drawBase(self, p: QPainter, baseRect: QRectF):
        func_dict = {
            BarStyle_Enum.StyleDonut: self.__drawBase_StyleDonut,
            BarStyle_Enum.StylePie: self.__drawBase_StylePie,
            BarStyle_Enum.StyleLine: self.__drawBase_StyleLine
        }
        if self.__m_bar_style in func_dict.keys():
            func_dict[self.__m_bar_style](p, baseRect)

    def __drawBase_StyleDonut(self, p: QPainter, baseRect: QRectF):
        p.setPen(QPen(self.palette().shadow().color(), self.__m_outlinePenWidth))
        p.setBrush(self.palette().base())
        p.drawEllipse(baseRect)

    def __drawBase_StylePie(self, p: QPainter, baseRect: QRectF):
        p.setPen(QPen(self.palette().base().color(), self.__m_outlinePenWidth))
        p.setBrush(self.palette().base())
        p.drawEllipse(baseRect)

    def __drawBase_StyleLine(self, p: QPainter, baseRect: QRectF):
        p.setPen(QPen(self.palette().base().color(), self.__m_outlinePenWidth))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(
            baseRect.adjusted(self.__m_outlinePenWidth / 2, self.__m_outlinePenWidth / 2, -self.__m_outlinePenWidth / 2,
                              -self.__m_outlinePenWidth / 2))

    def __drawValue(self, p: QPainter, baseRect: QRectF, value: float, arcLength: float):

        """
        nothing to draw
        """
        if value == self.__m_min:
            return

        '''
        for Line style
        '''
        if self.__m_bar_style == BarStyle_Enum.StyleLine:
            p.setPen(QPen(self.palette().highlight().color(), self.__m_dataPenWidth))
            p.setBrush(Qt.NoBrush)
            p.drawArc(baseRect.adjusted(self.__m_outlinePenWidth / 2, self.__m_outlinePenWidth / 2,
                                        -self.__m_outlinePenWidth / 2, -self.__m_outlinePenWidth / 2),
                      self.__m_position * 16, -arcLength * 16)
            return

        '''
        for Pie and Donut styles
        '''
        dataPath: QPainterPath = QPainterPath()
        dataPath.setFillRule(Qt.WindingFill)
        '''
        pie segment outer
        '''
        dataPath.moveTo(baseRect.center())
        dataPath.arcTo(baseRect, self.__m_position, -arcLength)
        dataPath.lineTo(baseRect.center())

        p.setBrush(self.palette().highlight())
        p.setPen(QPen(self.palette().shadow().color(), self.__m_dataPenWidth))
        p.drawPath(dataPath)

    def __calculateInnerRect(self, outerRadius: float) -> tuple[float, QRectF]:

        """
        for Line style
        """
        if self.__m_bar_style == BarStyle_Enum.StyleLine:
            innerRadius = outerRadius - self.__m_outlinePenWidth
        else:
            '''
            for Pie and Donut styles
            '''
            innerRadius = outerRadius * 0.75
        delta: float = (outerRadius - innerRadius) / 2
        innerRect = QRectF(delta, delta, innerRadius, innerRadius)
        return innerRadius, innerRect

    def __drawInnerBackground(self, p: QPainter, innerRect: QRectF):
        if self.__m_bar_style == BarStyle_Enum.StyleDonut:
            p.setBrush(self.palette().alternateBase())
            p.drawEllipse(innerRect)

    def __drawText(self, p: QPainter, innerRect: QRectF, innerRadius: float, value: float):
        if self.__m_format == '':
            return
        f: QFont = QFont(self.font())
        if 0.05 < 0.35 - self.__m_decimals * 0.08:
            f.setPixelSize(innerRadius * (0.35 - self.__m_decimals * 0.08))
        else:
            f.setPixelSize(innerRadius * 0.05)
        p.setFont(f)
        textRect: QRectF = QRectF(innerRect)
        p.setPen(self.palette().text().color())
        p.drawText(textRect, Qt.AlignCenter, self.__valueToText(value))

    def __valueToText(self, value: float) -> str:
        textToDraw = self.__m_format
        if self.__m_updateFlags == UpdateFlags_Enum.UF_VALUE:
            value_str = str('{: .' + str(self.__m_decimals) + 'f}').format(value)
            textToDraw = textToDraw.replace("%v", value_str)
        elif self.__m_updateFlags == UpdateFlags_Enum.UF_PERCENT:
            percent: float = (value - self.__m_min) / (self.__m_max - self.__m_min) * 100.0
            percent_str = str('{: .' + str(self.__m_decimals) + 'f}').format(percent)
            textToDraw = textToDraw.replace("%p", percent_str)
        elif self.__m_updateFlags == UpdateFlags_Enum.UF_MAX:
            if self.__m_min:
                value_str = str('{: .' + str(self.__m_decimals) + 'f}').format(self.__m_max - self.__m_min + 1)
                textToDraw = textToDraw.replace("%m", value_str).format('%.' + str(self.__m_decimals) + 'f')
            else:
                value_str = str('{: .' + str(self.__m_decimals) + 'f}').format(self.__m_max)
                textToDraw = textToDraw.replace("%m", value_str).format('%.' + str(self.__m_decimals) + 'f')
        return textToDraw

    def __rebuildDataBrushIfNeeded(self):
        if self.__m_rebuildBrush:
            self.__m_rebuildBrush = False
            dataBrush: QConicalGradient = QConicalGradient()
            dataBrush.setCenter(0.5, 0.5)
            dataBrush.setCoordinateMode(QGradient.StretchToDeviceMode)
            for item in self.__m_gradientData:
                pos, color = item
                dataBrush.setColorAt(1 - pos, color)
            dataBrush.setAngle(self.__m_position)
            p: QPalette = QPalette(self.palette())
            p.setBrush(QPalette.Highlight, dataBrush)
            self.setPalette(p)
