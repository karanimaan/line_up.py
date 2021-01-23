from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidget

from MovableLabel import MovableLabel


class MyListWidget(QListWidget):

    def __init__(self, window):
        super(MyListWidget, self).__init__()
        self.setViewMode(QListWidget.IconMode)
        self.setDragDropMode(self.InternalMove)
        self.setIconSize(QSize(79, 100))
        self.maximumItems = 30
        from line_up import MainWindow
        self.window: MainWindow = window

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        item = self.itemAt(e.pos())
        if item is None:  # if not clicking on item, do nothing
            return

        if e.button() == Qt.RightButton:
            self.takeItem(self.row(item))
            self.parentWidget().parent().listWidget.addItem(item)
            pass

        else:
            rect = self.visualItemRect(item)
            itemPos = self.mapToParent(QPoint(rect.x(), rect.y()))

            filename = item.filename
            label = MovableLabel(self.window, filename)
            pixmap = QPixmap('Players/' + filename).scaledToHeight(100, QtCore.Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            label.setFixedSize(pixmap.size())
            label.move(itemPos)
            label.grabMouse()
            label.oldPos = itemPos
            label.clicked = False
            label.show()
            label.ogIndex = self.row(item)

            self.takeItem(self.row(item))
