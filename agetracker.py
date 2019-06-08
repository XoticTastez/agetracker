import os
from datetime import date
from dateutil.relativedelta import relativedelta
from csv import reader
import re

path = os.getenv('LOCALAPPDATA') + '\\AgeTracker'
os.makedirs(path, exist_ok=True)
path += '\\data.csv'
if not os.path.isfile(path):
    open(path, 'x')
today = date.today()
names = []
init = True

def show_list():
    global names, init
    for row in reader(open(path, newline='')):
        print(row[0])
        bd = date(int(row[1]), int(row[2]), int(row[3]))
        diff = relativedelta(today, bd)
        output = '  '
        if diff.years > 0:
            output += f'{diff.years}y  '
        if diff.months > 0:
            output += f'{diff.months}m  '
        if diff.weeks > 0:
            output += f'{diff.weeks}w  '
        days = diff.days
        if days >= 7:
            days -= diff.weeks * 7
        if days > 0 or bd >= today:
            output += f'{days}d'
        print(output)
        if init:
            names += [row[0]]
    else:
        init = False

show_list()
print("Enter '?' for help.")
while True:
    inp = input('> ').strip()
    if inp == '?':
        print("To add a new entry, enter '+' followed by the name.\nTo remove an existing entry, enter '-' followed by the name.\nNames are case-sensitive, and year of birth's millennium/century\nshould not be omitted ('19' equates to the year 19, not 2019).")
    elif len(inp) < 2:
        continue
    elif inp[0] == '+':
        name = inp[1:].strip()
        if name in names:
            print(f"'{name}' is already registered.")
            continue
        bd = None
        while True:
            inp = input('Date of Birth (Y-M-D): ').strip()
            if re.match('[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}', inp):
                y = int(inp[:inp.find('-')])
                inp = inp[inp.find('-')+1:]
                m = int(inp[:inp.find('-')])
                inp = inp[inp.find('-')+1:]
                d = int(inp)
                try:
                    bd = date(y, m, d)
                    if bd > today:
                        raise Exception
                    break
                except: pass
            print('Invalid date.')
        open(path, 'a').write(f'{name},{bd.year},{bd.month},{bd.day}\n')
        print(f"'{name}' has been added.")
        show_list()
        names += [name]
    elif inp[0] == '-':
        inp = inp[1:].strip()
        if inp in names:
            lines = []
            for row in open(path).readlines():
                if inp not in row:
                    lines += [row]
            open(path, 'w').writelines(lines)
            print(f"'{inp}' has been removed.")
            show_list()
            names.remove(inp)
    elif inp.lower() == 'credits':
        print("Code by Vesdii\nIcon by Smashicons at Flaticon\nCompiled with PyInstaller")