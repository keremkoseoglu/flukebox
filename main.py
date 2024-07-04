""" Entry point """

import sys
from flukebox.gui.prime import start_gui
from flukebox.production.seeker import Seeker


def main():
    """Main entry point"""
    # Skippable hosts
    no_local = False
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
            start_gui(playlist=arg_split[1], no_local=no_local)
            return
        if arg_split[0] == "seek":
            Seeker().seek_and_produce(arg_split[1])
            return

    # GUI
    # Seeker().seek_and_produce("/Users/Kerem/Downloads/flukebox_seek.json")
    start_gui()


if __name__ == "__main__":
    main()
