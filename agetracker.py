import os
from datetime import date
from dateutil.relativedelta import relativedelta
import re

path = os.getenv('LOCALAPPDATA') + '\\AgeTracker'
os.makedirs(path, exist_ok=True)
path += '\\data.csv'
if not os.path.isfile(path):
    open(path, 'x').close()
today = date.today()
names = []

def show_list():
    init = True if not names else False
    print()
    with open(path) as file:
        for row in file:
            row = row.split(',')
            row[3] = row[3].strip()
            print(f'{row[0]}  ({row[1]}-{row[2]}-{row[3]})')
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
                names.append(row[0])
    print()

# The default parsing for dates is not very user-friendly, so: Improvise. Adapt. Overcome.
def parse_bd():
    while True:
        inp = input('Date of Birth (Y-M-D): ').strip()
        if inp.lower() == 'cancel':
            return None
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
                return bd
            except: pass
        print('Invalid date.')

show_list()
print("Enter '?' for help.")
while True:
    inp = input('> ').strip()
    # Help
    if inp == '?':
        print("To add a new entry, enter '+' followed by the name.\nTo remove an existing entry, enter '-' followed by the name.\nNames are case-sensitive, and year of birth's millennium/century\nshould not be omitted ('19' equates to the year 19, not 2019).\nTo abort date of birth entry, enter 'cancel'.")
    elif len(inp) < 2:
        continue
    # Add
    elif inp[0] == '+':
        name = inp[1:].strip()
        if name in names:
            print(f"'{name}' is already registered.")
            continue
        if ',' in name:
            print('Name cannot contain commas.')
            continue
        bd = parse_bd()
        if not bd:
            continue
        with open(path, 'a') as file:
            file.write(f'{name},{bd.year},{bd.month},{bd.day}\n')
        print(f"'{name}' has been added.")
        show_list()
        names.append(name)
    # Remove
    elif inp[0] == '-':
        inp = inp[1:].strip()
        if inp in names:
            lines = []
            with open(path) as file:
                for row in file:
                    if inp != row.split(',',1)[0]:
                        lines.append(row)
            with open(path, 'w') as file:
                file.writelines(lines)
            print(f"'{inp}' has been removed.")
            show_list()
            names.remove(inp)
    # Credits
    elif inp.lower() == 'credits':
        print("Code by Vesdii\nIcon by Smashicons at Flaticon\nCompiled with PyInstaller")
