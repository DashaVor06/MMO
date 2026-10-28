"""
Main launcher script for Laboratory Work 1.
Provides an interactive menu to choose between Part 1, Part 2, and Part 3.
"""

import part1
import part2
import part3


def main():
    parts = {
        "1": ("Part 1: Basic Python (Tasks 1.1 - 1.6)", part1.run),
        "2": ("Part 2: Functions, Patterns & Exceptions (Tasks 2.1 - 2.4)", part2.run),
        "3": ("Part 3: Object-Oriented Programming (Tasks 3.1 - 3.4)", part3.run),
    }

    while True:
        print("\n" + "=" * 50)
        print("     LABORATORY WORK 1 - MAIN RUNNER")
        print("=" * 50)
        for key, (desc, _) in parts.items():
            print(f"{key}. {desc}")
        print("0. Exit")

        choice = input("Select a part to run (0-3): ").strip()
        if choice == "0":
            print("Exiting program. Goodbye!")
            break
        elif choice in parts:
            parts[choice][1]()
        else:
            print("Invalid choice! Please select 0, 1, 2, or 3.")


if __name__ == "__main__":
    main()
