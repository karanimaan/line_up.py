from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QListWidget, QListWidgetItem


# noinspection PyTypeChecker
class MovableLabel(QLabel):

    def __init__(self, mainWindow: QMainWindow, filename: str):
        super().__init__(mainWindow)
        self.mainWindow = mainWindow
        self.filename = filename
        self.clicked = False
        self.ogIndex = -1
        self.buttonPressed = Qt.LeftButton  # default
        self.oldPos = None

    def mousePressEvent(self, evt):
        """Select the toolbar."""
        self.buttonPressed = evt.button()
        if evt.button() == Qt.RightButton:
            self.mouseReleaseEvent(evt)
        self.oldPos = evt.globalPos()
        self.ogIndex = -1

    def mouseMoveEvent(self, evt):
        """Move the toolbar with mouse iteration."""
        if self.clicked:
            delta = QPoint(evt.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
        else:
            self.clicked = True
        self.oldPos = evt.globalPos()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.releaseMouse()
        self.clicked = False
        listWidget: QListWidget = self.mainWindow.listWidget
        if ev.globalPos().x() < listWidget.width() or self.buttonPressed == Qt.RightButton:
            pos = listWidget.mapFromGlobal(ev.globalPos())
            index = listWidget.indexAt(pos).row()

            icon = QIcon(self.pixmap())
            item = QListWidgetItem(icon, "")
            item.filename = self.filename

            if index == -1:
                listWidget.addItem(item)
            else:
                listWidget.insertItem(index, item)

            self.setParent(None)
