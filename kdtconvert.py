import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText
from tkinter import Scrollbar

from convert import convert

def start(filenames):
    for filename in filenames:
        if filename.endswith('.xml'):
            s = convert(filename)
            if s == "":
                print(f'{filename} - неправильный формат файла')
                continue
            file = filename.split(sep='.')[0]
            with open(file + '.xnc', 'w') as f:
                f.write(s)
            print(f'{filename} - готово')
    input('Нажмите любую клавишу...')

class MyApp():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('KDT конвертер')
        self.root.resizable(False, False)
        self.root.geometry('300x150')
        self.open_button = ttk.Button(
            self.root,
            text='Выбрать файлы',
            command=self.select_file
        )
        h=Scrollbar(self.root, orient='horizontal')
        h.pack(side=tk.BOTTOM, fill='x')

        self.text = ScrolledText(wrap = tk.NONE, xscrollcommand = h.set)
        self.open_button.pack()
        self.text.pack(pady = 5, padx = 5)
        h.config(command = self.text.xview)
        self.root.mainloop()

    def select_file(self):
        filetypes = (
            ('файлы XML', '*.xml'),
            ('Все файлы', '*.*')
        )

        filenames = fd.askopenfilenames(
            title='Выбрать файлы',
            filetypes=filetypes)
        self.text.delete("1.0","end")
        
        for fname in filenames:
            self.text.insert(tk.INSERT,os.path.basename(fname)+'\n')

MyApp()
