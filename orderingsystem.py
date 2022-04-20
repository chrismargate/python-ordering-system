# Classes
from AboutusWindow import AboutusWindow
from BreakfastWindow import BreakfastWindow
from BurgersWindow import BurgersWindow
from ChickenWindow import ChickenWindow
from AppetizersWindow import AppetizersWindow
from BeveragesWindow import BeveragesWindow
from DessertsWindow import DessertsWindow
from BagWindow import BagWindow
from System_LoginWindow import LoginWindow
from System_DelWindow import DeliveryWindow

from Food import Food

# TKINTER
import os
import random
from tkinter import messagebox
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter.constants import BOTH, COMMAND, LEFT, NW, RIDGE, RIGHT, VERTICAL, Y, YES
import tkinter.ttk as ttk
import mysql.connector as sql

# PILLOW
from typing import Text
from PIL import ImageTk, Image


class OrderingSystem:

    logged_in = False
    on_loop = True

    def __init__(self, master=None):
        self.list_bag = []

        self.master = master
        self.master.resizable("False", "False")
        self.master.title("Eka's Borgers")

        # build ui
        self.mainframe = tk.Frame(self.master)
        self.navigationpanel = tk.Frame(self.mainframe)

        # Main widget
        self.mainwindow = self.mainframe

        # Mainframe
        self.mainframe.configure(background='#b92e34',
                                 height='380', width='960')
        self.mainframe.pack(side='top')
        self.opened_window = None

        # #Components for Navigation Frame
        # self.homebutton = tk.Button(self.navigationpanel)
        # self.homebutton.configure(background='#982121', compound='top', font='{arial black} 15 {}', foreground='white',command=self.home_action)
        # self.homebutton.configure(text='Home')
        # self.homebutton.place(anchor='nw', height='50', width='150', x='0', y='100')

        self.categoriesbutton = tk.Button(self.navigationpanel)
        self.categoriesbutton.configure(
            background='#982121', font='{arial black} 15 {}', foreground='white', text='Categories', command=self.display_buttons)
        self.categoriesbutton.place(
            anchor='nw', height='50', width='150', x='0', y='100')
        # self.categoriesbutton.place(anchor='nw', height='50', width='150', x='0', y='150')

        self.bagbutton = tk.Button(self.navigationpanel)
        self.bagbutton.configure(
            background='#982121', font='{arial black} 15 {}', foreground='white', text='Bag', command=self.bag_action)
        self.bagbutton.place(anchor='nw', height='50',
                             width='150', x='0', y='150')
        # self.bagbutton.place(anchor='nw', height='50', width='150', x='0', y='200')

        self.aboutusbutton = tk.Button(self.navigationpanel)
        self.aboutusbutton.configure(
            background='#982121', font='{arial black} 15 {}', foreground='white', text='About us', command=self.aboutus_action)
        self.aboutusbutton.place(
            anchor='nw', height='50', width='150', x='0', y='200')
        # self.aboutusbutton.place(anchor='nw', height='50', width='150', x='0', y='250')

        self.logoutbutton = tk.Button(self.navigationpanel)
        self.logoutbutton.configure(
            background='#982121', font='{arial black} 15 {}', foreground='white', text='Logout')
        self.logoutbutton["command"] = self.logout_action
        self.logoutbutton.place(anchor='nw', height='50',
                                width='150', x='0', y='300')

        self.navigationpanel.configure(
            background='#b92e34', height='500', width='150')
        self.navigationpanel.place(anchor='nw', x='0', y='0')

        # Components for Search Frame
        self.searchpanel = tk.Frame(self.mainframe)
        self.searchpanel.configure(height='50', width='950')
        self.searchpanel["background"] = "#b92e34"
        self.searchpanel.place(anchor='nw', x='151', y='0')

        self.checkoutbutton = tk.Button(self.searchpanel)
        self.checkoutbutton.configure(
            background='#982121', font='{arial black} 12 {}', foreground='white', text='Checkout')
        self.checkoutbutton["command"] = self.checkout_action
        self.checkoutbutton.place(
            anchor='nw', height='30', width='120', x='650', y='12')

        # The Frame for Displaying Featured Products
        self.displayingpanel = tk.Frame(self.mainframe)
        self.displayingpanel.configure(height='500', width='650')
        self.displayingpanel["bg"] = "#b92e34"
        self.displayingpanel.place(anchor='nw', x='151', y='50')

        # Frame of Category Choices
        self.categoriesframe = tk.Frame(self.mainframe)

        self.breakfastbutton = tk.Button(self.categoriesframe)
        self.breakfastbutton.configure(
            background='#982121', foreground='white', text='Breakfast', command=self.breakfast_category)
        self.breakfastbutton.place(anchor='nw', width='100', x='0', y='0')

        self.burgersbutton = tk.Button(self.categoriesframe)
        self.burgersbutton.configure(
            background='#982121', foreground='white', text='Burgers', command=self.burgers_category)
        self.burgersbutton.place(anchor='nw', width='100', x='0', y='25')

        self.chickensbutton = tk.Button(self.categoriesframe)
        self.chickensbutton.configure(
            background='#982121', foreground='white', text='Chickens', command=self.chickens_category)
        self.chickensbutton.place(anchor='nw', width='100', x='0', y='50')

        self.appetizersbutton = tk.Button(self.categoriesframe)
        self.appetizersbutton.configure(
            background='#982121', foreground='white', text='Appetizers', command=self.appetizers_category)
        self.appetizersbutton.place(anchor='nw', width='100', x='0', y='75')

        self.beveragesbutton = tk.Button(self.categoriesframe)
        self.beveragesbutton.configure(
            background='#982121', foreground='white', text='Beverages', command=self.beverages_action)
        self.beveragesbutton.place(anchor='nw', width='100', x='0', y='100')

        self.dessertsbutton = tk.Button(self.categoriesframe)
        self.dessertsbutton.configure(
            background='#982121', foreground='white', text='Desserts', command=self.desserts_category)
        self.dessertsbutton.place(anchor='nw', width='100', x='0', y='125')

        self.categoriesframe.configure(height='150', width='100')

        if LoginWindow.active_usertype == "CUSTOMER":
            self.generate_featured_products()
        else:
            self.generate_graph_buttons()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_buttons(self):
        if self.categoriesframe.winfo_ismapped():
            self.categoriesframe.place_forget()
            return
        self.categoriesframe.place(anchor='nw', x='151', y='131')

    def generate_graph_buttons(self):
        # Featured Graphs
        self.payment_method_graph = tk.Button(self.displayingpanel)
        self.payment_method_graph["width"] = "55"
        self.payment_method_graph["command"] = self.payment_graph_action
        self.payment_method_graph["text"] = "Most preferred payment method bar graph"
        self.payment_method_graph.grid(row=0, column=0)

        self.fooditem_graph = tk.Button(self.displayingpanel)
        self.fooditem_graph["width"] = "55"
        self.fooditem_graph["command"] = self.fooditem_graph_action
        self.fooditem_graph["text"] = "Most ordered food item by quantity bar graph"
        self.fooditem_graph.grid(row=0, column=1)

        self.foodtype_pie = tk.Button(self.displayingpanel)
        self.foodtype_pie["width"] = "55"
        self.foodtype_pie["command"] = self.foodtype_pie_action
        self.foodtype_pie["text"] = "Most ordered food type by quantity pie chart"
        self.foodtype_pie.grid(row=1, column=0)

    def payment_graph_action(self):
        connection = sql.connect(
            host="localhost", user="root", passwd="NewPassword")
        cur = connection.cursor()

        string_query = f'SELECT COUNT(payment_method),payment_method \
FROM ekasborgers.orders_T \
GROUP BY payment_method;'

        intervals = []
        payment_method = []
        cur.execute(string_query)

        for record in cur:
            intervals.append(record[0])
            payment_method.append(record[1])

        plt.bar(payment_method, intervals)

        plt.xlabel("Payment Methods")
        plt.ylabel("Number of Orders")
        plt.title("Most preferred payment method")
        plt.show()

        connection.close()

    def fooditem_graph_action(self):
        connection = sql.connect(
            host="localhost", user="root", passwd="NewPassword")
        cur = connection.cursor()

        string_query = f'SELECT SUM(quantity),ekasborgers.orders_t.food_id,ekasborgers.fooditems_t.food_name \
FROM ekasborgers.orders_T \
JOIN ekasborgers.fooditems_T \
ON ekasborgers.orders_t.food_id = ekasborgers.fooditems_t.food_id \
GROUP BY food_id;'

        intervals = []
        food_items = []
        cur.execute(string_query)

        for record in cur:
            intervals.append(record[0])
            food_items.append(str(record[1]) + "\n" + record[2])

        plt.bar(food_items, intervals)

        plt.xlabel("Food Item")
        plt.ylabel("Number of Orders")
        plt.title("Most ordered food item")
        plt.show()

        connection.close()

    def foodtype_pie_action(self):
        connection = sql.connect(
            host="localhost", user="root", passwd="NewPassword")
        cur = connection.cursor()

        string_query = f'SELECT SUM(quantity),ekasborgers.fooditems_t.food_type \
FROM ekasborgers.orders_T \
JOIN ekasborgers.fooditems_T \
ON ekasborgers.orders_t.food_id = ekasborgers.fooditems_t.food_id \
GROUP BY fooditems_t.food_type;'

        values = []
        food_types = []
        cur.execute(string_query)

        for record in cur:
            values.append(record[0])
            food_types.append(record[1])

        plt.pie(values, labels=food_types, autopct="%.lf%%")

        plt.title("Most ordered food item")
        plt.show()

        connection.close()

    def generate_featured_products(self):
        self.folder_names = ["Appetizers", "Breakfast",
                             "Beverages", "Desserts", "Chicken", "Burgers"]
        self.list_images = []
        self.list_chosen_words = []
        i = 0
        start_row = 0
        start_column = 0
        while i < 6:
            file_keyword = random.choice(self.folder_names)
            temp_list = os.listdir(os.getcwd() + f"\\assets\\{file_keyword}")
            temp_list = [x for x in temp_list if x.endswith(".png")]
            while True:
                image_keyword = random.choice(temp_list)
                if image_keyword in self.list_chosen_words:
                    continue
                else:
                    self.list_chosen_words.append(image_keyword)
                    break
            self.list_images.append(ImageTk.PhotoImage(Image.open(
                f"{os.getcwd()}\\assets\\{file_keyword}\\{image_keyword}").resize((263, 150), Image.ANTIALIAS)))
            i += 1

        i = 0
        for img in self.list_images:
            self.image_label = tk.Label(self.displayingpanel, image=img)
            self.image_label.grid(row=start_row, column=start_column)

            i += 1
            start_column += 1
            if start_column >= 3:
                start_column = 0
                start_row += 1

    def checkout_action(self):
        if BagWindow.list_bag == []:
            messagebox.showerror("View Error", "Your bag is empty!")
            return
        confirm_question = messagebox.askquestion(
            "Checkout", "Are you sure you want to check out?")
        if confirm_question == "no":
            return
        self.configure_opened_window()
        DeliveryWindow(self.opened_window).run()

    def breakfast_category(self):
        self.configure_opened_window()
        BreakfastWindow(self.opened_window).run()

    def burgers_category(self):
        self.configure_opened_window()
        BurgersWindow(self.opened_window).run()

    def chickens_category(self):
        self.configure_opened_window()
        ChickenWindow(self.opened_window).run()

    def appetizers_category(self):
        self.configure_opened_window()
        AppetizersWindow(self.opened_window).run()

    def desserts_category(self):
        self.configure_opened_window()
        DessertsWindow(self.opened_window).run()

    def beverages_action(self):
        self.configure_opened_window()
        BeveragesWindow(self.opened_window).run()

    def bag_action(self):
        self.configure_opened_window()
        BagWindow(self.opened_window).run()

    def aboutus_action(self):
        self.configure_opened_window()
        AboutusWindow(self.opened_window).run()

    def configure_opened_window(self):
        if (not self.opened_window == None) and self.opened_window.winfo_exists():
            self.opened_window.destroy()
        self.opened_window = tk.Toplevel()

    def logout_action(self):
        OrderingSystem.on_loop = True
        BagWindow.list_bag = []
        BreakfastWindow.list_bag = []
        BurgersWindow.list_bag = []
        ChickenWindow.list_bag = []
        AppetizersWindow.list_bag = []
        BeveragesWindow.list_bag = []
        DessertsWindow.list_bag = []
        OrderingSystem.logged_in = False
        LoginWindow.logged_in = False
        LoginWindow.active_accnumber = 0
        LoginWindow.active_usertype = ""
        self.master.destroy()

    def on_closing(self):
        confirm_close = messagebox.askquestion(
            "Close", "Are you sure you want to exit?", icon="warning")
        if confirm_close == "no":
            return
        OrderingSystem.on_loop = False
        self.master.destroy()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':

    while OrderingSystem.on_loop == True:
        OrderingSystem.on_loop = False
        LoginWindow(tk.Tk()).run()
        if LoginWindow.logged_in == True:
            OrderingSystem(tk.Tk()).run()
