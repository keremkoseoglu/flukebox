""" Entry point """
from PyQt5.Qt import QApplication
from flukebox.gui.prime import Prime

APP = QApplication([])
P = Prime()
os._exit(APP.exec_()) # pylint: disable=W0212
