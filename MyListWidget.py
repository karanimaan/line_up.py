from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtWidgets import QListWidget

from MovableLabel import MovableLabel


class MyListWidget(QListWidget):

    def __init__(self, parent):
        super(MyListWidget, self).__init__(parent)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        item = self.itemAt(e.pos())
        rect = self.visualItemRect(item)
        itemPos = QPoint(rect.x(), rect.y())
        imageSize = item.icon().actualSize(QSize(100, 200))

        self.takeItem(self.row(item))

        label = MovableLabel(self.parentWidget(), 'Pogba.jpg')
        pixmap = item.icon().pixmap(imageSize)
        label.setPixmap(pixmap)
        label.setFixedSize(imageSize)
        label.move(itemPos)
        label.grabMouse()
        label.oldPos = itemPos
        label.clicked = False
        label.show()
