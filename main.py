import json
import os
from datetime import date

FILE_NAME = "expenses_data.json"

expenses = []
budget = 0.0


def save_data():
    data = {"budget": budget, "expenses": expenses}
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


def load_data():
    global budget
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
            budget = data["budget"]
            expenses.extend(data["expenses"])
            return True
        except (json.JSONDecodeError, KeyError):
            print("Saved file is damaged. Starting fresh.")
    return False


def get_positive_number(message):
    while True:
        try:
            value = float(input(message))
            if value <= 0:
                print("Value must be greater than 0. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid input! Please enter a number.")


def get_total_spent():
    total = 0.0
    for item in expenses:
        total += item["amount"]
    return total


def get_category_totals():
    totals = {}
    for item in expenses:
        cat = item["category"]
        if cat in totals:
            totals[cat] += item["amount"]
        else:
            totals[cat] = item["amount"]
    return totals


def check_budget_status():
    spent = get_total_spent()
    if spent > budget:
        print(f"ALERT: Budget exceeded by Rs. {spent - budget:.2f}!")
    elif spent >= 0.8 * budget:
        print("WARNING: You have used 80% or more of your budget.")
    else:
        print(f"Remaining Budget: Rs. {budget - spent:.2f}")


def add_expense():
    category = input("Enter category (e.g. Food, Books): ").strip().title()
    if category == "":
        print("Category cannot be empty.")
        return
    amount = get_positive_number(f"Enter amount spent on {category} (Rs.): ")

    expenses.append({
        "date": str(date.today()),
        "category": category,
        "amount": amount
    })
    save_data()
    print(f"\nSuccess: Added Rs. {amount:.2f} for '{category}'.")
    check_budget_status()


def view_all_expenses():
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\n--- All Expenses ---")
    print(f"{'No.':<5}{'Date':<14}{'Category':<15}{'Amount (Rs.)':>12}")
    for i, item in enumerate(expenses, start=1):
        print(f"{i:<5}{item['date']:<14}{item['category']:<15}{item['amount']:>12.2f}")


def view_summary():
    spent = get_total_spent()
    percent_used = (spent / budget) * 100

    print("\n--- Expense Summary ---")
    print(f"Total Budget : Rs. {budget:.2f}")
    print(f"Total Spent  : Rs. {spent:.2f}")
    print(f"Remaining    : Rs. {budget - spent:.2f}")
    print(f"Budget Used  : {percent_used:.1f}%")
    check_budget_status()

    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    count = len(expenses)
    average = spent / count
    biggest = max(expenses, key=lambda item: item["amount"])
    print("\n--- Statistics ---")
    print(f"Number of expenses : {count}")
    print(f"Average expense    : Rs. {average:.2f}")
    print(f"Biggest expense    : Rs. {biggest['amount']:.2f} ({biggest['category']})")

    print("\n--- Category Breakdown ---")
    totals = get_category_totals()
    for cat, amt in totals.items():
        share = (amt / spent) * 100
        bar = "#" * int(share / 5)
        print(f"{cat:<12} Rs. {amt:>8.2f}  {share:5.1f}%  {bar}")

    highest = max(totals, key=totals.get)
    print(f"\nHighest Spending Category: {highest} (Rs. {totals[highest]:.2f})")


def delete_expense():
    if not expenses:
        print("\nNothing to delete.")
        return
    view_all_expenses()
    try:
        number = int(input("\nEnter the number of the expense to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if 1 <= number <= len(expenses):
        removed = expenses.pop(number - 1)
        save_data()
        print(f"Deleted: {removed['category']} - Rs. {removed['amount']:.2f}")
    else:
        print("No expense with that number.")


def search_by_category():
    name = input("Enter category to search: ").strip().title()
    found = False
    subtotal = 0.0
    print(f"\n--- Expenses in '{name}' ---")
    for item in expenses:
        if item["category"] == name:
            print(f"{item['date']}  Rs. {item['amount']:.2f}")
            subtotal += item["amount"]
            found = True
    if found:
        print(f"Total for {name}: Rs. {subtotal:.2f}")
    else:
        print("No expenses found in this category.")


def change_budget():
    global budget
    print(f"\nCurrent budget: Rs. {budget:.2f}")
    budget = get_positive_number("Enter new monthly budget (Rs.): ")
    save_data()
    print("Budget updated.")
    check_budget_status()


def reset_all():
    confirm = input("This will delete ALL data. Type YES to confirm: ")
    if confirm == "YES":
        expenses.clear()
        save_data()
        print("All expenses cleared.")
    else:
        print("Reset cancelled.")


print("--- Student Personal Expense and Budget Analyzer ---")

if load_data():
    print(f"Welcome back! Loaded {len(expenses)} saved expense(s).")
else:
    budget = get_positive_number("Enter your monthly budget (Rs.): ")
    save_data()

while True:
    print("\nOptions:")
    print("(1) Add Expense")
    print("(2) View All Expenses")
    print("(3) View Summary")
    print("(4) Delete Expense")
    print("(5) Search by Category")
    print("(6) Change Budget")
    print("(7) Reset All Expenses")
    print("(8) Exit")
    choice = input("Enter your choice (1-8): ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_all_expenses()
    elif choice == "3":
        view_summary()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        search_by_category()
    elif choice == "6":
        change_budget()
    elif choice == "7":
        reset_all()
    elif choice == "8":
        print(f"\nExiting. Final Total Spent: Rs. {get_total_spent():.2f}")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 8.")
