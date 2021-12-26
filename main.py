""" Entry point """
import os
import sys
from PyQt5.Qt import QApplication
from flukebox.gui.prime import Prime
from flukebox.production.producer import Producer
from flukebox.production.seeker import Seeker

def main():
    # Skippable hosts
    no_local = False
    arg_pos = -1
    for arg in sys.argv:
        if arg == "no_local":
            no_local = True

    # Scan for options
    arg_pos = -1
    for arg in sys.argv:
        arg_pos += 1
        if arg_pos == 0:
            continue
        arg_split = arg.split("=")
        if len(arg_split) < 2:
            continue
        if arg_split[0] == "playlist":
            Producer().produce_with_playlist(arg_split[1], no_local=no_local)
            return
        if arg_split[0] == "seek":
            Seeker().seek_and_produce(arg_split[1])
            return

    # GUI
    APP = QApplication([])
    P = Prime()
    os._exit(APP.exec_()) # pylint: disable=W0212

if __name__ == "__main__":
    main()
