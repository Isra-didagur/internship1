import time
import sys

# Constants for better readability
DEFAULT_SIZE = 5

def print_pattern_header(title, size):
    """Prints a formatted header before each pattern."""
    print("\n" + "="*50)
    print(f"Pattern: {title} (Size N={size})")
    print("="*50)
    # Pause slightly to distinguish output sections
    time.sleep(0.05)


def print_right_triangle(n):
    """
    Prints a right-aligned triangle where each row repeats the row number.
    Example (n=5):
    1
    2 2
    3 3 3
    4 4 4 4
    5 5 5 5 5
    """
    print_pattern_header("Right Triangle (Repeated Digits)", n)

    for i in range(1, n + 1):
        # Generate the string for the current row: 'i' repeated 'i' times, space-separated.
        line = (str(i) + " ") * i
        # Use rjust() to align the pattern to the right, based on the maximum width
        # The max width is reached by the last row (n * 2 spaces)
        max_width = n * 2
        print(line.strip().rjust(max_width))
    print("-" * 50)


def print_symmetrical_pyramid(n):
    """
    Prints a large symmetrical pyramid (diamond top) using increasing and
    decreasing sequences of numbers. This is often called Pascal's Triangle
    pattern or a simple Diamond pattern.
    Example (n=5):
        1
      1 2 1
    1 2 3 2 1
    ...
    """
    print_pattern_header("Symmetrical Pyramid (Increasing & Decreasing)", n)

    # 1. Top half (including the middle line)
    for i in range(1, n + 1):
        # Calculate leading spaces for centering. Each number takes 2 spaces.
        spaces = "  " * (n - i)
        line = spaces

        # Increasing sequence: 1 to i
        for j in range(1, i + 1):
            line += str(j) + " "

        # Decreasing sequence: i-1 down to 1
        for j in range(i - 1, 0, -1):
            line += str(j) + " "

        print(line.strip()) # strip() removes the trailing space at the end of the line

    print("-" * 50)


def print_inverted_pyramid(n):
    """
    Prints a large inverted pyramid shape.
    The number of digits decreases by 2 in each subsequent row.
    Example (n=5):
    1 1 1 1 1 1 1 1 1
      2 2 2 2 2 2 2
        3 3 3 3 3
          4 4 4
            5
    """
    print_pattern_header("Inverted Pyramid (Repeated Digits)", n)

    # We iterate from the first row (i=0) to the last (i=n-1)
    for i in range(n):
        num_to_print = i + 1
        # Number of digits in the row: 2*N - 1, decreasing by 2 each time
        num_count = 2 * (n - i) - 1
        
        # Leading spaces for centering. Each space is 2 characters wide.
        leading_spaces = "  " * i 
        
        # Generate the numbers string, space-separated
        numbers = (str(num_to_print) + " ") * num_count
        
        # Print the line, stripping the unwanted trailing space
        print(f"{leading_spaces}{numbers.strip()}")

    print("-" * 50)


# --- Execution Block ---
if __name__ == "__main__":
    # You can change the 'size' variable below to make the patterns bigger or smaller!
    size = DEFAULT_SIZE
    if len(sys.argv) > 1:
        try:
            size = int(sys.argv[1])
        except ValueError:
            print("Invalid input. Using default size 5.")

    print(f"Generating number patterns with size N={size}.")
    print_right_triangle(size)
    print_symmetrical_pyramid(size)
    print_inverted_pyramid(size)
    print("\nScript finished.")
