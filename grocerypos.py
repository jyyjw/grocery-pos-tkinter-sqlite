from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import sqlite3

window = Tk()
window.geometry('475x250+550+250')
window.configure(bg="#B6C4D6")

def add_product(conn, product):
    sql = ''' INSERT INTO products(name,price)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, product)
    conn.commit()
    return cur.lastrowid

def add_customer(conn, customer):
    sql = ''' INSERT INTO customers(name,phone)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid

# region add products
# try:
#     with sqlite3.connect('grocery.db') as conn:

#      # region Grocery Products List
#         products = [
#             ('Cereal', 10.99),
#             ('Milk 1L', 4.50),
#             ('Loaf of Bread', 3.25),
#             ('Eggs (Dozen)', 5.99),
#             ('Apples (1kg)', 6.40),
#             ('Bananas (Bunch)', 3.50),
#             ('Chicken Breast (500g)', 12.00),
#             ('Pasta (500g)', 2.10),
#             ('Rice (1kg)', 4.75),
#             ('Ground Beef (500g)', 9.50),
#             ('Cheddar Cheese', 7.20),
#             ('Greek Yogurt', 5.50),
#             ('Coffee Beans', 14.99),
#             ('Orange Juice', 4.80),
#             ('Potato Chips', 3.99),
#             ('Bottled Water (6pk)', 6.50),
#             ('Tomato Sauce', 3.20),
#             ('Butter', 6.25),
#             ('Frozen Pizza', 8.99),
#             ('Peanut Butter', 5.30)
#         ]
#     # endregion
#         for product in products:
#             product_id = add_product(conn, product)
#             print(f'Created product with the id {product_id}')

# except sqlite3.Error as e:
#      print(e)

# endregion 

# region add contacts
# try:
#     with sqlite3.connect('grocery.db') as conn:

#         customers = [
#                 ('Jungwon', '2531234567'), ('Heeseung', '2223334455'),('Jay', '5075811228'), ('Jake', '1233341234'),
#                 ('Sunghoon','1233345678'), ('Sunoo','2342233344'), ('Niki', '2332349890')
#         ]
#         for customer in customers:
#             customer_id = add_customer(conn, customer)
#             print(f'Created customer with the id {customer_id}')


# except sqlite3.Error as e:
#     print(e)
# endregion 

