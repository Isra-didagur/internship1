INVENTORY = []
next_id = 1

def display_menu():
    """Prints the main menu options to the console."""
    print("\n" + "="*40)
    print("    INVENTORY MANAGER CONSOLE APP")
    print("="*40)
    print("1. Add New Item (Create)")
    print("2. View All Inventory (Read)")
    print("3. Update Item Name or Quantity (Update)")
    print("4. Delete Item (Delete)")
    print("5. Exit")
    print("="*40)

def view_inventory():
    """Displays all items in the inventory with their details."""
    if not INVENTORY:
        print("\n[INFO] The inventory is currently empty.")
        return

    print("\n--- Current Inventory ---")
    print("{:<5} {:<10} {}".format("ID", "Quantity", "Item Name"))
    print("-" * 40)

    for item in INVENTORY:
        print(f"{item['id']:<5} {item['quantity']:<10} {item['name']}")

    print("-" * 40)

def add_item():
    """Prompts the user for item details and adds it to the inventory."""
    global next_id
    item_name = input("Enter the NAME of the new item: ").strip()
    
    if not item_name:
        print("\n[ERROR] Item name cannot be empty.")
        return
        
    try:
        quantity = int(input(f"Enter the starting QUANTITY for '{item_name}': "))
        if quantity < 0:
            print("\n[ERROR] Quantity must be zero or a positive number.")
            return
    except ValueError:
        print("\n[ERROR] Invalid quantity. Please enter a whole number.")
        return

    new_item = {
        'id': next_id,
        'name': item_name,
        'quantity': quantity
    }
    INVENTORY.append(new_item)
    print(f"\n[SUCCESS] Item '{item_name}' (ID: {next_id}, Qty: {quantity}) added to inventory.")
    next_id += 1

def get_item_by_id(item_id):
    """Helper function to find an item by its unique ID."""
    for item in INVENTORY:
        if item['id'] == item_id:
            return item
    return None

def update_item():
    """Allows the user to modify an item's name or quantity."""
    view_inventory()
    if not INVENTORY:
        return

    try:
        item_id = int(input("Enter the ID of the item you want to update: "))
    except ValueError:
        print("\n[ERROR] Invalid ID. Please enter a number.")
        return

    item_to_update = get_item_by_id(item_id)

    if item_to_update:
        print(f"\nEditing Item ID: {item_id} ('{item_to_update['name']}', Qty: {item_to_update['quantity']})")
        print("1. Change Item Name")
        print("2. Change Quantity")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            new_name = input("Enter the new item name: ").strip()
            if new_name:
                item_to_update['name'] = new_name
                print(f"\n[SUCCESS] Item ID {item_id} name updated to '{new_name}'.")
            else:
                print("\n[ERROR] Name cannot be empty. No change made.")
        elif choice == '2':
            try:
                new_quantity = int(input("Enter the new quantity: "))
                if new_quantity >= 0:
                    item_to_update['quantity'] = new_quantity
                    print(f"\n[SUCCESS] Item ID {item_id} quantity updated to {new_quantity}.")
                else:
                    print("\n[ERROR] Quantity must be zero or a positive number.")
            except ValueError:
                print("\n[ERROR] Invalid input. Please enter a whole number for quantity.")
        else:
            print("\n[ERROR] Invalid choice.")
    else:
        print(f"\n[ERROR] Item with ID {item_id} not found.")


def delete_item():
    """Prompts the user for an item ID and removes it from the inventory."""
    view_inventory()
    if not INVENTORY:
        return

    try:
        item_id = int(input("Enter the ID of the item you want to delete: "))
    except ValueError:
        print("\n[ERROR] Invalid ID. Please enter a number.")
        return

    item_to_delete = get_item_by_id(item_id)

    if item_to_delete:
        INVENTORY.remove(item_to_delete)
        print(f"\n[SUCCESS] Item ID {item_id} ('{item_to_delete['name']}') deleted from inventory.")
    else:
        print(f"\n[ERROR] Item with ID {item_id} not found.")


def main():
    """The main application loop."""
    print("Welcome to the Console Inventory Manager!")

    while True:
        display_menu()
        choice = input("Enter your option (1-5): ").strip()

        if choice == '1':
            add_item()
        elif choice == '2':
            view_inventory()
        elif choice == '3':
            update_item()
        elif choice == '4':
            delete_item()
        elif choice == '5':
            print("\nThank you for using the Inventory Manager. Goodbye!")
            break
        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1 and 5.")


# --- Execution Block ---
if __name__ == "__main__":
    main()
