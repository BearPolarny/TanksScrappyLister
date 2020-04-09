import os.path
import pickle
import pygubu
import pygubu.builder.ttkstdwidgets
from windows import *


class MainWindow:

    def save_func(self):
        with open(os.path.abspath(os.curdir) + '/tank_data/tanksGUI.p', 'wb') as file:
            pickle.dump(self.tanks, file)

    def exit_func(self):
        self.root.destroy()

    def edit_func(self):
        EditWindow(self.tanks, self.aliases)

    def add_func(self):
        AddWindow(self.tanks, self.aliases)

    def compare_func(self):
        CompWindow(self.tanks, self.aliases)

    def list_func(self):
        ListWindow(self.tanks, self.aliases)

    def __init__(self, root):
        self.root = root
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('GUIs/main_window.ui')
        self.main_window = builder.get_object('main_window')
        builder.connect_callbacks(self)
        self.label = builder.get_object('label_title')

        try:
            tanks = pickle.load(open(os.path.abspath(os.curdir) + '/tank_data/tanksGUI.p', 'rb'))
        except FileNotFoundError:
            tanks = {}
            print(os.path.curdir)
        self.tanks = tanks
        self.aliases = dict()

        for t in self.tanks.values():
            if t.alias:
                self.aliases[t.alias] = t.name
            else:
                self.aliases[t.name] = t.name

        self.label.configure(text='Tanks explorer v0.4')
        self.root.title('TankExplorer')

    def run(self):
        self.main_window.mainloop()