class GroceryPOS():
    def __init__(self):

        # Initialize all the tkinter widgets

        self.customer_label = Label(window, text="Customer Lookup", foreground='#445969', 
                                    font=('Skynight', 20), background='#B6C4D6',)
        self.customer_label.grid(row=0, column=1, pady=8)
        self.new_customer_button = Button(window, text="New Customer",background='#FFFFFF', font=('Skynight', 10), command=self.new_customer)
        self.new_customer_button.grid(row= 0, column= 2, pady = 8)
        self.customer_entry_var = StringVar()
        self.customer = ""
        self.customer_var = StringVar()
        self.customers = []
        self.cart = []
        self.customer_list = []
        self.customer_id = ""
        self.search_label = Label(text="Name or Phone",
                                    foreground='#445969', 
                                    font=('Skynight', 12), background='#B6C4D6')
        self.search_label.grid(row=1, column=0, padx=4)
        self.customer_cb_var = StringVar()
        self.customers_combobox = ttk.Combobox(window, width= 27, textvariable=self.customer_cb_var)
        self.customers_combobox.current()
        self.customer_label2 = Label(window, text= f"Hi {self.customer}!", font=('Skynight', 10), textvariable=self.customer_var)
        self.customer_select = Button(window, text="Select Customer", font=('Skynight', 10), command=self.select_customer)
        self.search_var = StringVar()
        self.search_entry = Entry(window, textvariable=self.search_var, width= 33, font='Skynight')
        self.search_entry.grid(row=1, column=1, pady=2, padx=2)
        self.search_button = Button(window, text='Search', font=('Skynight', 12), background='#FFFFFF', command=self.search_customer)
        self.search_button.grid(row=1, column=2, padx=5)

        # Product Search Widgets

        self.products_label = Label(window, text="Search Products",foreground='#445969', 
                                    font=('Skynight', 20), background='#B6C4D6', pady=15)
        self.products_label.grid(row=2, column=1, pady=2)
        self.products_entry_var = StringVar()
        #self.products = []
        self.products_list = []
        self.products_search_label = Label(window, text="Product name", foreground='#445969', 
                                    font=('Skynight', 14), background='#B6C4D6')
        self.products_search_var = StringVar()
        self.products_search_entry = Entry(window, textvariable=self.products_search_var, width=33, font='Skynight')
        self.products_search_label.grid(row=3, column=0, padx=4)
        self.products_search_entry.grid(row=3, column=1)
        self.products_search_button = Button(window, text="Search", foreground='#445969', 
                                    font=('Skynight', 12), background='White', command=self.search_product)
        self.products_search_button.grid(row=3, column=2, padx=5)
        self.product_results = ttk.Combobox(window, values=self.products_list, font=('Skynight', 15), width=10 )
        self.cart_text = f"Cart amount: {len(self.cart)}"

        # Cart Widgets

        self.cart_number_var = StringVar(value=self.cart_text)
        self.cart_number_label = Button(window, textvariable=self.cart_number_var, text=self.cart_text, foreground='#445969', 
                                    font=('Skynight', 11), background='#B6C4D6', command=self.view_cart)
        # self.cart_number_label = Label(window, textvariable=self.cart_number_var, text=self.cart_text, foreground='#445969', 
        #                             font=('Skynight', 11), background='#B6C4D6')
        self.cart_number_label.grid(row=0, column=0)
        self.customer_results = ttk.Combobox(window, values=self.customer_list, font=('Skynight', 15), width=10 )
        self.product_select = Button(window, text="Add to cart", font=('Skynight', 10), command=self.add_product)

        # New customer Widgets

        self.new_customer_title = Label(window, text="Create new customer", foreground='#445969', 
                                    font=('Skynight', 20), background='#B6C4D6' )
        self.new_customer_firstname_label = Label(window, text="First name: ", foreground='#445969', 
                                    font=('Skynight', 12), background='#B6C4D6')
        self.new_customer_lastname_label = Label(window, text="Last name: ", foreground='#445969', 
                                    font=('Skynight', 12), background='#B6C4D6')
        self.new_customer_firstentry_var = StringVar()
        self.new_customer_firstentry = Entry(window, textvariable=self.new_customer_firstentry_var, width=20, font='Skynight')
        self.new_customer_lastentry_var = StringVar()
        self.new_customer_lastentry = Entry(window, textvariable=self.new_customer_lastentry_var, width=20, font='Skynight')
        self.new_customer_phone_label = Label(window, text="Phone Number: ", foreground='#445969', 
                                    font=('Skynight', 12), background='#B6C4D6')
        self.new_customer_phoneentry_var = StringVar()
        self.new_customer_phoneentry = Entry(window, textvariable=self.new_customer_phoneentry_var, width=20, font='Skynight')
        self.new_customer_submit_button = Button(window, text="Submit", command=self.submit_new_customer,foreground='#445969', 
                                    font=('Skynight', 12), background='White')
        self.new_customer_back_button = Button(window, text="Back", background='#FFFFFF', font=('Skynight', 10), command=self.new_customer_back)

    def search_product(self):
        self.products_list = []
        try:
            input = self.products_search_entry.get()
            if len(input) == 0:
                messagebox.showerror("Error", "Search cannot be empty")
                return

            window.geometry('770x250+550+250')
            search_term = f"%{input}%"
            with sqlite3.connect('grocery.db') as connection:
                cursor = connection.cursor()
                sql = "SELECT name from products WHERE name LIKE ?"

                cursor.execute(sql, (search_term,))

                products = cursor.fetchall()

                for product in products:
                    self.products_list.append(product)

                self.product_results.config(values= self.products_list)
                self.product_results.grid(row=3, column=4)
                self.product_results.current(0)
                self.product_select.grid(row=3, column=5, padx=5)
        except TclError as e:
            messagebox.showerror("Error", "No results for that name")
            window.geometry('475x250+550+250')
            self.product_results.grid_forget()
            print(f"An error occurred: {e}")

    def search_customer(self):
        self.customer_list = []
        try:
            input = self.search_entry.get()
            if len(input) == 0:
                messagebox.showerror("Error", "Search cannot be empty")
                return
            
            window.geometry('770x250+550+250')
            search_term = f"%{input}%"
            
            with sqlite3.connect('grocery.db') as connection:
                cursor = connection.cursor()
                sql = "SELECT name FROM customers WHERE name LIKE ?"

                cursor.execute(sql, (search_term,))

                customers = cursor.fetchall()

                for customer in customers:
                    self.customer_list.append(customer)

                self.customer_results.config(values= self.customer_list)
                self.customer_results.grid(row=1, column=4)
                self.customer_results.current(0)
                
                self.customer_select.grid(row=1, column=5, padx=5)
        except TclError as e:
            messagebox.showerror("Error", "No results for that name")
            window.geometry('400x350+550+250')
            self.customer_results.grid_forget()
            print(f"An error occurred: {e}")
            
    def add_product(self):
        try:
            product = self.product_results.get()
            product = product[1:-1]
            search_term = f"%{product}%"
            
            self.products_search_var.set("")
            self.product_results.grid_forget()
            self.product_select.grid_forget()
            window.geometry('475x250+550+250')

            with sqlite3.connect('grocery.db') as connection:
                    
                    cursor = connection.cursor()
                    sql = "SELECT id from products WHERE name LIKE ?"

                    cursor.execute(sql, (search_term,))

                    id = cursor.fetchone()
                    product_id = id[0]

                    self.cart.append(product_id)
                
            print(f"Product id: {product_id}, Total Products {self.cart}")
            self.cart_number_var.set(value=f"Cart amount: {len(self.cart)}")

        except TypeError as e:
            print(f"Error: {e}")

    def select_customer(self):
        self.new_customer_button.grid_forget()
        self.customer_select.grid_forget()
        window.geometry('475x250+550+250')
        self.customer = self.customer_results.get()
        self.customer_var.set(f"Hi {self.customer}!")
        self.customer_results.grid_forget()
        print(self.customer)
        self.customer_label2.grid(row= 0, column= 2, pady = 8)
        self.search_var.set("")

        with sqlite3.connect('grocery.db') as connection:
                
                cursor = connection.cursor()
                sql = "SELECT id from customers WHERE name = ?"

                cursor.execute(sql, (self.customer,))

                id = cursor.fetchone()
                self.customer_id = id[0]
            
        print(f"customer id: {self.customer_id}")

        return self.main_screen_customer_selected()

    def new_customer(self):
        for widget in window.winfo_children():
            widget.grid_forget()
        self.new_customer_title.grid(row=0, column=1, pady=8)
        self.new_customer_firstname_label.grid(row=1, column=0, padx=4)
        self.new_customer_firstentry.grid(row=1, column=1, pady=2, padx=2)
        self.new_customer_back_button.grid(row=0, column=0)
        self.new_customer_lastname_label.grid(row=2, column=0, padx=4)
        self.new_customer_lastentry.grid(row=2, column=1, pady=2, padx=2)
        self.new_customer_phone_label.grid(row=3, column=0, padx=4)
        self.new_customer_phoneentry.grid(row=3, column=1, pady=2, padx=2)
        self.new_customer_submit_button.grid(row=4, column=1, pady=15)
     
    def submit_new_customer(self):
        first_name = self.new_customer_firstentry.get()
        last_name = self.new_customer_lastentry.get()
        phone = self.new_customer_phoneentry.get()

        print(f"First name: {first_name} \n Last name: {last_name} \n Phone: {phone}")
        for widget in window.winfo_children():
            widget.grid_forget()
        
        messagebox.showinfo("Customer Created", f"Created Customer with Name {first_name} {last_name} and Phone {phone}") 

        return self.main_screen()
    
    def new_customer_back(self):
        for widget in window.winfo_children():
            widget.grid_forget()
        
        return self.main_screen()
    
    def main_screen(self):

        self.search_button.grid(row=1, column=2, padx=5)
        self.products_label.grid(row=2, column=1, pady=2)
        self.products_search_label.grid(row=3, column=0, padx=4)
        self.products_search_entry.grid(row=3, column=1)
        self.products_search_button.grid(row=3, column=2, padx=5)
        self.cart_number_label.grid(row=0, column=0)
        self.search_entry.grid(row=1, column=1, pady=2, padx=2)
        self.search_label.grid(row=1, column=0, padx=4)
        self.new_customer_button.grid(row= 0, column= 2, pady = 8)
        self.customer_label.grid(row=0, column=1, pady=8)

    def main_screen_customer_selected(self):
        for widget in window.winfo_children():
            widget.grid_forget()
        self.customer_label2.grid(row= 0, column= 2, pady = 8)
        self.products_label.grid(row=0, column=1, pady=2)
        self.products_search_label.grid(row=3, column=0, padx=4)
        self.products_search_entry.grid(row=3, column=1)
        self.products_search_button.grid(row=3, column=2, padx=5)
        self.cart_number_label.grid(row=0, column=0)

    def id_to_name(self, id):
        with sqlite3.connect('grocery.db') as connection:                    
                    cursor = connection.cursor()
                    sql = "SELECT name from products WHERE id = ?"
                    cursor.execute(sql, (id,))
                    id = cursor.fetchone()
                    return id[0]

    def view_cart(self):
        item_list =[]

        if len(self.cart) == 0:
            messagebox.showerror("Error", "!cart is empty!")
            return

        for item in self.cart:
            print(type(item))
            item_list.append(self.id_to_name(item))

        top= Toplevel(window)
        top.geometry('300x200+700+250')
        top.title("Cart")
        top.configure(bg="#B6C4D6")
        top.title_label = Label(top, text= "Items in cart", font=('Skynight', 20), background='#B6C4D6', foreground='#445969')
        top.title_label.grid(row= 0, column=5)
        top.message = Message(top, text=f"{', '.join(item_list)}", background="#B6C4D6", foreground='#445969', font=('Skynight', 10))
        top.message.grid(row= 1, column=5)
        top.close_button = Button(text="Close", command=lambda: top.destroy(), font=('Skynight', 15))
        top.close_button.grid(row=2, column=5)

app = GroceryPOS()
window.mainloop()
