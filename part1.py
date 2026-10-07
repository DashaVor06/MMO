"""
Part 1 of Laboratory Work 1.
Contains tasks 1.1 through 1.6.
"""


# ==================== Task 1.1 ====================
def task1_1():
    print("\n--- Task 1.1: Divisors of a Number ---")
    # Prompt the user to enter an integer from the keyboard
    num = int(input("Enter a number: "))

    print("Divisors of:", num)

    # Iterate through all numbers from 1 up to num (inclusive)
    for i in range(1, num + 1):
        # Check if num is divisible by i without a remainder
        if num % i == 0:
            print(i, end=" ")
    print()


# ==================== Task 1.2 ====================
def task1_2():
    print("\n--- Task 1.2: String Analysis (Even Words & Longest Word) ---")
    # Prompt the user to enter a string from the keyboard
    text = input("Enter a string: ")

    # Split the input text into a list of words by spaces
    words = text.split()

    # Initialize counters for even-length words and the longest word
    even_count = 0
    longest_word = ""

    # Iterate through each word in the list
    for word in words:
        # Remove punctuation marks from the edges of the word
        clean_word = word.strip(".,!?:;\"'()")
        word_len = len(clean_word)

        # a) Check if the length of the word is even
        if word_len % 2 == 0 and word_len > 0:
            even_count += 1

        # b) Check if the current word is longer than the previously saved longest word
        if word_len > len(longest_word):
            longest_word = clean_word

    # Print the results
    print(f"Amount of words with even number of letters: {even_count}")
    print(f"Longest word: {longest_word}")


# ==================== Task 1.3 ====================
def task1_3():
    print("\n--- Task 1.3: List Processing (Max Even & Rearrange) ---")
    # Prompt the user to enter numbers separated by spaces
    user_input = input("Enter list of numbers separated by spaces: ")

    # Convert the input string into a list of integers
    numbers = []
    for item in user_input.split():
        numbers.append(int(item))

    # Check if the list is empty
    if not numbers:
        print("List is empty")
        return

    # --- Part 1: Find the largest even number ---
    max_even = None
    for num in numbers:
        if num % 2 == 0:
            if max_even is None or num > max_even:
                max_even = num

    # Print the result (largest even or the first element if no even numbers exist)
    if max_even is not None:
        print(f"Max even number: {max_even}")
    else:
        print(f"There is no even numbers. First number: {numbers[0]}")

    # --- Part 2: Separate positive numbers from the rest ---
    positives = []
    others = []

    for num in numbers:
        if num > 0:
            positives.append(num)
        else:
            others.append(num)

    # Combine positive numbers and non-positives into a new list
    transformed_list = positives + others
    print(f"Transformed list: {transformed_list}")


# ==================== Task 1.4 ====================
def task1_4():
    print("\n--- Task 1.4: Dictionary Sorting ---")
    # Sample dictionary where keys are item names and values are numbers
    my_dict = {"A": 15, "B": 5, "C": 42, "D": 8}
    print("Original dictionary:", my_dict)

    # 1. Sort dictionary by values in ASCENDING order
    sorted_asc = dict(sorted(my_dict.items(), key=lambda item: item[1]))

    # 2. Sort dictionary by values in DESCENDING order
    sorted_desc = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))

    # Print the sorted dictionaries
    print("Ascending order: ", sorted_asc)
    print("Descending order:", sorted_desc)


# ==================== Task 1.5 ====================
def task1_5():
    print("\n--- Task 1.5: Store Application ---")
    # Initial store data: product_name: [price, quantity]
    store = {
        "Bear": [15.0, 10],
        "Doll": [20.0, 5],
        "Car": [8.5, 12],
        "Lego": [30.0, 3],
    }

    # Main application loop
    while True:
        # Display menu options
        print("\n=== STORE MENU ===")
        print("a. View prices")
        print("b. View quantities")
        print("c. View full information")
        print("d. Purchase")
        print("e. Exit")

        choice = input("Select an option (a-e): ").strip().lower()

        # Using match-case
        match choice:
            # Option A: View prices
            case "a":
                print("\n--- PRODUCT PRICES ---")
                for item, info in store.items():
                    print(f"{item} - ${info[0]}")

            # Option B: View quantities
            case "b":
                print("\n--- PRODUCT QUANTITIES ---")
                for item, info in store.items():
                    print(f"{item} - {info[1]} pcs")

            # Option C: View all information
            case "c":
                print("\n--- FULL STORE INFORMATION ---")
                for item, info in store.items():
                    print(f"{item}: Price = ${info[0]}, Quantity = {info[1]}")

            # Option D: Purchase
            case "d":
                total_cost = 0.0
                print("\n--- PURCHASE MODE (Enter 'n' to stop) ---")

                while True:
                    item_name = input("\nEnter product name (or 'n' to exit purchase mode): ").strip()

                    if item_name.lower() == "n":
                        break

                    # Check if item exists in store
                    if item_name not in store:
                        print("This product is not available in the store!")
                        continue

                    # Get quantity to buy
                    buy_qty = int(input(f"Enter quantity of '{item_name}': "))
                    available_qty = store[item_name][1]

                    # Check stock availability
                    if buy_qty <= 0:
                        print("Quantity must be greater than zero.")
                    elif buy_qty > available_qty:
                        print(f"Not enough stock! Only {available_qty} left.")
                    else:
                        cost = store[item_name][0] * buy_qty
                        total_cost += cost

                        # Update stock remaining
                        store[item_name][1] -= buy_qty
                        print(f"Added to cart: {buy_qty} x {item_name} = ${cost}")
                        print(f"Remaining in stock: {store[item_name][1]}")

                # Summary of the current purchase session
                print(f"\n>>> Total cost of purchase: ${total_cost}")

            # Option E: Exit program
            case "e":
                print("\nGoodbye!")
                break

            # Default case for handling invalid choices
            case _:
                print("Invalid option! Please select a, b, c, d, or e.")


# ==================== Task 1.6 ====================
def task1_6():
    print("\n--- Task 1.6: Sum of Positive Tuple Elements ---")
    # Example tuple of integers
    numbers = (-5, 10, 3, -2, 8, 0, -1, 4)
    print("Original tuple:", numbers)

    # Variable to store the sum of positive numbers
    positive_sum = 0

    # Iterate through each number in the tuple
    for num in numbers:
        # Check if the number is strictly positive (greater than zero)
        if num > 0:
            positive_sum += num

    # Print the calculated sum
    print(f"Sum of positive elements: {positive_sum}")


def run():
    tasks = {
        "1": ("Task 1.1: Divisors of a Number", task1_1),
        "2": ("Task 1.2: String Analysis", task1_2),
        "3": ("Task 1.3: List Processing", task1_3),
        "4": ("Task 1.4: Dictionary Sorting", task1_4),
        "5": ("Task 1.5: Store Application", task1_5),
        "6": ("Task 1.6: Sum of Positive Tuple Elements", task1_6),
    }

    while True:
        print("\n" + "=" * 40)
        print("           PART 1 MENU")
        print("=" * 40)
        for key, (desc, _) in tasks.items():
            print(f"{key}. {desc}")
        print("0. Back / Exit")

        choice = input("Select a task to run (0-6): ").strip()
        if choice == "0":
            break
        elif choice in tasks:
            tasks[choice][1]()
        else:
            print("Invalid selection! Please enter a number from 0 to 6.")


if __name__ == "__main__":
    run()
