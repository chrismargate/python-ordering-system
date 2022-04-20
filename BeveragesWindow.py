from ProductCategoryWindow import ProductCategoryWindow
# from BagWindow import BagWindow

class BeveragesWindow(ProductCategoryWindow):

    list_bag = []

    def __init__(self,master=None):
        super().__init__(master)
        self.folder_name = "Beverages"
        self.food_id = 5000
        self.generate_product_items()
    
        self.master.protocol("WM_DELETE_WINDOW", self.update_list)

    def update_info_init(self,index):
        for item in BeveragesWindow.list_bag:
            if self.food_obj_references[index].get_number() == item.get_number():
                try:
                    self.current_quantity_references[index]["text"] = str(item.get_quantity())
                except IndexError as ie:
                    self.current_quantity_references[index]["text"] = str(0)
                    continue
     
    def update_list(self):
        temp_list = []
        duplicate = False
        for instance_item in self.list_bag_instance:
            duplicate = False
            if BeveragesWindow.list_bag == []:
                temp_list.append(instance_item)
                continue
            for class_item in BeveragesWindow.list_bag:
                if instance_item.get_number() == class_item.get_number():
                    class_item.set_quantity(instance_item.get_quantity()+class_item.get_quantity())
                    class_item.set_price(instance_item.get_price()+class_item.get_price())
                    print("duplicate")
                    duplicate = True
                    continue
            if duplicate == False:
                temp_list.append(instance_item)

        print("in")
        print(temp_list)
        BeveragesWindow.list_bag.extend(temp_list)
        self.master.destroy()