import os
from convert import convert

for filename in os.listdir():
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
#filename = "650x600-dno-90.xml"
