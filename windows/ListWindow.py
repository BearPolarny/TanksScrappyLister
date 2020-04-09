import pygubu
import tkinter as tk


class _ImportPopup:
    def exit_func(self):
        self.main_window.destroy()

    def yesman(self):
        from Scrapper import scrapper
        from Tank import tank_factory

        tanks_to_scrap = ['Panzer_I', 'Panzer_II', 'Panzer_III', 'Panzer_IV', 'Panther_tank', 'Tiger_I']
        # tanks_to_scrap_short = ['Panzer_I', 'Panzer_II']
        try:
            for url in tanks_to_scrap:
                boxes = scrapper(url)
                tanks, _ = tank_factory(boxes, url)
                for t in tanks:
                    self.tanks[t.name] = t
                    self.aliases[t.name] = t.name
        except TypeError:
            pass
        finally:
            self.parent.update_list()
            self.exit_func()

    def __init__(self, tanks, aliases, parent):
        """

        :param dict tanks:
        :param dict aliases:
        :param ListWindow parent:
        """
        self.parent = parent
        self.ready = False
        self.tanks = tanks
        self.aliases = aliases
        builder = pygubu.Builder()
        builder.add_from_file('GUIs/import.ui')
        self.main_window = builder.get_object('import')
        builder.connect_callbacks(self)
        self.main_window.protocol('WM_DELETE_WINDOW', self.exit_func)


class ListWindow:

    def remove_func(self):

        try:
            self.tanks.pop(self.selected_tank.name)
            self.aliases.pop(self.selected_tank.alias)
        except KeyError:
            pass
        self.update_list()
        self.textbox.configure(state=tk.NORMAL)
        self.textbox.delete('1.0', tk.END)
        self.textbox.configure(state=tk.DISABLED)

    def onselect(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.selected_tank = self.tanks[self.aliases[value]]
            tank_string = self.selected_tank.show_all()
            self.textbox.insert(tk.END, tank_string)
            self.textbox.configure(state=tk.DISABLED)
        except IndexError:
            pass

    def back_func(self):
        self.main_window.destroy()
        try:
            self.a.main_window.destroy()
        except AttributeError:
            pass

    def __init__(self, tanks, aliases):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('GUIs/list_window.ui')
        self.main_window = builder.get_object('list_of_tanks')
        builder.connect_callbacks(self)

        self.textbox = builder.get_object('text_tank_specs')
        self.listbox = builder.get_object('listbox_tanks')

        self.selected_tank = None
        self.tanks = tanks
        self.aliases = aliases

        if len(tanks):
            self.update_list()
        else:
            self.a = _ImportPopup(self.tanks, self.aliases, self)

        self.listbox.bind('<<ListboxSelect>>', self.onselect)

    def update_list(self):
        """ Updating list of tanks after deletion so it won't show deleted entry"""
        self.listbox.delete(0, tk.END)
        names = [len(tank.alias if tank.alias else tank.name)
                 for tank in self.tanks.values()]
        names.append(len('Turystyczny'))
        self.listbox.configure(width=max(names))

        for k, v in enumerate(self.tanks.values()):
            if v.alias:
                self.listbox.insert(k + 1, v.alias)
            else:
                self.listbox.insert(k + 1, v.name)
