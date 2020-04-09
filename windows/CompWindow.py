import tkinter as tk
import pygubu


class CompWindow:

    def exit_func(self):
        self.main_window.destroy()

    def tank_pop(self, event):
        widget = event.widget
        try:
            index = int(widget.curselection()[0])
            value = widget.get(index)
            selected_tank = self.tanks[self.aliases[value]]
            _PopTank(selected_tank)
        except IndexError:
            pass

    def __init__(self, tanks, aliases):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('GUIs/comp_window.ui')
        self.main_window = builder.get_object('comp_window')
        builder.connect_callbacks(self)

        listbox = builder.get_object('Listbox_2')

        self.tanks = tanks
        self.aliases = aliases

        listbox.bind('<<ListboxSelect>>', self.tank_pop)

        for k, v in enumerate(self.tanks.values()):
            if v.alias:
                listbox.insert(k + 1, v.alias)
            else:
                listbox.insert(k + 1, v.name)


class _PopTank:

    def __init__(self, tank):
        build = pygubu.Builder()
        build.add_from_file('GUIs/pop_tank.ui')
        build.get_object('pop_tank')
        text = build.get_object('text')

        tank_string = tank.show_all()
        text.insert(tk.END, tank_string)
        text.configure(state=tk.DISABLED)
