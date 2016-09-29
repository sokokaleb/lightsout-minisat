from Tkinter import *
import ttk

from src.util.board_configuration import BoardConfiguration

class LightsOutGUI(object):
    def __init__(self, minisat_wrapper=None):
        if minisat_wrapper is None:
            raise Exception('minisat_wrapper should be filled!')
        self.minisat_wrapper = minisat_wrapper
        self.board_config = BoardConfiguration(3, 3)

    def run(self):
        print 'I\'m running!' # Erase this once the function is implemented
        root = Tk()
        
        content = ttk.Frame(root)

        content.grid(column=0, row=0)

        root.mainloop()
