TASKS = []
next_id = 1

def display_menu():
    """Prints the main menu options to the console."""
    print("\n" + "="*40)
    print("      TASK MANAGER CONSOLE APP")
    print("="*40)
    print("1. Add New Task (Create)")
    print("2. View All Tasks (Read)")
    print("3. Update Task Description/Status (Update)")
    print("4. Delete Task (Delete)")
    print("5. Exit")
    print("="*40)

def view_tasks():
    """Displays all tasks with their index and status."""
    if not TASKS:
        print("\n[INFO] The task list is currently empty.")
        return

    print("\n--- Current Tasks ---")
    print("{:<5} {:<6} {}".format("ID", "Status", "Description"))
    print("-" * 35)

    for task in TASKS:
        status = "[DONE]" if task['done'] else "[TODO]"
        print(f"{task['id']:<5} {status:<6} {task['description']}")

    print("-" * 35)

def add_task():
    """Prompts the user for a task description and adds it to the list."""
    global next_id
    description = input("Enter the description for the new task: ").strip()
    if description:
        new_task = {
            'id': next_id,
            'description': description,
            'done': False
        }
        TASKS.append(new_task)
        print(f"\n[SUCCESS] Task '{description}' (ID: {next_id}) added.")
        next_id += 1
    else:
        print("\n[ERROR] Task description cannot be empty.")

def get_task_by_id(task_id):
    """Helper function to find a task by its unique ID."""
    for task in TASKS:
        if task['id'] == task_id:
            return task
    return None

def update_task():
    """Allows the user to modify a task's description or mark it as done/undone."""
    view_tasks()
    if not TASKS:
        return

    try:
        task_id = int(input("Enter the ID of the task you want to update: "))
    except ValueError:
        print("\n[ERROR] Invalid ID. Please enter a number.")
        return

    task_to_update = get_task_by_id(task_id)

    if task_to_update:
        print(f"\nEditing Task ID: {task_id} ('{task_to_update['description']}')")
        print("1. Change description")
        print("2. Toggle status (Done/To-Do)")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            new_description = input("Enter the new description: ").strip()
            if new_description:
                task_to_update['description'] = new_description
                print(f"\n[SUCCESS] Task ID {task_id} description updated.")
            else:
                print("\n[ERROR] Description cannot be empty. No change made.")
        elif choice == '2':
            task_to_update['done'] = not task_to_update['done']
            status = "DONE" if task_to_update['done'] else "TO-DO"
            print(f"\n[SUCCESS] Task ID {task_id} status changed to {status}.")
        else:
            print("\n[ERROR] Invalid choice.")
    else:
        print(f"\n[ERROR] Task with ID {task_id} not found.")


def delete_task():
    """Prompts the user for a task ID and removes it from the list."""
    view_tasks()
    if not TASKS:
        return

    try:
        task_id = int(input("Enter the ID of the task you want to delete: "))
    except ValueError:
        print("\n[ERROR] Invalid ID. Please enter a number.")
        return

    task_to_delete = get_task_by_id(task_id)

    if task_to_delete:
        TASKS.remove(task_to_delete)
        print(f"\n[SUCCESS] Task ID {task_id} ('{task_to_delete['description']}') deleted.")
    else:
        print(f"\n[ERROR] Task with ID {task_id} not found.")


def main():
    """The main application loop."""
    print("Welcome to the Console Task Manager!")

    while True:
        display_menu()
        choice = input("Enter your option (1-5): ").strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            update_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("\nThank you for using the Task Manager. Goodbye!")
            break
        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1 and 5.")


# --- Execution Block ---
if __name__ == "__main__":
    main()
