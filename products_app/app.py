#Assignment: Inventory Management App
#Author: mermaidinpython2018

import csv
import os

def menu(username="@prof-rossetti", products_count=100):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
    Please select an operation: """ # end of multi- line string. also using string interpolation
    return menu
#'Reset'   | Reset a csv product.


###professor example:

products = []

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"READING PRODUCTS FROM FILE: '{filepath}'")

    #TODO: open the file and populate the products list with product dictionaries
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            products.append(dict(row))
        return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id","name","aisle","department","price"])
        writer.writeheader() # uses fieldnames set above
        for p in products:
            writer.writerow(p)
    #TODO: open the file and write a list of dictionaries. each dict should represent a product.

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    print(len(products))
    write_products_to_file(filename, products)


def run():
    # First, read products from file...
    products = read_products_from_file()

    user = input("Please input username ")

    # Then, prompt the user to select an operation...
    number_of_products = len(products)
    menu_a = menu(username="@"+user, products_count=number_of_products) #TODO instead of printing, capture user input
    #operation = input(menu_a) #TODO instead of printing, capture user input
    #print("YOU CHOSE:" + operation)
    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    #TODO: handle selected operation

    crud_operation = input(menu_a).title()

    if crud_operation == "List":list_products(products)
    elif crud_operation == "Show":show_product(products)
    elif crud_operation == "Create":create_product(products)
    elif crud_operation == "Update":update_product(products)
    elif crud_operation == "Destroy":destroy_product(products)
    #elif crud_operation == "Reset":reset_products_file()
    else:
        print("OOPS SORRY. PLEASE TRY AGAIN.")

def list_products(products):
    print("-----------------------------------")
    print("LISTING PRODUCTS HERE")
    print("-----------------------------------")
    for product in products:
        print(" + Product #" + str(product["id"]) + ": " + product["name"])
    return products

def show_product(products):
    print("-----------------------------------")
    print("Showing a new product")
    print("-----------------------------------")
    product_id = input("OK. WHAT IS THE PRODUCT'S ID? ")
    product = [p for p in products if p["id"] == product_id][0]
    if product:
        print("READING PRODUCT HERE", product)
    else:
        print("COULDN'T FIND A PRODUCT WITH IDENTIFIER", product)

def get_product_id(product): return int(product["id"])

headers = ["id", "name", "aisle", "department", "price"]
user_input_headers = [header for header in headers if header != "id"]

def auto_incremented_id():
    product_ids = map(get_product_id, products)
    return max(product_ids) + 1

def create_product(products):
    print("-----------------------------------")
    print("Creating a new product")
    print("-----------------------------------")
    print("OK. PLEASE PROVIDE THE PRODUCT'S INFORMATION...")
    product = {"id": auto_incremented_id() }
    for header in user_input_headers:
        product[header] = input("The '{0}' is: ".format(header))
        while header=="price":
            if product[header].isalpha()==True:
                print("Wrong input! please enter a numeric number!")
                product[header] = input("The '{0}' is:".format(header))
                continue
            else:
                product[header]=round(float(product[header]),2)
                products.append(product)
                break
    print("CREATING PRODUCT HERE", product)
    write_products_to_file(products=products)
    # Finally, save products to file so they persist after script is done...


def update_product(products):
    print("-----------------------------------")
    print("Updating a new product")
    print("-----------------------------------")
    product_id = input("OK. WHAT IS THE PRODUCT'S ID? ")
    product = [p for p in products if p["id"] == product_id][0]
    if product:
        print("OK. PLEASE PROVIDE THE PRODUCT'S INFORMATION...")
        for header in user_input_headers:
            product[header] = input("Change '{0}' from '{1}' to: ".format(header, product[header]))
        print("UPDATING PRODUCT HERE", product)
    else:
        print("COULDN'T FIND A PRODUCT WITH IDENTIFIER", product_id)

# Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)

def destroy_product(products):
    print("-----------------------------------")
    print("Destorying a new product")
    print("-----------------------------------")
    product_id = input("OK. WHAT IS THE PRODUCT'S ID? ")
    product = [p for p in products if p["id"] == product_id][0]
    if product:
        print("DESTROYING PRODUCT HERE", product)
        del products[products.index(product)]
    else:
        print("COULDN'T FIND A PRODUCT WITH IDENTIFIER", product_id)
    write_products_to_file(products=products)


# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
