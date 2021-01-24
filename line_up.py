import json
import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QVBoxLayout, QWidget

from MovableLabel import MovableLabel
from MyListWidget import MyListWidget


# noinspection PyTypeChecker
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        listWidget = MyListWidget(self)
        listWidget.setFixedSize(500, 600)
        self.listWidget = listWidget

        subsListWidget = MyListWidget(self)
        subsListWidget.setFixedSize(650, 100)
        subsListWidget.verticalScrollBar().setDisabled(True)
        subsListWidget.maximumItems = 7
        self.subsListWidget = subsListWidget

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.subsListWidget)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.centralWidget = centralWidget

        self.setCentralWidget(self.centralWidget)

        '''json file contains positions of "outfield" players'''
        players = playersFilenames = subs = []
        try:
            with open('players.txt', 'r') as file:
                data = json.load(file)
                players = data['players']
                playersFilenames = [player['filename'] for player in players]
                subs = data['subs']
        except:
            pass

        images_directory = 'Players/'
        subs_list = [None] * 7
        index = -1

        for filename in os.listdir(images_directory):
            if filename == 'p95658.png':  # Maguire
                self.setWindowIcon(QIcon(images_directory + filename))
            for group in playersFilenames, subs:
                try:
                    index = group.index(filename)
                    break
                except ValueError:
                    pass
            else:
                group = None

            if group is playersFilenames:
                label = MovableLabel(self, filename)
                label.move(players[index]['x'], players[index]['y'])
            else:
                item = QListWidgetItem(QIcon(images_directory + filename), '')
                item.filename = filename
                if group is subs:
                    subs_list.insert(index, item)
                else:
                    listWidget.addItem(item)
        for sub in subs_list:
            if sub is not None:
                subsListWidget.addItem(sub)

        # self.setStyleSheet("background-color: black;")
        # self.setAcceptDrops(True)
        self.showMaximized()
        self.setWindowTitle('Team Maguinya')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with open('players.txt', 'w') as outfile:
            player: MovableLabel
            players = [{'filename': player.filename, 'x': player.x(), 'y': player.y()} for player in
                       self.findChildren(MovableLabel)]
            sub: QListWidgetItem
            subs = [sub.filename for sub in self.subsListWidget.findItems('*', Qt.MatchWildcard)]
            json.dump({'players': players, 'subs': subs}, outfile, indent=4)
