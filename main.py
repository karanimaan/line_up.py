#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication

import line_up

app = QApplication([])
window = line_up.MainWindow()
app.exec_()
