from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QGridLayout, QLabel, QWidget

app = QApplication([])
widget = QWidget()
listWidget = QListWidget()
item = QListWidgetItem('Pogba', listWidget)
pixmap = item.icon().pixmap(500, 500)

layout = QGridLayout()
label = QLabel(widget)
label.setPixmap(pixmap)
label.setFixedSize(500, 500)
layout.addWidget(listWidget)

palette = QPalette()
palette.setColor(QPalette.Highlight, listWidget.palette().color(QPalette.Base))
palette.setColor(QPalette.HighlightedText, listWidget.palette().color(QPalette.Text))
listWidget.setPalette(palette)

widget.setLayout(layout)

widget.show()
app.exec()