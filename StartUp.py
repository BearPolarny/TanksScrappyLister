import tkinter as tk
from windows.MainWindow import MainWindow

if __name__ == '__main__':
    root = tk.Tk()
    window = MainWindow(root)
    window.run()
