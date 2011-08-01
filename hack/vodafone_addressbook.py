#!/usr/bin/env python
"""
Automatic management of the address book of the italian "Vodafone Widget"

Requirements
------------

$ pip install autopy
$ pip install wmctrl

Usage
-----

$ python vodafone_rubrica.py rubrica.txt

rubrica.txt is a file with this format:

name +39123456789 *
name +39987654321
...

only the lines ending with * will be imported
"""

import sys
import time
import autopy
from wmctrl import Window

SLEEP=0.1

BOOK_GREY = 10592673
BOOK_RED = 16731469
DELETE_WHITE = 16777215
DELETE_GREY = 9605778
DELETE_RED = 16725301

class Point(tuple):

    def get_color(self):
        return autopy.screen.get_color(*self)

    def move(self):
        if Window.get_active().id != MAIN_WINDOW.id:
            print >> sys.stderr, 'Lost focus, exiting'
            sys.exit(1)
        autopy.mouse.move(*self)

    def click(self, t=SLEEP):
        self.move()
        autopy.mouse.click()
        time.sleep(t)

    def type(self, s):
        self.click()
        for ch in s:
            if 'A' <= ch <= 'z':
                autopy.key.tap(ch)
            else:
                autopy.key.tap(ord(ch))
        time.sleep(SLEEP)


class AddressBook(object):

    cmd_toggle = Point((217, 185))
    cmd_new_entry = Point((235, 206))
    txt_name = Point((20, 208))
    txt_number = Point((133, 208))
    cmd_save = Point((225, 208))
    cmd_delete_first = Point((232, 224))
    cmd_delete_yes = Point((195, 260))

    def toggle_if(self, expected_color):
        color = self.cmd_toggle.get_color()
        if color == expected_color:
            self.cmd_toggle.click()
            return True
        return False

    def open(self):
        return self.toggle_if(expected_color=BOOK_GREY)

    def close(self):
        return self.toggle_if(expected_color=BOOK_RED)

    def clear(self):
        self.open()
        last_delete = time.time()
        while True:
            self.cmd_delete_first.move()
            color = self.cmd_delete_first.get_color()
            if color == DELETE_WHITE:
                if time.time() - last_delete > 2:
                    break
                time.sleep(0.1)
            elif color in (DELETE_RED, DELETE_GREY):
                self.cmd_delete_first.click()
                self.cmd_delete_yes.click(0.5)
                last_delete = time.time()

    def add_entry(self, name, number):
        was_closed = self.open()
        self.cmd_new_entry.click()
        self.txt_name.type(name)
        self.txt_number.type(number)
        self.cmd_save.click()
        if was_closed:
            self.close()

def reposition_window():
    wins = Window.by_name_endswith('Widget vodafone.it')
    assert len(wins) == 1
    win = wins[0]
    win.resize_and_move(0, 0, win.w, win.h)
    win.activate()
    return win

def import_from_file(fname):
    f = open(fname)
    for line in f:
        if '*' not in line:
            continue
        name, number, vodafone = line.rsplit(None, 2)
        if number.startswith('+393') and not name.startswith('zz'):
            number = number[3:]
            yield name, number

def main():
    book = AddressBook()
    book.clear()
    book.open()
    for name, number in import_from_file(sys.argv[1]):
        book.add_entry(name, number)
        print name, number
    book.close()

if __name__ == '__main__':
    MAIN_WINDOW = reposition_window()
    main()
    
