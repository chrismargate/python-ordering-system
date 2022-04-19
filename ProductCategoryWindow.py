import os
from PIL import ImageTk,Image
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from Food import Food
from copy import deepcopy

class ProductCategoryWindow:

    def __init__(self,master=None):
        self.folder_name = ""
        self.food_id = 0
        self.list_bag_instance = []

        self.master = master
        self.master.geometry("550x700")
        self.master.resizable(False,False)

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH,expand=1)

        self.start_row = 1
        self.start_column = 0

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

        # self.generate_product_items()

        self.mainwindow = self.main_frame

    def generate_product_items(self):
        # print(f"List_bag_instance before generate: {self.list_bag_instance}")
        self.master.title(self.folder_name)
        self.img_list = []
        self.list_imgs = os.listdir(os.getcwd() + f"\\assets\\{self.folder_name}")

        for img in self.list_imgs:
            if img.endswith(".png"):
                self.img_list.append(ImageTk.PhotoImage(Image.open(f"{os.getcwd()}\\assets\\{self.folder_name}\\{img}").resize((263,150),Image.ANTIALIAS)))
                
        self.entry_references = []
        self.total_price_references = []
        self.current_quantity_references = []
        self.food_obj_references = []

        counter = 0
        counter_2 = 0
        for img in self.list_imgs:
            if img.endswith(".png"):
                temp_string = img.replace(".png","").split("=")
                img_path = f"{os.getcwd()}\\assets\\{self.folder_name}\\{img}"
                food_obj = Food(self.food_id+counter,temp_string[0],int(temp_string[1]),image_path = img_path)
                # food_obj.set_image(self.img_list[counter])
                self.food_obj_references.append(food_obj)
                del food_obj
                counter += 1
            counter_2 += 1

        for img in self.img_list:
            self.food_item_label = tk.Label(self.second_frame)
            self.food_item_label["image"] = img
            
            self.food_item_label.grid(row=self.start_row,column=self.start_column)

            self.food_order_frame = tk.LabelFrame(self.second_frame)
            self.food_order_frame["width"] = 263
            self.food_order_frame["height"] = 150

            self.current_quantity_label = tk.Label(self.food_order_frame,text="Current Bag Quantity: ")
            self.current_quantity_label["font"] = ("Arial",12)
            self.current_quantity_label.place(x=30,y=20)

            self.current_quantity_value = tk.Label(self.food_order_frame,text="0")
            self.current_quantity_value["font"] = ("Arial",12)
            self.current_quantity_value.place(x=180,y=20)

            self.quantity_label = tk.Label(self.food_order_frame,text="Quantity: ")
            self.quantity_label["font"] = ("Arial",12)
            self.quantity_label.place(x=30,y=60)

            self.minus_button = tk.Button(self.food_order_frame,text="-")
            self.minus_button["command"] = lambda val=self.start_row-1: self.minus_action(val)
            self.minus_button.place(x=120,y=60)
            
            self.quantity_var = tk.StringVar(value="0")
            self.quantity_value = tk.Entry(self.food_order_frame)
            self.quantity_value["textvariable"] = self.quantity_var
            self.quantity_value["state"] = "readonly"
            self.quantity_value.place(x=137.5,y=60,relheight=0.2,relwidth=0.2)

            self.plus_button = tk.Button(self.food_order_frame,text="+")
            self.plus_button["command"] = lambda val=self.start_row-1: self.plus_action(val)
            self.plus_button.place(x=180,y=60)

            self.total_price_label = tk.Label(self.food_order_frame,text="Total Price: ")
            self.total_price_label["font"] = ("Arial",12)
            self.total_price_label.place(x=30,y=100)

            self.total_price_value = tk.Label(self.food_order_frame,text="0")
            self.total_price_value["font"] = ("Arial",12)
            self.total_price_value.place(x=120,y=100)

            self.addtobag_button = tk.Button(self.food_order_frame,text="Add to Bag")
            self.addtobag_button["bg"] = "red"
            self.addtobag_button["fg"] = "white"
            self.addtobag_button["font"] = ("Arial",12)
            self.addtobag_button["command"] = lambda val=self.start_row-1: self.addtobag_action(val)
            self.addtobag_button.place(x=162.5,y=110)

            self.food_order_frame.grid(row=self.start_row,column=2)
            # self.update_info(self.start_row-1)

            self.current_quantity_references.append(self.current_quantity_value)
            self.entry_references.append(self.quantity_var)
            self.total_price_references.append(self.total_price_value)
            
            self.update_info_init(self.start_row-1)
            self.start_row += 1

    def bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def plus_action(self,index):
        entry_string = self.entry_references[index].get()
        entry_int = int(entry_string) + 1
        if entry_int >= 100:
            messagebox.showerror("Order Quantity Error","Maximum quantity reached!")
            return
        entry_string = str(entry_int)
        self.entry_references[index].set(entry_string)

        totals_label_int = entry_int * self.food_obj_references[index].get_price()
        totals_label_string = str(totals_label_int)

        self.total_price_references[index]["text"] = totals_label_string

    def minus_action(self,index):
        entry_string = self.entry_references[index].get()
        entry_int = int(entry_string) - 1
        if entry_int < 0:
            messagebox.showerror("Order Quantity","Minimum quantity reached!")
            return
        entry_string = str(entry_int)
        self.entry_references[index].set(entry_string)

        totals_label_string = self.total_price_references[index]["text"]
        totals_label_int = int(totals_label_string)
        totals_label_int = int(self.entry_references[index].get()) * self.food_obj_references[index].get_price()
        totals_label_string = str(totals_label_int)

        self.total_price_references[index]["text"] = totals_label_string

    def addtobag_action(self,index):
        if self.entry_references[index].get() == "0":
            messagebox.showerror("Add to Bag","Must have at least 1 item quantity to add to bag")
            return

        confirm_question = messagebox.askquestion("Add to Bag","Are you sure you want to add this to your bag?")
        if confirm_question == "no":
            return

        food_obj = deepcopy(self.food_obj_references[index])
        food_obj.set_quantity(0)
        food_obj.set_price(0)

        counter = 0
        for item in self.list_bag_instance:
            if item.get_number() == food_obj.get_number():
                temp_list = self.list_bag_instance
                item.set_quantity(item.get_quantity()+int(self.entry_references[index].get()))
                item.set_price(item.get_price()+int(self.total_price_references[index]["text"]))
                if item.get_quantity() >= 100:
                    messagebox.showerror("Add to Bag","Quantity you want to add to cart exceeds the 100 quantity limit")
                    return
                temp_list[counter] = item
                self.list_bag_instance = temp_list
                self.update_info(index)
                self.reset_quantity_entry(index)

                # for item in self.list_bag_instance:
                #     print(item.get_number(),item.get_name(),item.get_quantity(),item.get_price())
                return
            counter += 1
        food_obj.set_quantity(int(self.entry_references[index].get()))
        food_obj.set_price(food_obj.get_price() + int(self.total_price_references[index]["text"]))
        self.list_bag_instance.append(food_obj)

        self.update_info(index)
        self.reset_quantity_entry(index)

        # print(f"List_bag_instance after add to bag: {self.list_bag_instance}")
        
    def reset_quantity_entry(self,index):
        self.entry_references[index].set("0")
        self.total_price_references[index]["text"] = "0"

    def update_info(self,index):
        for item in self.list_bag_instance:
            if self.food_obj_references[index].get_number() == item.get_number():
                self.current_quantity_references[index]["text"] = str(item.get_quantity())
    

    def update_info_init(self,index):
        pass

    def update_list(self):
        pass
    
    def get_list_bag(self):
        return self.list_bag_instance

    def run(self):
        self.mainwindow.mainloop()