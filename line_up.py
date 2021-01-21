import json
import os
import sys

from PyQt5 import QtGui
from PyQt5.Qt import QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem

from MovableLabel import MovableLabel
from MyListWidget import MyListWidget


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        listWidget = MyListWidget()
        listWidget.setViewMode(QListWidget.IconMode)
        listWidget.setIconSize(QSize(79, 100))
        listWidget.setFixedSize(500, 700)
        listWidget.setDragDropMode(listWidget.InternalMove)
        listWidget.setParent(self)

        '''json file contains positions of "outfield" players'''
        try:
            with open('players.txt', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        images_directory = 'Players/'

        for filename in os.listdir(images_directory):
            playersIndex = next((i for i, player in enumerate(data) if player['filename'] ==
                                 filename), None)

            if playersIndex is None:
                item = QListWidgetItem(QIcon(images_directory + filename), '', listWidget)
                item.filename = filename
            else:
                pixmap = QPixmap(images_directory + filename).scaledToHeight(100, Qt.SmoothTransformation)
                label = MovableLabel(self, filename)
                label.setPixmap(pixmap)
                label.setFixedSize(pixmap.width(), pixmap.height())
                label.setParent(self)
                label.move(data[playersIndex]['x'], data[playersIndex]['y'])

        # self.setStyleSheet("background-color: black;")
        self.showMaximized()
        self.setAcceptDrops(True)
        self.listWidget = listWidget

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with open('players.txt', 'w') as outfile:
            player: MovableLabel
            json.dump([{'filename': player.filename, 'x': player.x(), 'y': player.y()} for player in
                       self.findChildren(MovableLabel)],
                      outfile, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
