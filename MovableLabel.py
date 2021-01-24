from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QListWidgetItem


class MovableLabel(QLabel):

    def __init__(self, mainWindow, filename: str):
        super().__init__(mainWindow)
        from line_up import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.filename = filename
        self.clicked = False
        self.ogIndex = -1
        self.buttonPressed = Qt.LeftButton  # default
        self.oldPos = None
        pixmap = QPixmap('Players/' + filename).scaledToHeight(100, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.setFixedSize(pixmap.width(), pixmap.height())
        self.raise_()

    def __int__(self, mainWindow):
        self.__init__(mainWindow, '')

    def mousePressEvent(self, evt):
        """Select the toolbar."""
        self.buttonPressed = evt.button()
        if evt.button() == Qt.RightButton:
            self.mouseReleaseEvent(evt)
        self.oldPos = evt.globalPos()
        self.ogIndex = -1
        self.raise_()

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
        index = -1

        if self.buttonPressed == Qt.RightButton:
            listWidget = self.mainWindow.listWidget
        else:
            from MyListWidget import MyListWidget
            listWidget: MyListWidget
            for listWidget in self.mainWindow.findChildren(MyListWidget):
                pos = listWidget.mapFromGlobal(ev.globalPos())
                if listWidget.rect().contains(pos) and listWidget.count() < listWidget.maximumItems:
                    index = listWidget.indexAt(pos).row()
                    break
            else:
                listWidget = None

        if listWidget is not None:
            icon = QIcon(self.pixmap())
            item = QListWidgetItem(icon, "")
            item.filename = self.filename

            if index == -1:
                listWidget.addItem(item)
            else:
                listWidget.insertItem(index, item)

            self.setParent(None)
