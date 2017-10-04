from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E

class Calculator(object):

    def __init__(self):
        self.total = 0

    def add(self, x):
        self.total += x

    def sub(self, x):
        self.total -= x

    def reset(self):
        self.total = 0

def test_Calculator():
    calc = Calculator()
    assert calc.total == 0
    calc.add(3)
    assert calc.total == 3
    calc.add(5)
    assert calc.total == 8
    calc.sub(7)
    assert calc.total == 1
    calc.sub(10)
    assert calc.total == -9
    calc.reset()
    assert calc.total == 0


class GUI(object):

    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        self.calculator = Calculator()

        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)

        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=W+E)
        self.update_total()

    def update_total(self):
        self.total_label_text.set(self.calculator.total)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            self.calculator.add(self.entered_number)
        elif method == "subtract":
            self.calculator.sub(self.entered_number)
        else: # reset
            self.calculator.reset()

        self.update_total()
        self.entry.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    my_gui = GUI(root)
    root.mainloop()
