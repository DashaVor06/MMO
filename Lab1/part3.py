"""
Part 3 of Laboratory Work 1.
Contains tasks 3.1 through 3.4 (OOP).
"""


# ==================== Task 3.1 ====================
class Example:
    # Two static (class) variables
    static_var1 = 10
    static_var2 = 5

    def __init__(self):
        # Two dynamic (instance) variables
        self.dynamic_var1 = 2
        self.dynamic_var2 = 3

    # First method: create a variable and print it
    def method1(self):
        local_var = "Hello from method1"
        print(local_var)

    # Second method: return the sum of two global (class) variables
    def method2(self):
        return Example.static_var1 + Example.static_var2

    # Third method: return dynamic_var1 raised to the power of dynamic_var2
    def method3(self):
        return self.dynamic_var1 ** self.dynamic_var2


def task3_1():
    print("\n--- Task 3.1: Class with Static and Dynamic Variables ---")
    # Create an object of the class
    obj = Example()

    # Print both methods
    obj.method1()
    print("Sum of static vars (method2):", obj.method2())
    print("dynamic_var1 ** dynamic_var2 (method3):", obj.method3())

    # Print variable a (we use static_var1 as 'a')
    a = Example.static_var1
    print("a =", a)


# ==================== Task 3.2 ====================
class House:
    def __init__(self, area, price):
        # Dynamic properties
        self._area = area
        self._price = price

    def final_price(self, discount):
        # Return price with discount
        return self._price - (self._price * discount / 100)


class SmallHouse(House):
    def __init__(self, price):
        # Area is always 40 m2
        super().__init__(40, price)


class Human:
    def __init__(self, money):
        self._money = money
        self._house = None

    # Private method for the deal
    def _make_deal(self, house, price):
        self._money -= price
        self._house = house

    # Public method to buy a house
    def buy_house(self, house, discount):
        price = house.final_price(discount)
        if self._money >= price:
            self._make_deal(house, price)
            print("House bought! Remaining money:", self._money)
        else:
            print("Not enough money! Need:", price, "Have:", self._money)


def task3_2():
    print("\n--- Task 3.2: House, SmallHouse, Human ---")
    # Create a small house with price 100000
    small_house = SmallHouse(100000)
    print("Small house area:", small_house._area)
    print("Final price with 10% discount:", small_house.final_price(10))

    # Create a human with 90000
    print("\nHuman with $90,000 trying to buy:")
    human = Human(90000)
    human.buy_house(small_house, 10)  # Should succeed

    # Create a human with 50000
    print("\nHuman with $50,000 trying to buy:")
    poor_human = Human(50000)
    poor_human.buy_house(small_house, 10)  # Should fail


# ==================== Task 3.3 ====================
class Worker:
    def __init__(self, name, surname, position, wage, bonus):
        self.name = name
        self.surname = surname
        self.position = position
        # Protected attribute: dictionary with wage and bonus
        self._income = {"wage": wage, "bonus": bonus}


class Position(Worker):
    def get_full_name(self):
        # Return full name
        return self.name + " " + self.surname

    def get_total_income(self):
        # Return total income with bonus
        return self._income["wage"] + self._income["bonus"]


def task3_3():
    print("\n--- Task 3.3: Worker and Position ---")
    # Create instances of Position
    worker1 = Position("Ivan", "Ivanov", "Manager", 50000, 10000)
    worker2 = Position("Petr", "Petrov", "Engineer", 60000, 15000)

    # Check attributes
    print("Worker1 name:", worker1.name)
    print("Worker1 surname:", worker1.surname)
    print("Worker1 position:", worker1.position)
    print("Worker1 income dict:", worker1._income)

    # Call methods
    print("Worker1 full name:", worker1.get_full_name())
    print("Worker1 total income:", worker1.get_total_income())

    print("\nWorker2 full name:", worker2.get_full_name())
    print("Worker2 total income:", worker2.get_total_income())


# ==================== Task 3.4 ====================
class Book:
    # Class variable (static)
    total_books = 0

    def __init__(self, title, author, pages):
        # Instance variables
        self.title = title
        self.author = author
        self.pages = pages
        # Increase total books count
        Book.total_books += 1

    # Instance method: uses self
    def get_info(self):
        return f"'{self.title}' by {self.author}, {self.pages} pages"

    # Instance method: check if book is long
    def is_long(self):
        return self.pages > 300

    # Static method: doesn't use self or cls
    @staticmethod
    def is_valid_pages(pages):
        # Check if pages count is valid
        return pages > 0

    # Class method: uses cls
    @classmethod
    def get_total_books(cls):
        return f"Total books created: {cls.total_books}"

    # Class method: alternative constructor
    @classmethod
    def from_string(cls, book_str):
        # Create a book from a string like "Title,Author,Pages"
        title, author, pages = book_str.split(",")
        return cls(title, author, int(pages))


def task3_4():
    print("\n--- Task 3.4: Book Class (Methods and Constructors) ---")
    # Reset count if needed for clean demonstration
    Book.total_books = 0

    # Create books using normal constructor
    book1 = Book("War and Peace", "Leo Tolstoy", 1225)
    book2 = Book("The Little Prince", "Antoine de Saint-Exupery", 96)

    # Call instance methods
    print(book1.get_info())
    print("Is long?", book1.is_long())
    print(book2.get_info())
    print("Is long?", book2.is_long())

    # Call static method
    print("Are 100 pages valid?", Book.is_valid_pages(100))
    print("Are -5 pages valid?", Book.is_valid_pages(-5))

    # Call class method
    print(Book.get_total_books())

    # Create a book using class method (alternative constructor)
    book3 = Book.from_string("1984,George Orwell,328")
    print(book3.get_info())
    print(Book.get_total_books())


def run():
    tasks = {
        "1": ("Task 3.1: Example Class (Variables and Methods)", task3_1),
        "2": ("Task 3.2: House, SmallHouse, Human Inheritance", task3_2),
        "3": ("Task 3.3: Worker and Position (Inheritance & Income)", task3_3),
        "4": ("Task 3.4: Book Class (Static, Class, and Instance Methods)", task3_4),
    }

    while True:
        print("\n" + "=" * 40)
        print("           PART 3 MENU")
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
