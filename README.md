[README.md](https://github.com/user-attachments/files/35391830/README.md)
# Student Personal Expense and Budget Analyzer

A simple Python console application that helps students track their expenses against a monthly budget. It saves data permanently in a JSON file, shows a category-wise summary and can export a text report.

---

## Features

- Set a monthly budget on the first run
- Add expenses with a category and amount
- Instant alert if the budget is exceeded, otherwise shows the remaining budget
- View all expenses as a numbered list
- Summary with total budget, total spent, remaining amount and category breakdown
- Shows the highest spending category
- Delete an expense by its number
- Download a report as `budget_report.txt`
- Data is saved automatically in `expenses_data.json`, so nothing is lost when the program closes
- Input validation, so wrong input never crashes the program

---

## Requirements

- Python 3.6 or above
- No external libraries (uses only the built-in `json` and `os` modules)

---

## How to Run

```bash
python main_01.py
```

On the first run the program asks for your monthly budget. After that, a menu is shown:

```
Options:
(1) Add Expense
(2) View All Expenses
(3) View Summary
(4) Delete Expense
(5) Download Report
(6) Exit
Enter your choice (1-6):
```

---

## Project Files

| File | Purpose |
|---|---|
| `main_01.py` | Main source code |
| `expenses_data.json` | Created automatically. Stores budget and expenses |
| `budget_report.txt` | Created when option 5 is used. Human-readable report |

---

## Team and Roles

| Member | Role | Functions / Part |
|---|---|---|
| **Parv** | Data Storage (File Handling) | `save_data()`, `load_data()` |
| **Ishaan** | Input Validation | `get_positive_number()` and budget setup in the main program |
| **Kartike** | Add Expense + View All Expenses | `add_expense()`, `view_all_expenses()` |
| **Kavya** | Calculations + Summary | `get_total_spent()`, `get_category_totals()`, `view_summary()` |
| **Arun** | Delete + Report + Menu | `delete_expense()`, `download_report()`, main menu loop |

### Parv: Data Storage
- Saves the budget and expenses to `expenses_data.json` using `json.dump`
- Loads them back at program start using `json.load`
- Uses `os.path.exists` so the first run does not crash
- Uses `global budget` because the budget value is reassigned while loading

### Ishaan: Input Validation
- `get_positive_number()` keeps asking until the user enters a valid number greater than 0
- Uses `try/except ValueError` to handle text input
- The same function is reused for both budget and expense amount
- Asks for the monthly budget on the first run (`if budget == 0`)

### Kartike: Add Expense + View All
- `add_expense()` cleans the category with `.strip().title()`, validates the amount, adds it to the list, saves it and shows the budget status
- `view_all_expenses()` prints all expenses in a numbered list

### Kavya: Calculations + Summary
- `get_total_spent()` adds up all expense amounts (accumulator pattern)
- `get_category_totals()` builds a dictionary of category and its total
- `view_summary()` shows budget, spent, remaining, category breakdown and the highest spending category using `max(totals, key=totals.get)`

### Arun: Delete + Report + Menu
- `delete_expense()` removes an expense by number (`pop(number - 1)`) and updates the file
- `download_report()` writes the full report to `budget_report.txt`
- The main menu loop (`while True` with `if/elif`) controls the whole program until option 6 is chosen

---

## Program Flow

```
Start -> load_data() -> (first run) set budget -> Menu loop
                                                   |
        1 Add  2 View All  3 Summary  4 Delete  5 Report  6 Exit
```

---

## Sample Output

```
Enter your choice (1-6): 2
--- All Expenses ---
1. Food - Rs. 500.00
2. Books - Rs. 300.00
3. Food - Rs. 200.00
```

---

## Concepts Used

- Functions and modularity
- Lists and dictionaries (list of dictionaries)
- File handling and JSON
- Exception handling (`try/except`)
- Loops and conditions
- f-string formatting
- Global variables

---

## Team

Parv | Ishaan | Kartike | Kavya | Arun
