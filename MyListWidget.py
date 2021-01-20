from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidget

from MovableLabel import MovableLabel


class MyListWidget(QListWidget):

    def __init__(self):
        super(MyListWidget, self).__init__()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        item = self.itemAt(e.pos())
        while item is None:
            return
        rect = self.visualItemRect(item)
        itemPos = QPoint(rect.x(), rect.y())
        imageSize = item.icon().actualSize(QSize(100, 200))

        filename = item.data(self.parentWidget().filenameRole)
        label = MovableLabel(self.parentWidget(), filename)
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
