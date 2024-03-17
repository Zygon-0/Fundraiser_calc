import time
import pandas as pd

# import needed functions
from _Functions.F_int_checker import int_check as ic

from _Functions.F_float_checker import float_check as fc

from _Functions.F_choice_checker import choice_checker as cc, yes_no_list

from _Functions.F_Not_Blank import not_blank as nb

from _Functions.F_currency import currency as cur

from _Functions.F_statement_generator_v3 import statement_generator as sg

# preset variables

# sets up dictionaries and lists
item_list = []
quantity_list = []
price_list = []

variable_dict = {
    "Item": item_list,
    "Quantity": quantity_list,
    "Price": price_list
}

# mian routine

# printing tittle
sg("Fundraiser Calculator", "+#", 3)
print()

product_name = nb("Product Name: ")

# just for nice formatting
print()
print("--------------------")
print()

# loop for component, quantity and price
item_name = ""

while item_name.lower() != "xxx":

    # get name
    item_name = nb("Item Name: ")
    if item_name.lower() == "xxx":
        break

    # get quantity
    quantity_num = ic("Item Quantity: ", low=1)

    # get price
    price_num = fc("Item Price: ", low=1)

    # add item, quantity and price to list
    item_list.append(item_name)
    quantity_list.append(quantity_num)
    price_list.append(price_num)

    # just for nice formatting
    print("----------")

# just for nice formatting
print()
print("--------------------")
print()

variable_frame = pd.DataFrame(variable_dict)
variable_frame = variable_frame.set_index('Item')

# Calculate cost of each component
variable_frame['Cost'] = variable_frame['Quantity'] * variable_frame['Price']

# Find sub-total
variable_sub = variable_frame['Cost'].sum()

add_dollars = ['Price', 'Cost']
for item in add_dollars:
    variable_frame[item] = variable_frame[item].apply(cur)

# **** Printing Area ****

print(variable_frame)
print()
print(f"Variable Costs: {cur(variable_sub)}")
