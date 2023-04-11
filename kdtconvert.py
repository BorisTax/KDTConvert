import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText
from tkinter import Scrollbar

from convertToXNC import convertToXNC
from convertToKDT import convertToKDT

class MyApp():

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('KDT конвертер')
        self.root.resizable(False, False)
        self.root.geometry('500x200')
        self.root.eval('tk::PlaceWindow . center')
        self.frame = ttk.Frame(self.root)
        self.open_xnc_button = ttk.Button(self.frame,
                                      text='Конвертировать XNC в KDT',
                                      command=self.select_file_xnc)
        self.open_xml_button = ttk.Button(self.frame,
                                      text='Конвертировать KDT в XNC',
                                      command=self.select_file_xml)
        self.help_button = ttk.Button(self.frame,
                                      text='?',
                                      width=3,
                                      command=self.help)
        h = Scrollbar(self.root, orient='horizontal')
        h.pack(side=tk.BOTTOM, fill='x')

        self.text = ScrolledText(wrap=tk.NONE, xscrollcommand=h.set)
        self.frame.pack()
        self.open_xnc_button.pack(side=tk.LEFT)
        self.open_xml_button.pack(side=tk.LEFT)
        self.help_button.pack(side=tk.RIGHT)
        self.text.pack(pady=5, padx=5)
        h.config(command=self.text.xview)
        self.root.mainloop()

    def select_file_xml(self):
        filetypes = (('файлы XML', '*.xml'), ('Все файлы', '*.*'))
        filenames = fd.askopenfilenames(title='Выбрать файлы',
                                        filetypes=filetypes)
        if len(filenames) == 0: return
        self.start(filenames, convertToXNC, 'xnc')

    def select_file_xnc(self):
        filetypes = (('файлы XNC', '*.xnc'), ('Все файлы', '*.*'))
        filenames = fd.askopenfilenames(title='Выбрать файлы',
                                        filetypes=filetypes)
        if len(filenames) == 0: return
        self.start(filenames, convertToKDT, 'xml')

    def help(self):
        message = 'Конвертер xml файлов в формате KDT в xnc шаблон Giblab. \nАвтор: Тахмазов Борис'
        tk.messagebox.showinfo(title='О программе', message=message)

    def start(self, filenames, func, ext):
        self.text.delete("1.0", "end")
        for filename in filenames:
            s = func(filename)
            if s == "":
                self.text.insert(
                    tk.INSERT,
                    os.path.basename(filename) +
                    ' - неправильный формат файла\n')
                print(f'{filename} - неправильный формат файла')
                continue
            file = os.path.splitext(filename)[0]
            with open(file + '.' + ext, 'w') as f:
                f.write(s)
            self.text.insert(tk.INSERT,
                             os.path.basename(file) + '.' + ext + ' - готово\n')
            #print(f'{filename} - готово')


MyApp()
