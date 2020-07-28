from PyQt5.QtWidgets import *
from view import View
from model import Model
import sys

qt_app = QApplication(sys.argv)
model = Model()
view = View(model)
view.showNormal()
qt_app.exec_()



