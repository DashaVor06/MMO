"""
Part 2 of Laboratory Work 1.
Contains tasks 2.1 through 2.4.
"""


# ==================== Task 2.1 ====================
def count_vowels_and_consonants(text):
    # Sets of vowels and consonants for English alphabet (case-insensitive)
    vowels = "aeiouAEIOU"
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"

    # Initialize counters
    vowel_count = 0
    consonant_count = 0

    # Iterate over each character in the input string
    for char in text:
        if char in vowels:
            vowel_count += 1
        elif char in consonants:
            consonant_count += 1

    return vowel_count, consonant_count


def task2_1():
    print("\n--- Task 2.1: Count Vowels and Consonants ---")
    user_input = input("Enter a string: ")

    # Call the function and unpack returned values
    vowels_num, consonants_num = count_vowels_and_consonants(user_input)

    # Output the results
    print(f"Number of vowels: {vowels_num}")
    print(f"Number of consonants: {consonants_num}")


# ==================== Task 2.2 ====================
def process_data(data):
    # Match the type and pattern of the incoming data
    match data:
        # Case 1: Input argument is a DICTIONARY
        case dict():
            print("\n[Input type: Dictionary]")
            # Find 3 keys with the largest values
            top_3_keys = sorted(data.items(), key=lambda item: item[1], reverse=True)[:3]
            print(f"Original dictionary: {data}")
            print(f"Top 3 keys with largest values: {top_3_keys}")

        # Case 2: Input argument is a LIST
        case list():
            print("\n[Input type: List]")

            # Count even numbers
            even_count = 0
            for item in data:
                if isinstance(item, int) and item % 2 == 0:
                    even_count += 1

            # Remove duplicate elements
            unique_list = list(set(data))

            print(f"Original list: {data}")
            print(f"Number of even numbers: {even_count}")
            print(f"List without duplicates: {unique_list}")

        # Case 3: Input argument is a NUMBER (int or float)
        case int() | float() if not isinstance(data, bool):
            print("\n[Input type: Number]")
            # Convert number to string, strip non-digits, and calculate sum
            num_str = str(data).replace("-", "").replace(".", "")
            digit_sum = sum(int(char) for char in num_str)

            print(f"Original number: {data}")
            print(f"Sum of digits: {digit_sum}")

        # Case 4: Input argument is a STRING
        case str():
            print("\n[Input type: String]")
            # Clean punctuation symbols
            cleaned_text = data
            for punctuation in ".,!?:;\"'()":
                cleaned_text = cleaned_text.replace(punctuation, "")

            # Split text into words and count them
            words = cleaned_text.split()
            word_count = len(words)

            print(f"Original string: '{data}'")
            print(f"Cleaned string: '{cleaned_text}'")
            print(f"Number of words: {word_count}")

        # Default case for unsupported data types
        case _:
            print("\n[Unsupported Type]")
            print(f"Cannot process data of type: {type(data)}")


def task2_2():
    print("\n--- Task 2.2: Pattern Matching by Type (process_data) ---")
    print("Testing all cases with match-case:")

    # Test 1: Dictionary
    test_dict = {"A": 10, "B": 85, "C": 42, "D": 99, "E": 5}
    process_data(test_dict)

    # Test 2: List
    test_list = [4, 2, 7, 4, 8, 2, 10, 7, 1]
    process_data(test_list)

    # Test 3: Number
    test_number = 5824
    process_data(test_number)

    # Test 4: String
    test_string = "Hello, world! Welcome to Python programming..."
    process_data(test_string)


# ==================== Task 2.3 ====================
def count_non_zero_columns(matrix):
    # Check for empty matrix edge cases
    if not matrix or not matrix[0]:
        return 0

    rows_count = len(matrix)
    cols_count = len(matrix[0])
    non_zero_cols = 0

    # Iterate over each column index
    for col_idx in range(cols_count):
        has_zero = False

        # Check all rows for the current column
        for row_idx in range(rows_count):
            if matrix[row_idx][col_idx] == 0:
                has_zero = True
                break  # Stop checking this column as soon as a zero is found

        # If no zero was found in the column, increment the counter
        if not has_zero:
            non_zero_cols += 1

    return non_zero_cols


def task2_3():
    print("\n--- Task 2.3: Non-zero Columns in Matrix ---")
    # Sample rectangular matrix (3 rows x 4 columns)
    matrix = [
        [1, 2, 0, 4],
        [5, 0, 6, 8],
        [9, 10, 11, 12],
    ]

    print("Matrix:")
    for row in matrix:
        print(row)

    result = count_non_zero_columns(matrix)
    print(f"\nNumber of columns without zero elements: {result}")


# ==================== Task 2.4 ====================
def safe_divide(a, b):
    print(f"\n--- Trying to divide {a} by {b} ---")
    try:
        # Code that might raise an exception
        result = a / b
    except ZeroDivisionError:
        # Handles division by zero error
        print("Error: Cannot divide by zero!")
    except TypeError:
        # Handles invalid data types (e.g., dividing string by number)
        print("Error: Invalid data type for division!")
    else:
        # Executes ONLY if NO exception was raised in try block
        print(f"Success! Result: {result}")
    finally:
        # ALWAYS executes regardless of whether an exception occurred or not
        print("Cleanup: This block always runs (finally).")


def task2_4():
    print("\n--- Task 2.4: Exception Handling (try / except / else / finally) ---")
    # Case 1: Successful operation
    safe_divide(10, 2)

    # Case 2: Division by zero
    safe_divide(10, 0)

    # Case 3: Invalid type
    safe_divide(10, "two")


def run():
    tasks = {
        "1": ("Task 2.1: Count Vowels and Consonants", task2_1),
        "2": ("Task 2.2: Process Data with Pattern Matching", task2_2),
        "3": ("Task 2.3: Non-Zero Columns in Matrix", task2_3),
        "4": ("Task 2.4: Safe Division (Exception Handling)", task2_4),
    }

    while True:
        print("\n" + "=" * 40)
        print("           PART 2 MENU")
        print("=" * 40)
        for key, (desc, _) in tasks.items():
            print(f"{key}. {desc}")
        print("0. Back / Exit")

        choice = input("Select a task to run (0-4): ").strip()
        if choice == "0":
            break
        elif choice in tasks:
            tasks[choice][1]()
        else:
            print("Invalid selection! Please enter a number from 0 to 4.")


if __name__ == "__main__":
    run()
