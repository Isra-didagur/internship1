def celsius_to_fahrenheit(celsius):
    """Converts temperature from Celsius ($\degree$C) to Fahrenheit ($\degree$F)."""
    # Formula: F = C * 9/5 + 32
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Converts temperature from Fahrenheit ($\degree$F) to Celsius ($\degree$C)."""
    # Formula: C = (F - 32) * 5/9
    return (fahrenheit - 32) * 5/9

def get_temperature_input(scale):
    """Handles temperature input and validation, ensuring the input is a number."""
    while True:
        try:
            # Step 1: Design a program to accept temperature input.
            temp_input = float(input(f"Enter temperature in {scale}: ").strip())
            return temp_input
        except ValueError:
            print("\n[ERROR] Invalid input. Please enter a numerical value for the temperature.")

def display_menu():
    """Prints the main conversion menu, allowing direction choice."""
    print("\n" + "="*40)
    print("  TEMPERATURE CONVERTER CONSOLE APP")
    print("="*40)
    # Step 3: Allow users to choose the conversion direction.
    print("1. Celsius (\u00b0C) to Fahrenheit (\u00b0F)")
    print("2. Fahrenheit (\u00b0F) to Celsius (\u00b0C)")
    print("3. Exit")
    print("="*40)

def main():
    """The main application loop for the temperature converter."""
    print("Welcome to the Temperature Converter!")

    while True:
        display_menu()
        choice = input("Enter your option (1-3): ").strip()

        if choice == '1':
            # C to F conversion (Step 2: Implement logic)
            celsius = get_temperature_input("Celsius")
            fahrenheit = celsius_to_fahrenheit(celsius)
            print("-" * 40)
            # Using \u00b0 for the degree symbol in console output
            print(f"Result: {celsius}\u00b0C is equal to {fahrenheit:.2f}\u00b0F")
            print("-" * 40)

        elif choice == '2':
            # F to C conversion (Step 2: Implement logic)
            fahrenheit = get_temperature_input("Fahrenheit")
            celsius = fahrenheit_to_celsius(fahrenheit)
            print("-" * 40)
            print(f"Result: {fahrenheit}\u00b0F is equal to {celsius:.2f}\u00b0C")
            print("-" * 40)

        elif choice == '3':
            # Exit
            print("\nThank you for using the Temperature Converter. Goodbye!")
            break

        else:
            # Invalid choice handling
            print("\n[ERROR] Invalid choice. Please enter 1, 2, or 3.")

# --- Execution Block ---
if __name__ == "__main__":
    main()
