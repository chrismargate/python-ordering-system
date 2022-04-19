class Food:
    def __init__(self,number,name,price,quantity = 1,image_path = None):
        self.number = number
        self.name = name
        self.quantity = quantity
        self.price = price
        self.image_path = image_path

    def get_number(self):
        return self.number

    def set_number(self,number):
        self.number = number

    def get_name(self):
        return self.name
    
    def set_name(self,name):
        self.name = name

    def get_price(self):
        return self.price

    def set_price(self,price):
        self.price = price

    def get_quantity(self):
        return self.quantity
    
    def set_quantity(self,quantity):
        self.quantity = quantity
    
    def get_image_path(self):
        return self.image_path

    def set_image_path(self,image_path):
        self.image_path = image_path

    def __repr__(self):
        return f"{self.number}"