import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText
from tkinter import Scrollbar

from convert import convert



class MyApp():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('KDT конвертер')
        self.root.resizable(False, False)
        self.root.geometry('500x200')
        self.root.eval('tk::PlaceWindow . center')
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
        filetypes = (('файлы XML', '*.xml'), ('Все файлы', '*.*'))
        filenames = fd.askopenfilenames(title='Выбрать файлы', filetypes=filetypes)
        if len(filenames) == 0: return
        self.start(filenames)

    def start(self, filenames):
        self.text.delete("1.0","end")
        for filename in filenames:
            s = convert(filename)
            if s == "":
                self.text.insert(tk.INSERT,os.path.basename(filename)+' - неправильный формат файла\n')
                #print(f'{filename} - неправильный формат файла')
                continue
            file = filename.split(sep='.')[0]
            with open(file + '.xnc', 'w') as f:
                f.write(s)
            self.text.insert(tk.INSERT,os.path.basename(filename)+' - готово\n')
            #print(f'{filename} - готово')

MyApp()
