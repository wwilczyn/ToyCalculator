import tkinter as tk
import tkinter.messagebox


class CalculatorButton(tk.Button):
    """A button with callback, to be used with a CalculatorGrid widget."""

    def __init__(self, master, callback=None, **kwargs):
        self.callback = callback
        super().__init__(master, **kwargs)
        self.config(command=self.on_click)

    def on_click(self):
        if self.callback:
            self.callback(self['text'])


class CopyLabel(tk.Label):
    """A label that allows copying its text to the clipboard."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Bind the double-click event to out on_copy method
        self.bind('<Double-Button-1>', self.on_copy)

    def on_copy(self, event):
        self.clipboard_clear()
        self.clipboard_append(self['text'])
        tk.messagebox.showinfo('Clipboard', 'text copied')


class CalculatorGrid(tk.Frame):
    """A tkinter Frame that displays buttons and implements a simple calculator."""

    keys = [[('C', 1), ('CE', 1)],
            [('7', 1), ('8', 1), ('9', 1), ('+', 1)],
            [('4', 1), ('5', 1), ('6', 1), ('-', 1)],
            [('1', 1), ('2', 1), ('3', 1), ('*', 1)],
            [('0', 1), ('=', 2), ('/', 1)],
            ]

    # allowed_chars = [key[0] for key_row in keys for key in key_row]

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        max_columns = max(len(row) for row in CalculatorGrid.keys)
        self.result = CopyLabel(self, borderwidth=2, relief='sunken', anchor='w', bg='white')
        self.result.grid(row=0, column=0, columnspan=max_columns, sticky="nsew")

        # Add the buttons
        keypad = tk.Frame(self)
        keypad.grid(row=1, column=0, sticky='nsew')

        row = 0
        for key_row in CalculatorGrid.keys:
            col = 0
            for key in key_row:
                btn = CalculatorButton(keypad, text=key[0], width=2,
                                       callback=self.on_click)
                btn.grid(row=row, column=col, columnspan=key[1], sticky=tk.E + tk.W)
                col += key[1]
            row += 1

    def on_click(self, char: str):
        """Called by a CalculatorButton when it's clicked."""
        if char == '=':
            if self.result['text']:
                try:
                    answer = str(eval(self.result['text']))
                except SyntaxError:
                    tk.messagebox.showerror("Error", "Your calculation isn't valid.")
                except ZeroDivisionError:
                    tk.messagebox.showerror('Error', "You can't divide by zero.")
                else:
                    self.result['text'] = answer
        elif char == 'C':
            self.result['text'] = ''
        elif char == 'CE':
            self.result['text'] = self.result['text'][:-1]
        else:
            self.result['text'] += char


def test():
    def clicked(caption: str):
        print(f'{caption} was clicked')

    main_window = tk.Tk()
    main_window.title("CalculatorButton test")
    main_window.geometry('640x480')

    btn = CalculatorButton(main_window, callback=clicked, text='Test')
    btn.grid(row=0, column=0, sticky="nsew")

    main_window.mainloop()


if __name__ == '__main__':
    test()
