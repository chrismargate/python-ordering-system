import os
import tkinter as tk
import tkinter.ttk as ttk


class AboutusWindow:
    def __init__(self, master=None):
        self.master = master
        self.master.title("About Us")
        self.master.resizable("false","false")

        # build ui
        self.aboutuswindow = tk.Frame(self.master)
        self.aboutustexts = tk.Text(self.aboutuswindow)
        self.aboutustexts.configure(font='{arial black} 11 {}', height='10', width='50', bg='#982121', fg='yellow')
        _text_ = '''This is Eka's Borgers App. Here, we aim to serve delicious
fast-food without compromising your time. We also offer our 
customers delivery so that your health will not be endangered, especially in this time of covid-19 pandemic. 
Your life is our priority!

Contact us:

Facebook: Eka's Borgers

Twitter: @Ekasboorgir

'''
        self.aboutustexts.insert('0.0', _text_)
        self.aboutustexts.place(anchor='nw', height='300', width='500', x='0', y='0')
        self.aboutuswindow.configure(height='300', width='500')
        self.aboutuswindow.pack(side='top')

        # Main widget
        self.mainwindow = self.aboutuswindow

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    AboutusWindow(root).run()