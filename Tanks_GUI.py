#!/usr/bin/env python
# coding: utf-8

# In[9]:


import tkinter as tk
import tkinter.ttk
import pygubu.builder.ttkstdwidgets
import tkinter.messagebox as msg
import pygubu
import pickle
from Scrapper import scrapper
from Tank import tank_factory
from urllib.error import HTTPError
import os.path


# In[12]:


class NotATankException(Exception):
    pass


class AddWindow:

    def exit_func(self):
        self.main_window.destroy()

    def add_func(self):
        try:
            for tank in self.tanks_to_save:
                if tank not in self.tanks:
                    self.tanks[tank.name] = tank
            name = self.tanks[self.tanks_to_save[-1].name].name

            for t in self.tanks.values():
                if t.name not in self.aliases.values():
                    if t.alias:
                        self.aliases[t.alias] = t.name
                    else:
                        self.aliases[t.name] = t.name
            if name:
                msg.showinfo("Added", "Dodano czolg {}, gratki".format(name))
        except TypeError:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, "There is no tank to add")
            self.textbox.configure(state=tk.DISABLED)
        except IndexError:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, "Url was correct, but wiki infobox wasn't found\n"
                                        "Are you sure you used URL to tank wikipage?")
            self.textbox.configure(state=tk.DISABLED)

    def download_data_func(self):
        entry = self.builder.get_object("Entry_1")
        url_end = entry.get()
        try:
            boxs = scrapper(url_end)
            tnks = tank_factory(boxs, url_end)
            for t in tnks:
                if t.type.find('tank') == -1:
                    raise NotATankException

            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            #             print(value)
            tank_string = ""
            i = 1
            if len(tnks) > 1:
                tank_string = "Warning! More than one tank\nYou will be saving both!\n\n"
            for tank in tnks:
                tank_string += 'Tank no.{}:\n'.format(i)
                tank_string += tank.show_all()
                i += 1

            self.textbox.insert(tk.END, tank_string)
            self.textbox.configure(state=tk.DISABLED)
            self.tanks_to_save = tnks
        except HTTPError:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, "Bad URL\n"
                                        "https://en.wikipedia.org/wiki/{} is not correct".format(url_end))
            self.textbox.configure(state=tk.DISABLED)
        except NotATankException:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, "This probably isn't a tank")
            self.textbox.configure(state=tk.DISABLED)
    def __init__(self, tanks, alias):
        super().__init__()
        self.tanks_to_save = None
        self.tanks = tanks
        self.aliases = alias
        self.builder = builder = pygubu.Builder()
        builder.add_from_file("GUIs/add_window.ui")
        self.main_window = builder.get_object('add_window')

        builder.connect_callbacks(self)
        self.textbox = builder.get_object("Text_1")
        self.textbox.insert(tk.END, "Enter end of URL to english wikipedia\n"
                                    "page of tank you desire\n"
                                    "E.g. for Panzer I enter: \n"
                                    "Panzer_I")
        self.textbox.configure(state=tk.DISABLED)


# In[5]:


class EditWindow:

    def save_func(self):

        if self.edited_value == 'Alias':
            self.selected_tank.alias = self.textbox.get('1.0', tk.END)[:-1]
            for t in self.tanks.values():
                if t.alias:
                    self.aliases[t.alias] = t.name
                else:
                    self.aliases[t.name] = t.name
        else:
            self.selected_tank.chapters[self.edited_value] = self.textbox.get('1.0', tk.END)[:-1]

    def exit_func(self):
        self.main_window.destroy()

    def onselect_tank(self, evt):
        w = evt.widget
        try:
            index = int(w.curselection()[0])

            value = w.get(index)
            self.textbox.delete('1.0', tk.END)
            tank = self.tanks[self.aliases[value]]

            names = [len(value) for value in tank.chapters.keys()]
            # print(names)
            self.listbox_info.delete(0, tk.END)
            self.listbox_info.configure(width=max(names))

            self.selected_tank = tank
            self.listbox_info.insert(1, "Alias")

            for k, v in enumerate(tank.chapters.keys()):
                self.listbox_info.insert(k + 2, v)

            al = self.selected_tank.alias if self.selected_tank.alias else self.selected_tank.name
            self.title.set("Tank: {}, Value: ".format(al))

        except IndexError:
            print('pff')

    def onselect_info(self, event):
        w = event.widget

        try:
            index = int(w.curselection()[0])

            value = w.get(index)
            self.textbox.delete('1.0', tk.END)
            self.edited_value = value
            al = self.selected_tank.alias if self.selected_tank.alias else self.selected_tank.name
            if value == 'Alias':
                self.textbox.insert(
                    tk.END, self.selected_tank.alias)
            else:
                self.textbox.insert(
                    tk.END, self.selected_tank.chapters[self.edited_value])

            self.title.set("Tank: {}, Value: {}".format(al, value))
        except IndexError:
            pass

    def __init__(self, tanks, aliases):
        self.tanks = tanks
        self.aliases = aliases
        self.edited_value = None
        self.selected_tank = None

        self.builder = builder = pygubu.Builder()

        builder.add_from_file('GUIs/edit_window.ui')

        self.main_window = builder.get_object('edit_window')
        builder.connect_callbacks(self)
        self.listbox_tanks = builder.get_object('listbox_tanks')
        names = [len(tank.alias if tank.alias else tank.name)
                 for tank in tanks.values()]
        self.listbox_tanks.configure(width=max(names))

        for k, v in enumerate(self.tanks.values()):
            if v.alias:
                self.listbox_tanks.insert(k + 1, v.alias)
            else:
                self.listbox_tanks.insert(k + 1, v.name)

        self.listbox_info = builder.get_object('listbox_info')
        self.listbox_tanks.bind('<<ListboxSelect>>', self.onselect_tank)
        self.listbox_info.bind('<<ListboxSelect>>', self.onselect_info)

        self.textbox = builder.get_object('textbox_info')
        self.title = tk.StringVar()
        self.title.set('Tank: , Value: ')
        label = self.builder.get_object('Label_1')
        label.configure(textvariable=self.title)


