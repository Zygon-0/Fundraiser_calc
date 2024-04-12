import math
import time
import pandas as pd

# import needed functions
from _Functions.F_int_checker import int_check as ic

from _Functions.F_float_checker import float_check as fc

from _Functions.F_choice_checker import choice_checker as cc, yes_no_list

from _Functions.F_Not_Blank import not_blank as nb

from _Functions.F_currency import currency as cur

from _Functions.F_statement_generator_v3 import statement_generator as sg


def costs_printing(variable_fixed, _frame, _sub):
    print(f"*_____ {variable_fixed} Costs ____*")
    print()
    print(_frame)
    print()
    print(f"{variable_fixed} Costs: {cur(_sub)}")
    print()


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

    print()

    # just for nice formatting
    if var_fixed == "variable":
        print("------ Variable  Costs ------")
        print("(item; Name, quantity, price)")
    else:
        print("-------- Fixed Costs --------")
        print("---- (item; Name, price) ----")

    print("-----------------------------")
    print()
    print("type \"xxx\" in \"Item Name\" when done")

    if var_fixed == "variable":
        print("Do not put down items with a quantity")
        print("of 1 (this will be done next)")
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
            quantity_num = ic("Item Quantity: ", low=2)
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

    fixed_dict = {
        "Item": item_list,
        "Cost": expense_cost}

    expense_fixed_frame = pd.DataFrame(fixed_dict)
    expense_fixed_frame = expense_fixed_frame.set_index('Item')

    # just for nice formatting
    print()
    print("-----------------------------")

    if var_fixed == "variable":
        return [expense_frame, expense_sub]
    else:
        return [expense_fixed_frame, expense_sub]


def profit_goal(total_costs):

    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:
        # ask for profit goal...
        response = input("how much profit would you like to make(as $ or %): ")

        # check if first character is $
        if response[0] == "$":
            profit_type = "$"
            amount = float(response[1:])

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            amount = float(response[:-1])

        else:
            profit_type = "?"
            amount = float(response)

        try:
            # check amount is a number more than 0
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "?" and amount >= 100:
            print()
            dollar_type = cc(f"Do you mean ${amount:.2f}? ie {amount:.2f} dollars, y/n: ", yes_no_list,
                             "Please enter yes or no as your response", 1)

            # Set profit type based on users response above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "?" and amount < 100:
            print()
            dollar_type = cc(f"Do you mean {amount:.0f}%? ie {amount:.0f} percent, y/n: ", yes_no_list,
                             "Please enter yes or no as your response", 1)

            # Set profit type based on users response above
            if dollar_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to the main routine
        if profit_type == "$":
            return amount
        else:
            goal_1 = (amount / 100) * total_costs
            return goal_1


def round_up(amount, rounded_to):
    return int(math.ceil(amount / rounded_to)) * rounded_to


# mian routine

# printing tittle
sg("Fundraiser Calculator", "+#", 3)
print()

product_name = nb("What is Your Products Name: ")

how_many = ic("How Many Items Will You be Producing: ")

# get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

have_fixed = cc("do you have fixed costs (ie items with a quantity of one): ", yes_no_list,
                "please input yes or no (or y / n)", 1)

if have_fixed == "yes":
    # get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
    all_costs = fixed_sub + variable_sub
else:
    all_costs = variable_sub

print()
goal = profit_goal(all_costs)
print()

# calculate recommended price
selling_price = 0

round_to = ic("what do you want it rounded to ie 53; 53(1), 55(5), 60(10): ", 0, 1000)

rounded = round_up(goal / how_many, round_to)
required_sales = cur(all_costs + goal)
minimum = goal / how_many

# **** Printing Area ****

print(f"*_____ Fund Raising - {product_name} _____*\n\n")

costs_printing("Variable", variable_frame, variable_sub)
if have_fixed == "yes":
    costs_printing("Fixed", fixed_frame, fixed_sub)
print()

print(f"*_____ Total costs: {cur(all_costs)} _____*")
print()
print(f"*_____Profit & Sales Targets_____*")
print(f"Profit Target: {cur(goal)}")
print(f"Total Sales Needed: {required_sales}")
print()

print("*_____ Selling _____*")
print(f"Minimum Sell Price: {minimum}")
print(f"Recommended Selling Price: {rounded}")

# write text to file
variable_txt = pd.DataFrame.to_string(variable_frame)
fixed_txt = pd.DataFrame.to_string(fixed_frame)
file_name = f"{product_name}.txt"
text_file = open(file_name, "w+")

to_write = [f"Product: {product_name}\n", "Variable Costs", variable_txt, f"Total: {cur(variable_sub)}\n",
            "Fixed Costs", fixed_txt, f"Total: {cur(fixed_sub)}\n", f"Grand Total: {cur(all_costs)}\n",
            "Profit & Sales Targets", f"Profit Target: {cur(goal)}", f"Total Sales Needed: {required_sales}\n",
            "Selling", f"Minimum Sell: {cur(minimum)}", f"Recommended Sell: {cur(rounded)}"]

for i in to_write:
    print(i)
    print()
    text_file.write(i)
    text_file.write("\n")


text_file.close()
