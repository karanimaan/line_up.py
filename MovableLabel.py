from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QListWidget, QListWidgetItem


class MovableLabel(QLabel):
    """WToolBar is a personalized toolbar."""

    homeAction = None

    oldPos = QPoint()

    def __init__(self, mainWindow: QMainWindow, filename: str):
        super().__init__(mainWindow)
        self.mainWindow = mainWindow
        self.filename = filename
        self.clicked = False

    def mousePressEvent(self, evt):
        """Select the toolbar."""
        self.oldPos = evt.globalPos()

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
        if ev.globalPos().x() < listWidget.width():
            pos = listWidget.mapFromGlobal(ev.globalPos())
            index = listWidget.indexAt(pos).row()
            icon = QIcon(self.pixmap())
            listWidget.insertItem(index, QListWidgetItem(icon, ""))

            self.hide()
            if self in self.mainWindow.players:
                self.mainWindow.players.remove(self)
        if self not in self.mainWindow.players:
            self.mainWindow.players.append(self)