# In[6]:


class ListWindow:

    def remove_func(self):
        # dict().pop
        try:
            self.tanks.pop(self.selected_tank.name)
        except KeyError:
            pass
        self.update_list()

    def onselect(self, event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            #             print(value)
            self.selected_tank = self.tanks[self.aliases[value]]
            tank_string = self.selected_tank.show_all()
            self.textbox.insert(tk.END, tank_string)
            self.textbox.configure(state=tk.DISABLED)
        except IndexError:
            pass

    def back_func(self):
        self.main_window.destroy()

    def __init__(self, tanks, aliases):
        self.selected_tank = None
        self.tanks = tanks
        self.aliases = aliases

        self.builder = builder = pygubu.Builder()

        builder.add_from_file('GUIs/list_window.ui')

        self.main_window = builder.get_object('list_of_tanks')

        builder.connect_callbacks(self)

        self.textbox = builder.get_object('text_tank_specs')
        self.listbox = builder.get_object('listbox_tanks')

        self.listbox.bind('<<ListboxSelect>>', self.onselect)

        self.update_list()

    def update_list(self):
        self.listbox.delete(0, tk.END)
        names = [len(tank.alias if tank.alias else tank.name)
                 for tank in self.tanks.values()]
        self.listbox.configure(width=max(names))

        for k, v in enumerate(self.tanks.values()):
            if v.alias:
                self.listbox.insert(k + 1, v.alias)
            else:
                self.listbox.insert(k + 1, v.name)


# In[7]:


class MainWindow:

    def save_func(self):
        pickle.dump(self.tanks, open('tank_data/tanksGUI.p', 'wb'))

    def exit_func(self):
        self.root.destroy()

    def edit_func(self):
        EditWindow(self.tanks, self.aliases)

    def add_func(self):
        # self.label.grid_forget()
        AddWindow(self.tanks, self.aliases)

    def compare_func(self):
        pass

    def list_func(self):
        ListWindow(self.tanks, self.aliases)

    # noinspection PyShadowingNames
    def __init__(self, root):
        self.root = root
        # tanks = dict()
        try:
            if tanks := pickle.load(open('tank_data/tanksGUI.p', 'rb')):
                # if tanks:= pickle.load(open('tank_data/tanks.p', 'rb')):
                for t in tanks.values():
                    if t.alias:
                        # print(t.alias)
                        pass
                    else:
                        # print(t.name)
                        pass
        except FileNotFoundError:
            print(os.path.curdir)

        self.builder = builder = pygubu.Builder()

        builder.add_from_file('GUIs/mainwindow.ui')

        self.main_window = builder.get_object('mainwindow')

        # callbacks = {
        #     'add_func': self.add_func,
        #     'compare_func': self.compare_func,
        #     'list_func': self.list_func
        # }

        builder.connect_callbacks(self)

        self.label = builder.get_object('label_title')
        self.label.configure(text="Tanks explorer v0.1.1")

        self.tanks = tanks

        self.aliases = dict()
        for t in self.tanks.values():
            if t.alias:
                self.aliases[t.alias] = t.name
            else:
                self.aliases[t.name] = t.name

        # but_add = builder.get_object('button_add')
        # but_add.configure(state=tk.DISABLED)
        but_comp = builder.get_object('button_compare')
        but_comp.configure(state=tk.DISABLED)

    def run(self):
        self.main_window.mainloop()

# In[15]:
