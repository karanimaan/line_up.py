import sys

from PyQt5.QtWidgets import QApplication

import line_up

app = QApplication([])
window = line_up.MainWindow()
app.exec_()
