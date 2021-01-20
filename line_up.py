import json
import os
import sys

from PyQt5 import QtGui
from PyQt5.Qt import QPixmap
from PyQt5.QtCore import QPoint, Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem

from MovableLabel import MovableLabel
from MyListWidget import MyListWidget


class MainWindow(QMainWindow):


    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.players = []
        pixmap = QPixmap()

        listWidget = MyListWidget(self)
        listWidget.setViewMode(QListWidget.IconMode)
        listWidget.setFixedSize(500, 700)
        listWidget.setIconSize(QSize(100, 200))
        listWidget.setDragDropMode(listWidget.InternalMove)
        listWidget.setFocusPolicy(Qt.NoFocus) #Why no work?
        self.listWidget = listWidget

        '''json file contains positions of "outfield" players'''
        try:
            with open('players.txt', 'r') as file:
                data = json.load(file)
        except:
            data = []

        dir = 'Players/'

        for filename in os.listdir(dir):
            playersIndex = next((i for i, player in enumerate(data) if player['filename'] ==
                                 filename), None)
            playersIndex = None #Create button to reset @myself
            if playersIndex == None:
                item = QListWidgetItem(QIcon(dir + filename), filename, listWidget)
            else:
                pixmap = QPixmap(dir + filename).scaledToHeight(100, Qt.SmoothTransformation)
                label = MovableLabel(self, filename)
                label.setPixmap(pixmap)
                label.setFixedSize(pixmap.width(), pixmap.height())
                label.setParent(self)
                label.move(data[playersIndex]['x'], data[playersIndex]['y'])
                self.players.append(label)
        self.setStyleSheet("background-color: black;")
        self.showMaximized()
        self.setAcceptDrops(True)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with open('players.txt', 'w') as outfile:
            json.dump([{'filename': player.filename, 'x': player.x(), 'y': player.y()} for player in self.players],
                      outfile, indent= 4)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
