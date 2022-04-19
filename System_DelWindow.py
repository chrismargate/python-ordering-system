from System_LoginWindow import LoginWindow
from BreakfastWindow import BreakfastWindow
from BurgersWindow import BurgersWindow
from ChickenWindow import ChickenWindow
from AppetizersWindow import AppetizersWindow
from BeveragesWindow import BeveragesWindow
from DessertsWindow import DessertsWindow
from BagWindow import BagWindow
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import date
import mysql.connector as sql

class EmptyFieldError(Exception):
    pass

class InvalidFieldError(Exception):
    pass

class DeliveryWindow:

    def __init__(self, master=None):

        self.master = master
        self.master.resizable("False","False")

        # build ui
        # ---------------------DELIVERY FRAME---------------------------
        self.frame_delWindow = tk.Frame(self.master)
        self.frame_delWindow.configure(background='#b92e34', height='350', relief='raised', width='485')
        self.frame_delWindow.pack(expand='false', side='top')

        # ---------------------LABELS---------------------------
        #FRAME
        self.label_delDetails = tk.Label(self.frame_delWindow)
        self.label_delDetails.configure(background='#982121', cursor='arrow', font='{Arial} 30 {bold}', foreground='#f9d71c')
        self.label_delDetails.configure(relief='flat', text='     DELIVERY DETAILS       ')
        self.label_delDetails.place(anchor='nw', x='0', y='0')

        #CONTACT NUMBER
        self.label_delContactNum = tk.Label(self.frame_delWindow)
        self.label_delContactNum.configure(background='#b92e34', font='{Consolas} 15 {bold}', foreground='#f9d71c', text='CONTACT NUMBER:*')
        self.label_delContactNum.place(anchor='nw', x='10', y='60')

        #ADDRESS LINE 1
        self.label_delAddLine1 = tk.Label(self.frame_delWindow)
        self.label_delAddLine1.configure(background='#b92e34', font='{Consolas} 15 {bold}', foreground='#f9d71c', text='ADDRESS LINE #1:*')
        self.label_delAddLine1.place(anchor='nw', x='10', y='90')

        #ADDRESS LINE 2
        self.label_delAddLine2 = tk.Label(self.frame_delWindow)
        self.label_delAddLine2.configure(background='#b92e34', font='{Consolas} 15 {bold}', foreground='#f9d71c', text='ADDRESS LINE #2:')
        self.label_delAddLine2.place(anchor='nw', x='10', y='120')

        #CITY
        self.label_delCity = tk.Label(self.frame_delWindow)
        self.label_delCity.configure(background='#b92e34', font='{Consolas} 15 {bold}', foreground='#f9d71c', text='CITY:*')
        self.label_delCity.place(anchor='nw', x='10', y='150')

        #PAYMENT
        self.label_delPayment = tk.Label(self.frame_delWindow)
        self.label_delPayment.configure(background='#b92e34', font='{Consolas} 15 {bold}', foreground='#f9d71c', text='PAYMENT METHOD:*')
        self.label_delPayment.place(anchor='nw', x='10', y='180')

        #CARD NUMBER
        self.label_delCardNum = tk.Label(self.frame_delWindow)
        self.label_delCardNum.configure(background='#b92e34', cursor='arrow', font='{Consolas} 10 {bold}', foreground='#f9d71c')
        self.label_delCardNum.configure(takefocus=False, text='Card Number:')
        # self.label_delCardNum.place(anchor='nw', x='10', y='230')

        #EXPIRY DATE
        self.label_delExpDate = tk.Label(self.frame_delWindow)
        self.label_delExpDate.configure(background='#b92e34', font='{Consolas} 10 {bold}', foreground='#f9d71c', text='Expiry Date:')
        # self.label_delExpDate.place(anchor='nw', x='10', y='265')

        #CVC
        self.label_delCVC = tk.Label(self.frame_delWindow)
        self.label_delCVC.configure(text='CVC:')
        self.label_delCVC.configure(background='#b92e34', font='{Consolas} 10 {bold}', foreground='#f9d71c', takefocus=False)
        # self.label_delCVC.place(anchor='nw', x='319', y='230')

        #NAME ON THE CARD
        self.label_delCardName = tk.Label(self.frame_delWindow)
        self.label_delCardName.configure(background='#b92e34', font='{Consolas} 10 {bold}', foreground='#f9d71c', text='Name on the card:')
        # self.label_delCardName.place(anchor='nw', x='228', y='265')
        # ---------------------ENTRIES---------------------------
        #CONTACT NUMBER
        self.entry_delContactNum = tk.Entry(self.frame_delWindow)
        self.entry_delContactNum.configure(relief='sunken')
        self.entry_delContactNum.place(anchor='nw', width='250', x='220', y='60')

        #ADDRESS LINE 1
        self.entry_delAddLine1 = tk.Entry(self.frame_delWindow)
        self.entry_delAddLine1.configure(relief='sunken')
        self.entry_delAddLine1.place(anchor='nw', width='250', x='220', y='90')

        #ADDRESS LINE 2
        self.entry_delAddLine2 = tk.Entry(self.frame_delWindow)
        self.entry_delAddLine2.configure(relief='sunken')
        self.entry_delAddLine2.place(anchor='nw', width='250', x='220', y='120')

        #CITY
        self.entry_delCity = tk.Entry(self.frame_delWindow)
        self.entry_delCity.configure(relief='sunken')
        self.entry_delCity.place(anchor='nw', width='250', x='220', y='150')

        #CARD NUMBER
        self.entry_delCardNum = tk.Entry(self.frame_delWindow)
        self.entry_delCardNum.configure(validate='focusin')
        # self.entry_delCardNum.place(anchor='nw', x='97', y='245')

        #EXPIRY DATE
        self.entry_delExpDate = tk.Entry(self.frame_delWindow)
        # self.entry_delExpDate.place(anchor='nw', x='97', y='280')

        #NAME ON THE CARD
        self.entry_delCardName = tk.Entry(self.frame_delWindow)
        # self.entry_delCardName.place(anchor='nw', x='350', y='280')

        #CVC
        self.entry_delCVC = tk.Entry(self.frame_delWindow)
        # self.entry_delCVC.place(anchor='nw', x='350', y='245')

        # ---------------------BUTTONS--------------------------------
        #CONFIRM
        self.button_delConfirm = tk.Button(self.frame_delWindow)
        self.button_delConfirm.configure(background='#77dd77', font='{arial} 10 {bold}', relief='ridge', text='CONFIRM')
        self.button_delConfirm["command"] = self.confirm_action
        self.button_delConfirm.place(width='150', x='260', y='315')

        #CANCEL
        self.button_delCancel = tk.Button(self.frame_delWindow)
        self.button_delCancel.configure(background='#ff6961', font='{arial} 10 {bold}', relief='ridge', text='CANCEL')
        self.button_delCancel["command"] = self.master.destroy
        self.button_delCancel.place(anchor='nw', width='150', x='70', y='315')

        self.payment_var = tk.StringVar(value="N/A")
        #COD RADIOBUTTON
        self.rbutton_delCOD = tk.Radiobutton(self.frame_delWindow)
        self.rbutton_delCOD.configure(anchor='n', font='{Consolas} 11 {bold}')
        # self.rbutton_delCOD["foreground"] = '#f9d71c'
        self.rbutton_delCOD["background"] = '#b92e34'
        self.rbutton_delCOD.configure(indicatoron='true', overrelief='groove', relief='flat', text='Cash on delivery (COD)')
        self.rbutton_delCOD["variable"] = self.payment_var
        self.rbutton_delCOD["value"] = "0"
        self.rbutton_delCOD["command"] = self.button_clicked
        self.rbutton_delCOD.place(anchor='nw', x='50', y='205')

        #CARD RADIOBUTTON
        self.rbutton_delVisaMcard = tk.Radiobutton(self.frame_delWindow)
        self.rbutton_delVisaMcard.configure( font='{Consolas} 11 {bold}', text='Visa/self.mastercard')
        # self.rbutton_delVisaMcard["foreground"] = '#f9d71c'
        self.rbutton_delVisaMcard["background"] = '#b92e34'
        self.rbutton_delVisaMcard["variable"] = self.payment_var
        self.rbutton_delVisaMcard["value"] = "1"
        self.rbutton_delVisaMcard["command"] = self.button_clicked
        self.rbutton_delVisaMcard.place(anchor='nw', x='275', y='205')

        # Main widget
        self.mainwindow = self.frame_delWindow

    def button_clicked(self):
        if self.payment_var.get() == "0":
            if self.label_delCardNum.winfo_ismapped():
                # self.label_delCardNum.place(anchor='nw', x='10', y='230')
                self.label_delCardNum.place_forget()
                self.label_delExpDate.place_forget()
                self.label_delCVC.place_forget()
                self.label_delCardName.place_forget()

                self.entry_delCardNum.place_forget()
                self.entry_delExpDate.place_forget()
                self.entry_delCardName.place_forget()
                self.entry_delCVC.place_forget()
            return
        if not self.label_delCardNum.winfo_ismapped():
            self.label_delCardNum.place(anchor='nw', x='10', y='230')
            self.label_delExpDate.place(anchor='nw', x='10', y='265')
            self.label_delCVC.place(anchor='nw', x='319', y='230')
            self.label_delCardName.place(anchor='nw', x='228', y='265')

            self.entry_delCardNum.place(anchor='nw', x='97', y='245')
            self.entry_delExpDate.place(anchor='nw', x='97', y='280')
            self.entry_delCardName.place(anchor='nw', x='350', y='280')
            self.entry_delCVC.place(anchor='nw', x='350', y='245')

    def confirm_action(self):
        
        bag_list = []
        bag_list.extend(BreakfastWindow.list_bag)
        bag_list.extend(BurgersWindow.list_bag)
        bag_list.extend(ChickenWindow.list_bag)
        bag_list.extend(AppetizersWindow.list_bag)
        bag_list.extend(BeveragesWindow.list_bag)
        bag_list.extend(DessertsWindow.list_bag)

        # for food_item in bag_list:
        #     print(food_item.get_number(),food_item.get_name())
        
        # return

        if self.empty_fields():
            return

        contact_number = self.entry_delContactNum.get()
        address_line = self.entry_delAddLine1.get() + self.entry_delAddLine2.get()
        city = self.entry_delCity.get()
        payment_method = ""
        card_number = ""
        card_name = ""
        cvc_number = ""
        expiry_date = ""
        # card_number = self.entry_delCardNum.get()
        # card_name = self.entry_delCardName.get()
        # cvc_number = self.entry_delCVC.get()
        # expiry_date = self.entry_delExpDate.get()
        if self.payment_var.get() == "0":
            print("in payment 0")
            payment_method = "COD"
        elif self.payment_var.get() == "1":
            print("in payment 1")
            payment_method = "VISA/MASTERCARD"
            card_number = self.entry_delCardNum.get()
            card_name = self.entry_delCardName.get()
            cvc_number = self.entry_delCVC.get()
            expiry_date = self.entry_delExpDate.get()

        todays_date = date.today().strftime("%m/%d/%y")
        
        try:
            for food_item in bag_list:
                connection = sql.connect(host="localhost",user="root",passwd="NewPassword")
                my_cursor = connection.cursor()
                string_for_insert = f'INSERT INTO ekasborgers.orders_t(customer_id,food_id,quantity,order_date,total_price,payment_method,card_number,card_cvc,card_name,card_expiry ) \
VALUES ("{LoginWindow.active_accnumber}", "{food_item.get_number()}", "{food_item.get_quantity()}", "{todays_date}", "{food_item.get_price()}", "{payment_method}","{card_number}","{cvc_number}","{card_name}","{expiry_date}");'
                # string_for_insert = f"INSERT INTO ekasborgers.orders_t (`order_id`, `customer_id`, `food_id`, `quantity`, `order_date`, `total_price`, `payment_method`) VALUES ('{LoginWindow.active_accnumber}`, `{food_item.get_number()}`, `{food_item.get_quantity()}`, `{todays_date}`, `{food_item.get_price()}`, `{payment_method}')"
    
                my_cursor.execute(string_for_insert)
                connection.commit()
                connection.close()
        except Exception as e:
            connection.close()
            print(f"\t{e}\t")
            return

        connection.close()
        messagebox.showinfo("Order successful","You're order has been placed! Please wait for your delivery to arrive.")
        self.master.destroy()

    def empty_fields(self):
        try:
            for letter in self.entry_delContactNum.get().strip():
                if letter == "":
                    raise EmptyFieldError
                if not letter.isdigit():
                    raise Exception
        except EmptyFieldError as efe:
            messagebox.showerror("Empty Field","Contact number field is empty!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Invalid input for contact number!")
            return

        try:
            if self.entry_delAddLine1.get().strip() == "":
                raise EmptyFieldError

            if len(self.entry_delAddLine1.get().strip()) < 10:
                raise Exception
        except EmptyFieldError as efe:
            messagebox.showerror("Empty Field","Contact number field is empty!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Invalid input for address. Address must be at least 5 characters!")
            return True

        try:
            if self.entry_delCity.get().strip() == "":
                raise EmptyFieldError

            if len(self.entry_delCity.get().strip()) < 5:
                raise Exception
        except EmptyFieldError as efe:
            messagebox.showerror("Empty Field","City field is empty!")
            return True
        except Exception as e:
            messagebox.showerror("Invalid Input","Invalid input for city. City name must be at least 5 characters!")
            return True

        # try:
        #     if self.entry_delCity.get().strip() == "":
        #         raise EmptyFieldError

        #     if len(self.entry_delAddLine1.get().strip()) < 5:
        #         raise Exception
        # except EmptyFieldError as efe:
        #     messagebox.showerror("Empty Field","Contact number field is empty!")
        #     return True
        # except Exception as e:
        #     messagebox.showerror("Invalid Input","Invalid input for city. City name must be at least 5 characters!")
        #     return True

        if self.payment_var.get() == "N/A" or self.payment_var.get() == "":
            messagebox.showerror("Empty Field","No payment method has been selected!")
            return True
        
        if self.payment_var.get() == "1":
            try:
                if self.entry_delCardNum.get().strip() == "":
                    raise EmptyFieldError

                for number in self.entry_delCardNum.get().strip():
                    if not number.isdigit():
                        raise Exception
            except EmptyFieldError as efe:
                messagebox.showerror("Empty Field","Card number field is empty!")
                return True
            except Exception as e:
                messagebox.showerror("Invalid Input","Invalid input for card number. Card number must not have any spaces, letters or symbols!")
                return True

            try:
                if self.entry_delExpDate.get().strip() == "":
                    raise EmptyFieldError

                if len(self.entry_delExpDate.get().strip()) < 7:
                    raise Exception
            except EmptyFieldError as efe:
                messagebox.showerror("Empty Field","Expiry date field is empty!")
                return True
            except Exception as e:
                messagebox.showerror("Invalid Input","Invalid input for expiry date. Expiry date format must be 'MM/YYYY'!")
                return True

            try:
                if self.entry_delCardName.get().strip() == "":
                    raise EmptyFieldError

                if len(self.entry_delCardName.get().strip()) < 5:
                    raise Exception
            except EmptyFieldError as efe:
                messagebox.showerror("Empty Field","Cardholder's name field is empty!")
                return True
            except Exception as e:
                messagebox.showerror("Invalid Input","Invalid input for cardholder name. Cardholder name must be at least 5 characters!")
                return True

            try:
                if self.entry_delCVC.get().strip() == "":
                    raise EmptyFieldError

                for number in self.entry_delCVC.get().strip():
                    if not number.isdigit():
                        raise Exception

            except EmptyFieldError as efe:
                messagebox.showerror("Empty Field","CVC field is empty!")
                return True
            except Exception as e:
                messagebox.showerror("Invalid Input","Invalid input for CVC. CVC must be at least 3 numbers!")
                return True

        return False

    def invalid_fields(self):
        pass

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = DeliveryWindow(root)
    app.run()

