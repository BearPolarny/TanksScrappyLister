import tkinter as tk
import pygubu


class EditWindow:

    def save_func(self):

        # manual selection (3/3)
        if self.edited_value == 'Alias':
            new_alias = self.textbox.get('1.0', tk.END)[:-1]
            if self.selected_tank.alias:
                self.aliases[new_alias] = self.aliases[self.selected_tank.alias]
            else:
                self.aliases[new_alias] = self.aliases[self.selected_tank.name]
            if self.selected_tank.name in self.aliases.keys():
                self.aliases.pop(self.selected_tank.name)
            if self.selected_tank.alias in self.aliases.keys():
                self.aliases.pop(self.selected_tank.alias)
            self.selected_tank.alias = new_alias

        elif self.edited_value == 'Name':
            new_name = self.textbox.get('1.0', tk.END)[:-1]

            if not self.selected_tank.alias:
                self.aliases[new_name] = self.aliases[self.selected_tank.name]
                self.aliases.pop(self.selected_tank.name)
            self.selected_tank.name = new_name

        elif self.edited_value == 'Final':
            self.selected_tank.final = self.textbox.get('1.0', tk.END)[:-1]
        else:
            self.selected_tank.chapters[self.edited_value] = self.textbox.get('1.0', tk.END)[:-1]

    def exit_func(self):
        self.main_window.destroy()

    def onselect_tank(self, evt):
        w = evt.widget
        try:
            # position and tank under selection

            index = int(w.curselection()[0])
            value = w.get(index)

            self.textbox.delete('1.0', tk.END)
            tank = self.tanks[self.aliases[value]]

            names = [len(value) for value in tank.chapters.keys()]
            # print(names)
            names.append(len('Turystyczny'))
            self.listbox_info.delete(0, tk.END)
            self.listbox_info.configure(width=max(names))

            self.selected_tank = tank

            # Manually add positions (1/3)
            self.listbox_info.insert(1, 'Alias')
            self.listbox_info.insert(2, 'Name')
            self.listbox_info.insert(3, 'Final')

            # Add tanks values to list (1.5/3)
            for k, v in enumerate(tank.chapters.keys()):
                self.listbox_info.insert(k + 4, v)

            al = self.selected_tank.alias if self.selected_tank.alias else self.selected_tank.name
            self.title.set('Tank: {}, Value: '.format(al))

        except IndexError:
            print('pff')

    def onselect_info(self, event):
        w = event.widget

        try:
            # position and value under selection
            index = int(w.curselection()[0])
            value = w.get(index)

            self.textbox.delete('1.0', tk.END)
            self.edited_value = value

            # alias for title update
            al = self.selected_tank.alias if self.selected_tank.alias else self.selected_tank.name

            # Selecting correct value from tank
            # manual section (2/3):
            if value == 'Alias':
                if self.selected_tank.alias:
                    self.textbox.insert(
                        tk.END, str(self.selected_tank.alias))
            elif value == 'Name':
                self.textbox.insert(
                    tk.END, self.selected_tank.name
                )
            elif value == 'Final':
                self.textbox.insert(tk.END,
                                    "Data not final, to set as final save this field as tank's alias")
            # automatic section
            else:
                if a := self.selected_tank.chapters[self.edited_value]:
                    self.textbox.insert(
                        tk.END, a)

            self.title.set('Tank: {}, Value: {}'.format(al, value))
        except IndexError:
            pass

    def __init__(self, tanks, aliases):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('GUIs/edit_window.ui')
        self.main_window = builder.get_object('edit_window')
        builder.connect_callbacks(self)

        self.listbox_tanks = builder.get_object('listbox_tanks')
        self.listbox_info = builder.get_object('listbox_info')
        self.textbox = builder.get_object('textbox_info')
        label = self.builder.get_object('Label_1')

        self.listbox_tanks.bind('<<ListboxSelect>>', self.onselect_tank)
        self.listbox_info.bind('<<ListboxSelect>>', self.onselect_info)

        self.tanks = tanks
        self.aliases = aliases
        self.edited_value = None
        self.selected_tank = None

        names = [len(tank.alias if tank.alias else tank.name)
                 for tank in tanks.values()]
        names.append(len('Turystyczny'))
        self.listbox_tanks.configure(width=max(names))

        for k, v in enumerate(self.tanks.values()):
            if v.alias:
                self.listbox_tanks.insert(k + 1, v.alias)
            else:
                self.listbox_tanks.insert(k + 1, v.name)

        self.title = tk.StringVar()
        self.title.set('Tank: , Value: ')
        label.configure(textvariable=self.title)
