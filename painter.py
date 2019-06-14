import sys
import gui
import cmd

if (sys.argv[1]=="-gui"):
    gui.gui()
elif (sys.argv[1]=="-cmd"):
    cmd.cmd(sys.argv[2])
else:
    print("Warn Usage, See: python3 painter.py [option:gui/cmd] [file]")

