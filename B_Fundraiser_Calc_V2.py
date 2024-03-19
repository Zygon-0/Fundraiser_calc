import time
import pandas as pd

# import needed functions
from _Functions.F_int_checker import int_check as ic

from _Functions.F_float_checker import float_check as fc

from _Functions.F_choice_checker import choice_checker as cc, yes_no_list

from _Functions.F_Not_Blank import not_blank as nb

from _Functions.F_currency import currency as cur

from _Functions.F_statement_generator_v3 import statement_generator as sg


def get_expenses(var_fixed):
    # sets up dictionaries and lists
    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

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
        if var_fixed == "variable":
            quantity_num = ic("Item Quantity: ", low=1)
        else:
            quantity_num = 1

        # get price
        price_num = fc("Item Price: ", low=1)

        # add item, quantity and price to list
        item_list.append(item_name)
        quantity_list.append(quantity_num)
        price_list.append(price_num)

        # just for nice formatting
        print("----------")

    expense_frame = pd.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']
    expense_cost = expense_frame['Cost']

    # Find sub-total
    expense_sub = expense_frame['Cost'].sum()

    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(cur)

    expense_frame_list = {
        "Item": item_list,
        "Cost": expense_cost}

    expense_fixed_frame = pd.DataFrame(expense_frame_list)
    expense_fixed_frame = expense_fixed_frame.set_index('Item')

    # just for nice formatting
    print()
    print("--------------------")
    print()

    if var_fixed == "variable":
        return [expense_frame, expense_sub]
    else:
        return [expense_fixed_frame, expense_sub]


# mian routine

# printing tittle
sg("Fundraiser Calculator", "+#", 3)
print()

product_name = nb("Product Name: ")

# get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

# get fixed costs
fixed_expenses = get_expenses("fixed")
fixed_frame = fixed_expenses[0]
fixed_sub = fixed_expenses[1]


# **** Printing Area ****

print("*_____ Variable Costs ____*")
print()
print(variable_frame)
print()
print(f"Variable Costs: {cur(variable_sub)}")
print()
print("*____ Fixed Costs ____*")
print()
print(fixed_frame)
print()
print(f"Fixed Costs: {cur(fixed_sub)}")
