#Classes
from System_RegWindow import RegisterWindow

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector as sql

class EmptyUsernameField(Exception):
    pass

class EmptyPasswordField(Exception):
    pass

class InvalidUsername(Exception):
    pass

class InvalidPassword(Exception):
    pass

class LoginWindow:

    active_accnumber = 0
    logged_in = False
    active_usertype = ""

    def __init__(self, master=None):
        self.master = master
        self.master.resizable("False","False")
        self.master.title("Log In")
        
        # build ui
        # ---------------------LOGIN FRAME---------------------------
        self.frame_login = tk.Frame(master, container='false')
        self.frame_login.configure(background='#b92e34', height='300', relief='raised', width='335')
        self.frame_login.pack(side='top')
        
        self.opened_window = None

        # ---------------------LABELS--------------------------------
        #FRAME LABEL
        self.label_login = tk.Label(self.frame_login)
        self.label_login.configure(background='#982121', cursor='arrow', font='{arial} 20 {bold}', foreground='#f9d71c')
        self.label_login.configure(relief='flat', text='          USER LOGIN           ')
        self.label_login.place(anchor='nw', x='0')

        #USERNAME LABEL
        self.label_loginUname = tk.Label(self.frame_login)
        self.label_loginUname.configure(background='#b92e34', font='{consolas} 15 {bold}', foreground='#f9d71c', text='USERNAME:')
        self.label_loginUname.place(anchor='nw', x='10', y='70')

        #PASSWORD LABEL
        self.label_loginPassword = tk.Label(self.frame_login)
        self.label_loginPassword.configure(background='#b92e34', font='{consolas} 15 {bold}', foreground='#f9d71c', justify='left')
        self.label_loginPassword.configure(takefocus=False, text='PASSWORD:')
        self.label_loginPassword.place(anchor='nw', x='10', y='120')

        # ---------------------ENTRIES--------------------------------

        self.username_var = tk.StringVar(value="")
        self.password_var = tk.StringVar(value="")
        
        #USERNAME ENTRY
        self.entry_loginUname = tk.Entry(self.frame_login)
        self.entry_loginUname.configure(relief='sunken')
        self.entry_loginUname["textvariable"] = self.username_var
        self.entry_loginUname.place(anchor='nw', width='200', x='120', y='75')

        #PASSWORD ENTRY
        self.entry_loginPassword = tk.Entry(self.frame_login)
        self.entry_loginPassword.configure(relief='sunken', show='•', takefocus=False)
        self.entry_loginPassword["textvariable"] = self.password_var
        self.entry_loginPassword.place(anchor='nw', width='200', x='120', y='125')

        # ---------------------BUTTONS--------------------------------
        #LOGIN BUTTON
        self.button_loginLogin = tk.Button(self.frame_login)
        self.button_loginLogin.configure(background='#77dd77', font='{arial} 10 {bold}', relief='ridge', text='LOGIN')
        self.button_loginLogin["command"] = self.login_action
        self.button_loginLogin.place(anchor='nw', width='200', x='70', y='170')

        # REGISTER BUTTON
        self.button_loginRegister = tk.Button(self.frame_login)
        self.button_loginRegister.configure(background='#FFFF00', font='{arial} 10 {bold}', relief='ridge', text='REGISTER')
        self.button_loginRegister["command"] = self.register_action
        self.button_loginRegister.place(anchor='nw', width='200', x='70', y='210')

        #CANCEL BUTTON
        self.button_loginCancel = tk.Button(self.frame_login)
        self.button_loginCancel.configure(background='#ff6961', font='{arial} 10 {bold}', relief='ridge', text='CANCEL')
        self.button_loginCancel["command"] = self.master.destroy
        self.button_loginCancel.place(anchor='nw', width='200', x='70', y='250')

        # Main widget
        self.mainwindow = self.frame_login

    def login_action(self):
        if self.empty_username():
            messagebox.showerror("Empty Field","Username field is empty!")
            self.reset_entries()
            return
        if self.empty_password():
            messagebox.showerror("Empty Field","Password field is empty!")
            self.reset_entries()
            return
        try:
            username_match = False
            password_match = False
            connection = sql.connect(host="localhost",user="root",passwd="NewPassword")
            cur = connection.cursor()
            cur.execute("SELECT account_number,user_name,user_password,user_type FROM ekasborgers.useraccounts_t;")

            for column in cur:
                if self.username_var.get() == column[1]:
                    username_match = True
                    if self.password_var.get() == column[2]:
                        password_match = True
                        LoginWindow.logged_in = True
                        LoginWindow.active_accnumber = int(column[0])
                        LoginWindow.active_usertype = column[3]
                    else:
                        messagebox.showerror("Log In Error","Incorrect Password!  Please try again!")
                        self.reset_entries()
                        return
                    break
            
            if username_match == False:
                messagebox.showerror("Log In Error","Username is incorrect or does not exist! Please try again!")
                self.reset_entries()
                return

            connection.close()
        except Exception as e:
            print(f"\t{e}\t")
            return
        
        messagebox.showinfo("Log in success","You have logged in successfully!")
        self.master.destroy()

    def register_action(self):
        self.configure_opened_window()
        RegisterWindow(self.opened_window).run()

    def empty_username(self):
        try:
            if self.username_var.get().strip() == "":
                raise EmptyUsernameField
        except EmptyUsernameField as euf:
            return True
        return False

    def empty_password(self):
        try:
            if self.password_var.get().strip() == "":
                raise EmptyPasswordField
        except EmptyPasswordField as epf:
            return True
    
        return False

    def reset_entries(self):
        self.username_var.set("")
        self.password_var.set("")
    
    def configure_opened_window(self):
        if (not self.opened_window == None) and self.opened_window.winfo_exists():
            self.opened_window.destroy()
        self.opened_window = tk.Toplevel()

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = LoginWindow(root)
    app.run()

