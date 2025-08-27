import json
from datetime import datetime

def readFile():
    file = open("inventory.json", "r")
    data = json.load(file)
    file.close()
    return data

def writeFile(data):
    file = open("inventory.json", "w")
    json.dump(data, file, indent=2)
    file.close()

def writeLog(message):
    file = open("logs.txt", "a")
    file.write(message + "\n")
    file.close()

def getCurrentTime():
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return time_string

def printDepartment(dept_name, items):
    print("\n" + dept_name.upper() + " DEPARTMENT:")
    print("-" * 25)
    
    for item_key in items:
        item = items[item_key]
        print("• " + item["name"])
        print("  Price: $" + str(item["price"]))
        print("  Stock: " + str(item["count"]) + " units")
        print()

def buyItem(inventory):
    user_name = input("Enter your name: ")
    
    print("\nAvailable items:")
    for dept_key in inventory:
        for item_key in inventory[dept_key]:
            item = inventory[dept_key][item_key]
            print(item_key + " - " + item["name"] + " ($" + str(item["price"]) + ")")
    
    item_to_buy = input("\nEnter item name: ")
    quantity = int(input("Enter quantity: "))
    
    purchase_time = getCurrentTime()

    # Find and update item in the json
    for dept_key in inventory:
        if item_to_buy in inventory[dept_key]:
            item = inventory[dept_key][item_to_buy]
            if item["count"] >= quantity:
                item["count"] = item["count"] - quantity
                total_price = item["price"] * quantity
                
                # Create log message
                log_message = purchase_time + " - " + user_name + " bought " + str(quantity) + " " + item["name"] + " for $" + str(total_price)
                
                print("Purchase successful!")
                print("Total cost: $" + str(total_price))
                
                # Save to files
                writeFile(inventory)
                writeLog(log_message)
                
                return
            else:
                # Log failed purchase
                fail_message = purchase_time + " - " + user_name + " tried to buy " + str(quantity) + " " + item["name"] + " but not enough stock"
                writeLog(fail_message)
                print("Not enough stock!")
                return
    
    # Log item not found
    not_found_message = purchase_time + " - " + user_name + " tried to buy " + item_to_buy + " but item not found"
    writeLog(not_found_message)
    print("Item not found!")

def main():
    inventory = readFile()
    
    print("=" * 40)
    print("INVENTORY SYSTEM")
    print("=" * 40)
    
    for dept_key in inventory:
        dept_items = inventory[dept_key]
        printDepartment(dept_key, dept_items)
    
    # Add purchase option
    print("\n" + "=" * 40)
    buy_choice = input("Do you want to buy something? (y/n): ")
    if buy_choice == "y":
        buyItem(inventory)

print("Reading")
main()