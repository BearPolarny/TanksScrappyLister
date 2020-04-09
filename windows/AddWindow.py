import tkinter as tk
import pygubu

from urllib.error import HTTPError
from Scrapper import scrapper
from Tank import tank_factory


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

            for t in self.tanks.values():
                if t.name not in self.aliases.values():
                    if t.alias:
                        self.aliases[t.alias] = t.name
                    else:
                        self.aliases[t.name] = t.name

            for tank in self.tanks.values():
                for nkey in self.non_keys:
                    if nkey not in tank.chapters.keys():
                        tank.chapters[nkey] = 'missing data'

        except TypeError:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, 'There is no tank to add')
            self.textbox.configure(state=tk.DISABLED)
        except IndexError:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, "Url was correct, but wiki infobox wasn't found\n"
                                        "Are you sure you used URL to tank wikipage?")
            self.textbox.configure(state=tk.DISABLED)
        finally:
            self.main_window.bind('<Return>', lambda event: self.download_data_func())

    def download_data_func(self):

        url_end = self.entry.get()
        try:
            boxes = scrapper(url_end)
            tanks, self.non_keys = tank_factory(boxes, url_end)

            for t in tanks:
                if t.type.find('tank') == -1:
                    raise NotATankException

            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)

            tank_string = ''
            i = 1
            if len(tanks) > 1:
                tank_string = 'Warning! More than one tank\nYou will be saving both!\n\n'
            for tank in tanks:
                tank_string += 'Tank no.{}:\n'.format(i)
                tank_string += tank.show_all()
                i += 1

            self.textbox.insert(tk.END, tank_string)
            self.textbox.configure(state=tk.DISABLED)
            self.tanks_to_save = tanks
        except HTTPError:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, 'Bad URL\n'
                                        'https://en.wikipedia.org/wiki/{} is not correct'.format(url_end))
            self.textbox.configure(state=tk.DISABLED)
        except NotATankException:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, "This probably isn't a tank")
            self.textbox.configure(state=tk.DISABLED)
        # except (TimeoutError, URLError):
        #     self.textbox.configure(state=tk.NORMAL)
        #     self.textbox.delete('1.0', tk.END)
        #     self.textbox.insert(tk.END, "Timeout")
        #     self.textbox.configure(state=tk.DISABLED)
        except TypeError:
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete('1.0', tk.END)
            self.textbox.insert(tk.END, "Nothing was collected. \nYou got internet error, didn't ya?")
            self.textbox.configure(state=tk.DISABLED)
        finally:
            self.main_window.bind('<Return>', lambda event: self.add_func())

    def __init__(self, tanks, alias):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('GUIs/add_window.ui')
        self.main_window = builder.get_object('add_window')
        builder.connect_callbacks(self)

        self.textbox = builder.get_object('Text_1')
        self.entry = self.builder.get_object('Entry_1')

        self.tanks_to_save = None
        self.tanks = tanks
        self.aliases = alias
        self.non_keys = set()

        self.entry.focus_set()
        self.entry.bind('<Return>', lambda event: self.download_data_func())

        self.textbox.insert(tk.END, 'Enter end of URL to english Wikipedia\n'
                                    'page of tank you desire\n'
                                    'E.g. for Panzer I enter: \n'
                                    'Panzer_I')
        self.textbox.configure(state=tk.DISABLED)
