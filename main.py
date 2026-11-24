import json
import os
from datetime import date, datetime

FILE_NAME = "expenses_data.json"
REPORT_NAME = "budget_report.txt"

expenses = []
category_limits = {}
budget = 0.0


def save_data():
    data = {
        "budget": budget,
        "expenses": expenses,
        "category_limits": category_limits
    }
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
            category_limits.update(data.get("category_limits", {}))
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


def get_category_spent(category):
    total = 0.0
    for item in expenses:
        if item["category"] == category:
            total += item["amount"]
    return total


def get_total_limits():
    total = 0.0
    for limit in category_limits.values():
        total += limit
    return total


def limit_label(spent, limit):
    if spent > limit:
        return "EXCEEDED"
    elif spent >= 0.8 * limit:
        return "NEAR LIMIT"
    else:
        return "OK"


def budget_status_text():
    spent = get_total_spent()
    if spent > budget:
        return f"ALERT: Budget exceeded by Rs. {spent - budget:.2f}!"
    elif spent >= 0.8 * budget:
        return "WARNING: You have used 80% or more of your budget."
    else:
        return f"Remaining Budget: Rs. {budget - spent:.2f}"


def check_category_status(category):
    if category not in category_limits:
        return
    limit = category_limits[category]
    spent = get_category_spent(category)
    label = limit_label(spent, limit)
    if label == "EXCEEDED":
        print(f"CATEGORY ALERT: '{category}' limit exceeded by Rs. {spent - limit:.2f}!")
    elif label == "NEAR LIMIT":
        print(f"CATEGORY WARNING: You have used 80% or more of the '{category}' limit.")
    else:
        print(f"'{category}' limit remaining: Rs. {limit - spent:.2f}")


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
    print(budget_status_text())
    check_category_status(category)


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
    print(budget_status_text())

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
        line = f"{cat:<12} Rs. {amt:>8.2f}  {share:5.1f}%  {bar}"
        if cat in category_limits:
            line += f"  [Limit Rs. {category_limits[cat]:.2f}: {limit_label(amt, category_limits[cat])}]"
        print(line)

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
    print(f"\nCurrent overall budget: Rs. {budget:.2f}")
    budget = get_positive_number("Enter new overall monthly budget (Rs.): ")
    save_data()
    print("Overall budget updated.")
    print(budget_status_text())


def set_category_limit():
    category = input("Enter category name: ").strip().title()
    if category == "":
        print("Category cannot be empty.")
        return
    limit = get_positive_number(f"Enter monthly limit for {category} (Rs.): ")
    category_limits[category] = limit
    save_data()
    print(f"Limit for '{category}' set to Rs. {limit:.2f}.")
    if get_total_limits() > budget:
        print("Note: Total of all category limits is more than your overall budget.")
    check_category_status(category)


def view_category_limits():
    if not category_limits:
        print("\nNo category limits set yet.")
        return
    print("\n--- Category Limits ---")
    print(f"{'Category':<15}{'Limit':>10}{'Spent':>10}{'Left':>10}  Status")
    for cat, limit in category_limits.items():
        spent = get_category_spent(cat)
        print(f"{cat:<15}{limit:>10.2f}{spent:>10.2f}{limit - spent:>10.2f}  {limit_label(spent, limit)}")


def download_report():
    spent = get_total_spent()
    lines = []
    lines.append("STUDENT EXPENSE AND BUDGET REPORT")
    lines.append("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append("")
    lines.append("OVERALL SUMMARY")
    lines.append(f"Total Budget : Rs. {budget:.2f}")
    lines.append(f"Total Spent  : Rs. {spent:.2f}")
    lines.append(f"Remaining    : Rs. {budget - spent:.2f}")
    lines.append(f"Budget Used  : {(spent / budget) * 100:.1f}%")
    lines.append(budget_status_text())
    lines.append("")

    lines.append("CATEGORY BREAKDOWN")
    totals = get_category_totals()
    if totals:
        for cat, amt in totals.items():
            lines.append(f"{cat:<15} Rs. {amt:>9.2f}  {(amt / spent) * 100:5.1f}%")
        highest = max(totals, key=totals.get)
        lines.append(f"Highest Spending Category: {highest} (Rs. {totals[highest]:.2f})")
    else:
        lines.append("No expenses recorded.")
    lines.append("")

    lines.append("CATEGORY LIMITS")
    if category_limits:
        for cat, limit in category_limits.items():
            cat_spent = get_category_spent(cat)
            lines.append(f"{cat:<15} Limit Rs. {limit:>9.2f}  Spent Rs. {cat_spent:>9.2f}  {limit_label(cat_spent, limit)}")
    else:
        lines.append("No category limits set.")
    lines.append("")

    lines.append("ALL EXPENSES")
    if expenses:
        for i, item in enumerate(expenses, start=1):
            lines.append(f"{i:<4}{item['date']:<13}{item['category']:<15}Rs. {item['amount']:.2f}")
    else:
        lines.append("No expenses recorded.")

    with open(REPORT_NAME, "w") as f:
        f.write("\n".join(lines))
    print(f"\nReport downloaded as '{REPORT_NAME}'")
    print(f"Location: {os.path.abspath(REPORT_NAME)}")


def reset_all():
    confirm = input("This will delete ALL expenses. Type YES to confirm: ")
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
    budget = get_positive_number("Enter your overall monthly budget (Rs.): ")
    save_data()

while True:
    print("\nOptions:")
    print("(1)  Add Expense")
    print("(2)  View All Expenses")
    print("(3)  View Summary")
    print("(4)  Delete Expense")
    print("(5)  Search by Category")
    print("(6)  Change Overall Budget")
    print("(7)  Set Category Limit")
    print("(8)  View Category Limits")
    print("(9)  Download Report")
    print("(10) Reset All Expenses")
    print("(11) Exit")
    choice = input("Enter your choice (1-11): ")

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
        set_category_limit()
    elif choice == "8":
        view_category_limits()
    elif choice == "9":
        download_report()
    elif choice == "10":
        reset_all()
    elif choice == "11":
        print(f"\nExiting. Final Total Spent: Rs. {get_total_spent():.2f}")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 11.")
