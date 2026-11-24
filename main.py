import json
import os

FILE_NAME = "expenses_data.json"

expenses = []
budget = 0.0


def save_data():
    data = {"budget": budget, "expenses": expenses}
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)


def load_data():
    global budget
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
            budget = data["budget"]
            expenses.extend(data["expenses"])
        except (ValueError, KeyError):
            print("Saved file is damaged. Starting fresh.")


def get_positive_number(message):
    while True:
        try:
            value = float(input(message))
            if value <= 0:
                print("Value must be greater than 0.")
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


def add_expense():
    category = input("Enter category (e.g. Food, Books): ").strip().title()
    if category == "":
        print("Category cannot be empty.")
        return
    amount = get_positive_number("Enter amount (Rs.): ")

    expenses.append({"category": category, "amount": amount})
    save_data()
    print(f"Added Rs. {amount:.2f} for {category}.")

    total = get_total_spent()
    if total > budget:
        print(f"ALERT: Budget exceeded by Rs. {total - budget:.2f}!")
    else:
        print(f"Remaining budget: Rs. {budget - total:.2f}")


def view_all_expenses():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    print("--- All Expenses ---")
    for i in range(len(expenses)):
        print(f"{i + 1}. {expenses[i]['category']} - Rs. {expenses[i]['amount']:.2f}")


def view_summary():
    total = get_total_spent()
    print("--- Summary ---")
    print(f"Total Budget: Rs. {budget:.2f}")
    print(f"Total Spent : Rs. {total:.2f}")
    print(f"Remaining   : Rs. {budget - total:.2f}")
    if total > budget:
        print("ALERT: Budget exceeded!")

    if len(expenses) == 0:
        print("No expenses yet.")
        return

    print("--- Category Breakdown ---")
    totals = get_category_totals()
    for cat in totals:
        print(f"{cat}: Rs. {totals[cat]:.2f}")

    highest = max(totals, key=totals.get)
    print(f"Highest Spending Category: {highest} (Rs. {totals[highest]:.2f})")


def delete_expense():
    if len(expenses) == 0:
        print("Nothing to delete.")
        return
    view_all_expenses()
    try:
        number = int(input("Enter expense number to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if 1 <= number <= len(expenses):
        expenses.pop(number - 1)
        save_data()
        print("Expense deleted.")
    else:
        print("No expense with that number.")


def download_report():
    total = get_total_spent()
    with open("budget_report.txt", "w") as f:
        f.write("EXPENSE AND BUDGET REPORT\n\n")
        f.write(f"Total Budget: Rs. {budget:.2f}\n")
        f.write(f"Total Spent : Rs. {total:.2f}\n")
        f.write(f"Remaining   : Rs. {budget - total:.2f}\n")
        if total > budget:
            f.write("ALERT: Budget exceeded!\n")
        f.write("\nCategory Breakdown:\n")
        totals = get_category_totals()
        for cat in totals:
            f.write(f"{cat}: Rs. {totals[cat]:.2f}\n")
        f.write("\nAll Expenses:\n")
        for item in expenses:
            f.write(f"{item['category']} - Rs. {item['amount']:.2f}\n")
    print("Report saved as budget_report.txt")


print("--- Student Personal Expense and Budget Analyzer ---")

load_data()
if budget == 0:
    budget = get_positive_number("Enter your monthly budget (Rs.): ")
    save_data()

while True:
    print("\nOptions:")
    print("(1) Add Expense")
    print("(2) View All Expenses")
    print("(3) View Summary")
    print("(4) Delete Expense")
    print("(5) Download Report")
    print("(6) Exit")
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_all_expenses()
    elif choice == "3":
        view_summary()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        download_report()
    elif choice == "6":
        print(f"Exiting. Final Total Spent: Rs. {get_total_spent():.2f}")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 6.")
