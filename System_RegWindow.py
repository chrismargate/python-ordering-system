import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector as sql

class EmptyFieldError(Exception):
    pass

class ExistingUsername(Exception):
    pass

class RegisterWindow:
    def __init__(self, master=None):

        self.master = master
        self.master.title("Register")
        self.master.resizable("False","False")

        # build ui
        # ---------------------REGISTER FRAME--------------------------------
        self.frame_regWindow = tk.Frame(self.master)
        self.frame_regWindow.configure(background='#b92e34', height='350', relief='raised', width='485')
        self.frame_regWindow.pack(expand='false', side='top')

        # ---------------------LABELS----------------------------------------
        #FRAME LABEL
        self.label_createAcc = tk.Label(self.frame_regWindow)
        self.label_createAcc.configure(background='#982121', cursor='arrow', font='{Arial} 30 {bold}', foreground='#f9d71c')
        self.label_createAcc.configure(relief='flat', text='     CREATE ACCOUNT       ')
        self.label_createAcc.place(anchor='nw', x='0', y='0')

        #LAST NAME LABEL
        self.label_lName = tk.Label(self.frame_regWindow)
        self.label_lName.configure(background='#b92e34', font='{Consolas} 15 {bold}', foreground='#f9d71c', text='LAST NAME:*')
        self.label_lName.place(anchor='nw', x='10', y='60')

        #FIRST NAME LABEL
        self.label_fName = tk.Label(self.frame_regWindow)
        self.label_fName.configure(background='#b92e34', font='{Consolas} 15 {bold}', foreground='#f9d71c', text='FIRST NAME:*')
        self.label_fName.place(anchor='nw', x='10', y='90')

        #ADDRESS LABEL
        self.label_address = tk.Label(self.frame_regWindow)
        self.label_address.configure(background='#b92e34', font='{cONSOLAS} 15 {bold}', foreground='#f9d71c', text='ADDRESS:')
        self.label_address.place(anchor='nw', x='10', y='120')

        #CONTACT NUMBER LABEL
        self.label_cNumber = tk.Label(self.frame_regWindow)
        self.label_cNumber.configure(background='#b92e34', font='{consolas} 15 {bold}', foreground='#f9d71c', text='CONTACT NUMBER:')
        self.label_cNumber.place(anchor='nw', x='10', y='150')

        #USERNAME LABEL
        self.label_uName = tk.Label(self.frame_regWindow)
        self.label_uName.configure(background='#b92e34', font='{consolas} 15 {bold}', foreground='#f9d71c', text='USERNAME:*')
        self.label_uName.place(anchor='nw', x='10', y='180')

        #PASSWORD LABEL
        self.label_password = tk.Label(self.frame_regWindow)
        self.label_password.configure(background='#b92e34', font='{CONSOLAS} 15 {bold}', foreground='#f9d71c', text='PASSWORD:*')
        self.label_password.place(anchor='nw', x='10', y='210')

        #CONFIRM PASSWORD LABEL
        self.label_conPassword = tk.Label(self.frame_regWindow)
        self.label_conPassword.configure(background='#b92e34', font='{CONSOLAS} 15 {bold}', foreground='#f9d71c', text='CONFIRM PASSWORD:*')
        self.label_conPassword.place(anchor='nw', x='10', y='240')

        # ---------------------ENTRIES----------------------------------------
        #LAST NAME ENTRY
        self.entry_lName = tk.Entry(self.frame_regWindow)
        self.entry_lName.configure(relief='sunken')
        self.entry_lName.place(anchor='nw', width='250', x='220', y='60')

        #FIRST NAME ENTRY
        self.entry_fName = tk.Entry(self.frame_regWindow)
        self.entry_fName.configure(relief='sunken')
        self.entry_fName.place(anchor='nw', width='250', x='220', y='90')

        #ADDRESS ENTRY
        self.entry_address = tk.Entry(self.frame_regWindow)
        self.entry_address.configure(relief='sunken')
        self.entry_address.place(anchor='nw', width='250', x='220', y='120')

        #CONTACT NUMBER ENTRY
        self.entry_cNumber = tk.Entry(self.frame_regWindow)
        self.entry_cNumber.configure(relief='sunken')
        self.entry_cNumber.place(anchor='nw', width='250', x='220', y='150')

        #USERNAME ENTRY
        self.entry_uName = tk.Entry(self.frame_regWindow)
        self.entry_uName.configure(relief='sunken')
        self.entry_uName.place(anchor='nw', width='250', x='220', y='180')

        #PASSWORD ENTRY
        self.entry_password = tk.Entry(self.frame_regWindow)
        self.entry_password.configure(relief='sunken', show='•')
        self.entry_password.place(anchor='nw', width='250', x='220', y='210')

        #CONFIRM PASSWORD ENTRY
        self.entry_conPassword = tk.Entry(self.frame_regWindow)
        self.entry_conPassword.configure(relief='sunken', show='•')
        self.entry_conPassword.place(anchor='nw', width='250', x='220', y='240')

        # ---------------------BUTTONS----------------------------------------
        #REGISTER BUTTON
        self.button_register = tk.Button(self.frame_regWindow)
        self.button_register.configure(background='#77dd77', font='{arial} 10 {bold}', relief='ridge', text='REGISTER')
        self.button_register["command"] = self.register_action
        self.button_register.place(width='150', x='160', y='275')

        #CANCEL BUTTON
        self.button_regCancel = tk.Button(self.frame_regWindow)
        self.button_regCancel.configure(background='#ff6961', font='{arial} 10 {bold}', relief='ridge', text='CANCEL')
        self.button_regCancel["command"] = self.master.destroy
        self.button_regCancel.place(anchor='nw', width='150', x='160', y='315')

        # Main widget
        self.mainwindow = self.frame_regWindow

    def register_action(self):
        if self.empty_field():
            return

        connection = sql.connect(host="localhost",user="root",passwd="NewPassword")
        cur = connection.cursor()
        string_for_insert = f'INSERT INTO ekasborgers.useraccounts_t(user_name,user_password,user_type,f_name,l_name,address,contact_number) VALUES \
("{self.entry_uName.get()}", "{self.entry_password.get()}", "CUSTOMER","{self.entry_fName.get()}", "{self.entry_lName.get()}", "{self.entry_address.get()}", "{self.entry_cNumber.get()}");'
        cur.execute(string_for_insert)

        connection.commit()

        connection.close()

        self.reset_entries()
        messagebox.showinfo("Register successful","Your account has been created successsfully!")

        confirm_question = messagebox.askquestion("Question","Would you like to close this window?")

        if confirm_question == "no":
            return

        self.master.destroy()

    def empty_field(self):
        try:
            if self.entry_lName.get().strip() == "":
                raise EmptyFieldError
            for letter in self.entry_lName.get().strip():
                if letter.isdigit():
                    raise Exception
        except EmptyFieldError as efe:
            messagebox.showerror("Invalid Input","Last name field is empty!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Invalid last name!")
            return True

        try:
            if self.entry_fName.get().strip() == "":
                raise EmptyFieldError
            for letter in self.entry_fName.get().strip():
                if letter.isdigit():
                    raise Exception
        except EmptyFieldError as efe:
            messagebox.showerror("Invalid Input","First name field is empty!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Invalid first name!")
            return True

        try:
            if self.entry_uName.get().strip() == "":
                raise EmptyFieldError
            if len(self.entry_uName.get().strip()) < 5:
                raise Exception

            connection = sql.connect(host="localhost",user="root",passwd="NewPassword")
            cur = connection.cursor()

            cur.execute("SELECT user_name FROM ekasborgers.useraccounts_T;")

            for account in cur:
                if account[0] == self.entry_uName.get().strip():
                    raise ExistingUsername

            connection.close()
        except EmptyFieldError as efe:
            messagebox.showerror("Invalid Input","Username field is empty!")
            return True
        except ExistingUsername as eu:
            messagebox.showerror("Invalid Input","An account with an existing username already exists! Please try again!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Username must have at least 5 characters")
            return True
        
        try:
            if self.entry_password.get().strip() == "":
                raise EmptyFieldError
            if len(self.entry_password.get().strip()) < 5:
                raise Exception
        except EmptyFieldError as efe:
            messagebox.showerror("Invalid Input","Password field is empty!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Password must have at least 5 characters")
            return True

        try:
            if self.entry_conPassword.get().strip() == "":
                raise EmptyFieldError
            if not self.entry_password.get().strip() == self.entry_conPassword.get().strip():
                raise Exception
        except EmptyFieldError as efe:
            messagebox.showerror("Invalid Input","Confirm password field is empty!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Password does not match confirm password field!")
            return True

        return False

    def reset_entries(self):
        self.entry_lName.delete(0,"end")
        self.entry_fName.delete(0,"end")
        self.entry_address.delete(0,"end")
        self.entry_cNumber.delete(0,"end")
        self.entry_uName.delete(0,"end")
        self.entry_password.delete(0,"end")
        self.entry_conPassword.delete(0,"end")

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = RegisterWindow(root)
    app.run()

