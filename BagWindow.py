from AboutusWindow import AboutusWindow
from BreakfastWindow import BreakfastWindow
from BurgersWindow import BurgersWindow
from ChickenWindow import ChickenWindow
from AppetizersWindow import AppetizersWindow
from BeveragesWindow import BeveragesWindow
from DessertsWindow import DessertsWindow
# from BagWindow import BagWindow

import os
from PIL import ImageTk,Image
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from Food import Food
from copy import deepcopy

class BagWindow:

    list_bag = []

    def __init__(self,master=None):

        self.master = master
        self.master.geometry("550x700")
        self.master.resizable(False,False)
        self.master.title("Bag")

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH,expand=1)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion= self.canvas.bbox("all")))

        self.second_frame = tk.Frame(self.canvas)
        self.second_frame.bind("<Enter>",self.bound_to_mousewheel)
        self.second_frame.bind("<Leave>",self.unbound_to_mousewheel)

        self.canvas.create_window((0,0),window=self.second_frame,anchor=tk.NW)

        # self.sample_init()

        BagWindow.retrieve_bag()
        
        self.generate_bag_items()

        self.mainwindow = self.main_frame

        # self.master.protocol("WM_DELETE_WINDOW", self.update_list)
    
    def sample_init(self):
        BagWindow.list_bag.append(Food(1000,"Hello",quantity=1,price=199,image_path=f"{os.getcwd()}\\assets\\Appetizers\\Bagel Bites=79.png"))
        BagWindow.list_bag.append(Food(1000,"Hello",quantity=1,price=199,image_path=f"{os.getcwd()}\\assets\\Appetizers\\CHicken Buffalo=99.png"))
        BagWindow.list_bag.append(Food(1000,"Hello",quantity=1,price=199,image_path=f"{os.getcwd()}\\assets\\Appetizers\\Fries=69.png"))

    def generate_bag_items(self):

        if BagWindow.list_bag == []:
            messagebox.showerror("View Error","Your bag is empty!")
            self.master.destroy()
            return
        
        self.start_row = 1
        self.start_column = 0

        self.img_list = []

        for item in BagWindow.list_bag:
            self.img_list.append(ImageTk.PhotoImage(Image.open(item.get_image_path()).resize((263,150),Image.ANTIALIAS)))
                
        self.entry_references = []
        self.total_price_references = []
        self.current_quantity_references = []
        self.food_obj_references = []

        for food_item,img in zip(BagWindow.list_bag,self.img_list):
            self.food_item_label = tk.Label(self.second_frame)
            self.food_item_label["image"] = img
            
            self.food_item_label.grid(row=self.start_row,column=self.start_column)

            self.food_order_frame = tk.LabelFrame(self.second_frame)
            self.food_order_frame["width"] = 263
            self.food_order_frame["height"] = 150

            self.quantity_label = tk.Label(self.food_order_frame,text="Quantity: ")
            self.quantity_label["font"] = ("Arial",12)
            self.quantity_label.place(x=50,y=40)

            
            self.quantity_var = tk.StringVar(value=str(food_item.get_quantity()))
            self.quantity_value = tk.Entry(self.food_order_frame)
            self.quantity_value["textvariable"] = self.quantity_var
            self.quantity_value["state"] = "readonly"
            self.quantity_value.place(x=137.5,y=40,relheight=0.2,relwidth=0.2)

            self.total_price_label = tk.Label(self.food_order_frame,text="Total Price: ")
            self.total_price_label["font"] = ("Arial",12)
            self.total_price_label.place(x=50,y=80)

            self.price_var = tk.StringVar(value=str(food_item.get_price()))
            self.total_price_value = tk.Label(self.food_order_frame)
            self.total_price_value["textvariable"] = self.price_var
            self.total_price_value["font"] = ("Arial",12)
            self.total_price_value.place(x=140,y=80)

            self.remove_button = tk.Button(self.food_order_frame,text="Remove Item")
            self.remove_button["bg"] = "red"
            self.remove_button["fg"] = "white"
            self.remove_button["font"] = ("Arial",12)
            self.remove_button["command"] = lambda val=self.start_row-1: self.remove_action(val)
            self.remove_button.place(x=150,y=110)

            self.food_order_frame.grid(row=self.start_row,column=2)
            self.start_row += 1

            self.entry_references.append(self.quantity_var)
            self.total_price_references.append(self.total_price_value)

    def bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def remove_action(self,index):
        confirm = messagebox.askquestion("Remove item","Would you like to remove this item?")
        if confirm == "no":
            return

        self.update_list(BagWindow.list_bag[index].get_number())
        messagebox.showinfo("Item removed","Item has been successfully removed from your bag!")

    @classmethod
    def retrieve_bag(cls):
        print(f"BreakfastWindow list_bag at initilization:{BreakfastWindow.list_bag}")
        print(f"BurgersWindow list_bag at initilization:{BurgersWindow.list_bag}")
        print(f"ChickenWindow list_bag at initilization:{ChickenWindow.list_bag}")
        print(f"AppetizersWindow list_bag at initilization:{AppetizersWindow.list_bag}")
        print(f"BeveragesWindow list_bag at initilization:{BeveragesWindow.list_bag}")
        print(f"DessertsWindow list_bag at initilization:{DessertsWindow.list_bag}")

        cls.list_bag = []
        cls.list_bag.extend(BreakfastWindow.list_bag)
        cls.list_bag.extend(BurgersWindow.list_bag)
        cls.list_bag.extend(ChickenWindow.list_bag)
        cls.list_bag.extend(AppetizersWindow.list_bag)
        cls.list_bag.extend(BeveragesWindow.list_bag)
        cls.list_bag.extend(DessertsWindow.list_bag)

        for item in BagWindow.list_bag:
            print(item.get_number(),item.get_name(),item.get_quantity(),item.get_price())

    def update_info(self,index):
        for item in BagWindow.list:
            if self.food_obj_references[index].get_number() == item.get_number():
                self.current_quantity_references[index]["text"] = str(item.get_quantity())

    def update_list(self,remove_item_number):
        print("in update list")
        
        counter = 0
        for item in BreakfastWindow.list_bag:
            if item.get_number() == remove_item_number:
                del BreakfastWindow.list_bag[counter]
                print("removed")
                break
            counter += 1

        counter = 0
        for item in BeveragesWindow.list_bag:
            if item.get_number() == remove_item_number:
                del BeveragesWindow.list_bag[counter]
                print("removed")
                break
            counter += 1

        counter = 0
        for item in BurgersWindow.list_bag:
            if item.get_number() == remove_item_number:
                del BurgersWindow.list_bag[counter]
                print("removed")
                break
            counter += 1

        counter = 0
        for item in ChickenWindow.list_bag:
            if item.get_number() == remove_item_number:
                del ChickenWindow.list_bag[counter]
                print("removed")
                break
            counter += 1

        counter = 0
        for item in BreakfastWindow.list_bag:
            if item.get_number() == remove_item_number:
                del BreakfastWindow.list_bag[counter]
                print("removed")
                break
            counter += 1

        counter = 0
        for item in DessertsWindow.list_bag:
            if item.get_number() == remove_item_number:
                del DessertsWindow.list_bag[counter]
                print("removed")
                break
            counter += 1

        self.master.destroy()

    def run(self):
        self.mainwindow.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    BagWindow(root).run()