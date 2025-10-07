import os
###bookcatelog program with persistent storage using text files

FILE_NAME = "book_catalog.txt" # Changed to text file format
CATALOG = []
next_id = 1
DELIMITER = "|" # Define a simple delimiter for text file storage

def load_catalog():
    """
    Loads the book catalog from the text file on startup.
    Each line in the file is expected to be: id|title|author|read_status
    This implements file storage and error handling (Step 1 & 2).
    """
    global CATALOG
    global next_id
    if os.path.exists(FILE_NAME):
        try:
            CATALOG = []
            max_id = 0
            with open(FILE_NAME, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue # Skip empty lines

                    parts = line.split(DELIMITER)
                    if len(parts) == 4:
                        # Expecting: [ID, Title, Author, Read Status]
                        try:
                            book_id = int(parts[0])
                            # Convert file string ('True'/'False') to Python boolean
                            is_read = parts[3].lower() == 'true'
                            book = {
                                'id': book_id,
                                'title': parts[1],
                                'author': parts[2],
                                'read': is_read
                            }
                            CATALOG.append(book)
                            max_id = max(max_id, book_id)
                        except ValueError:
                            # Skip lines where ID is not a valid integer
                            print(f"[WARNING] Skipping invalid ID format in file: {line}")
                            continue
                    else:
                        # Handle lines that don't match the expected format
                        print(f"[WARNING] Skipping invalid line format in file: {line}")
                        continue

                # Set next_id correctly after loading all valid books
                if CATALOG:
                    next_id = max_id + 1
                print(f"[INFO] Loaded {len(CATALOG)} books from {FILE_NAME}.")

            # If file exists but is empty/corrupted, CATALOG will be empty and next_id will be 1
            if not CATALOG:
                next_id = 1

        except Exception as e:
            # Step 2: Implement error handling for file operations
            print(f"[ERROR] Failed to read catalog file: {e}. Starting with empty catalog.")
            CATALOG = []
    else:
        print(f"[INFO] {FILE_NAME} not found. Starting with a new empty catalog.")

def save_catalog():
    """
    Persistently saves the current book catalog to the text file.
    Each book is written as a single line, delimited by the pipe character.
    This implements file storage (Step 1).
    """
    try:
        with open(FILE_NAME, 'w') as f:
            for book in CATALOG:
                # Join the book's properties into a single delimited string
                line = DELIMITER.join([
                    str(book['id']),
                    book['title'],
                    book['author'],
                    str(book['read']) # Boolean value converted to string ('True' or 'False')
                ])
                f.write(line + '\n')
            print(f"[INFO] Catalog successfully saved to {FILE_NAME}.")
        
    except Exception as e:
        # Step 2: Implement error handling for file operations
        print(f"[ERROR] Failed to write catalog file: {e}")

def get_book_by_id(book_id):
    """Helper function to find a book by its unique ID."""
    for book in CATALOG:
        if book['id'] == book_id:
            return book
    return None

def display_menu():
    """Prints the main menu options to the console."""
    print("\n" + "="*40)
    print("      PERSISTENT BOOK CATALOG MANAGER")
    print("="*40)
    print("1. Add New Book (Create)")
    print("2. View All Books (Read)")
    print("3. Update Book Details (Update)")
    print("4. Delete Book (Delete)")
    print("5. Exit and Save")
    print("="*40)

# --- CRUD Operations ---

def add_book():
    """Prompts the user for book details and adds it to the list."""
    global next_id
    title = input("Enter the TITLE of the book: ").strip()
    author = input("Enter the AUTHOR of the book: ").strip()

    if not title or not author:
        print("\n[ERROR] Title and Author cannot be empty.")
        return

    new_book = {
        'id': next_id,
        'title': title,
        'author': author,
        'read': False # Default status
    }
    CATALOG.append(new_book)
    print(f"\n[SUCCESS] Book '{title}' by {author} (ID: {next_id}) added.")
    next_id += 1

def view_catalog():
    """Displays all books in the catalog with their status."""
    if not CATALOG:
        print("\n[INFO] The book catalog is currently empty.")
        return

    print("\n--- Current Book Catalog ---")
    print("{:<5} {:<10} {:<30} {}".format("ID", "Status", "Title", "Author"))
    print("-" * 75)

    for book in CATALOG:
        status = "[READ]" if book['read'] else "[UNREAD]"
        # Limit title length for clean console display
        display_title = book['title'][:27] + '...' if len(book['title']) > 30 else book['title']
        print(f"{book['id']:<5} {status:<10} {display_title:<30} {book['author']}")

    print("-" * 75)

def update_book():
    """Allows the user to modify a book's title, author, or status."""
    view_catalog()
    if not CATALOG:
        return

    try:
        book_id = int(input("Enter the ID of the book you want to update: "))
    except ValueError:
        print("\n[ERROR] Invalid ID. Please enter a number.")
        return

    book = get_book_by_id(book_id)

    if book:
        print(f"\nEditing Book ID: {book_id} ('{book['title']}')")
        print("1. Change Title")
        print("2. Change Author")
        print("3. Toggle Read/Unread Status")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            new_title = input("Enter the new title: ").strip()
            if new_title:
                book['title'] = new_title
                print(f"\n[SUCCESS] Book ID {book_id} title updated.")
            else:
                print("\n[ERROR] Title cannot be empty. No change made.")
        elif choice == '2':
            new_author = input("Enter the new author: ").strip()
            if new_author:
                book['author'] = new_author
                print(f"\n[SUCCESS] Book ID {book_id} author updated.")
            else:
                print("\n[ERROR] Author cannot be empty. No change made.")
        elif choice == '3':
            book['read'] = not book['read']
            status = "READ" if book['read'] else "UNREAD"
            print(f"\n[SUCCESS] Book ID {book_id} status changed to {status}.")
        else:
            print("\n[ERROR] Invalid choice.")
    else:
        print(f"\n[ERROR] Book with ID {book_id} not found.")


def delete_book():
    """Prompts the user for a book ID and removes it from the catalog."""
    view_catalog()
    if not CATALOG:
        return

    try:
        book_id = int(input("Enter the ID of the book you want to delete: "))
    except ValueError:
        print("\n[ERROR] Invalid ID. Please enter a number.")
        return

    book_to_delete = get_book_by_id(book_id)

    if book_to_delete:
        CATALOG.remove(book_to_delete)
        print(f"\n[SUCCESS] Book ID {book_id} ('{book_to_delete['title']}') deleted.")
    else:
        print(f"\n[ERROR] Book with ID {book_id} not found.")


def main():
    """The main application loop."""
    print("Welcome to the Persistent Book Catalog Manager!")
    load_catalog() # Load data from file on startup

    while True:
        display_menu()
        choice = input("Enter your option (1-5): ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            view_catalog()
        elif choice == '3':
            update_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            save_catalog() # Save data to file before exiting
            print("\nExiting. All changes have been saved. Goodbye!")
            break
        else:
            print("\n[ERROR] Invalid choice. Please enter a number between 1 and 5.")


# --- Execution Block ---
if __name__ == "__main__":
    main()
