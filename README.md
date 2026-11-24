[README.md](https://github.com/user-attachments/files/35328432/README.md)
# Student Personal Expense and Budget Analyzer

**Course Code:** 2026CSAE100 (Python Collaborative Project)
**Academic Year:** 2026-27
**Batch:** 70, Bennett University

## Team Details

| Role | Student Name | Enrollment No. |
|------|--------------|----------------|
| Analytics and Computation Lead | Arun | S26CSEU2492 |
| Budgeting and Logic Engineer | Kartike Yadav | S26CSEU2494 |
| UI and Input Validation Lead | Ishaan Bhardwaj | S26CSEU2493 |
| Data Structures Architect | Parv Girdhar | S26CSEU2497 |
| Testing and Documentation Lead | Kavya Chattha | S26CSEU2500 |

## Problem Statement

University students often struggle to manage their monthly allowances effectively and frequently lose track of where their money goes. They lack a simple, centralized tool to record daily spending, classify expenses into categories, and receive warnings before they overspend.

Solving this problem is useful because it promotes financial literacy, prevents end-of-month cash shortages, and helps students prioritize academic and essential living expenses over discretionary spending.

## Project Objectives

1. Accurately record student expenses.
2. Classify expenses into specific categories (for example Food, Transport, Academics).
3. Calculate total monthly expenditure and compare it against a predefined budget.
4. Generate rule-based alerts or warnings when a user nears the budget limit.
5. Analyze spending habits and programmatically identify the highest spending category.

## Main Features / Modules

| No. | Module | Description |
|-----|--------|-------------|
| 1 | Data Entry Module | Prompts the user to enter new expenses with amount and category. |
| 2 | Budget and Alert Module | Compares current expenditure with the budget and triggers alerts at the 80% and 100% thresholds. |
| 3 | Analytics Module | Calculates total expenditure and aggregates totals by category to find spending trends. |
| 4 | UI and Validation Module | Provides a continuous interactive menu and uses error handling to prevent crashes from invalid input. |
| 5 | File Handling Module | Saves data in a JSON file so records are kept between program sessions. |

## Additional Features

- Automatic date for every expense
- View all expenses in a numbered table
- Statistics: number of expenses, average expense, biggest expense
- Category breakdown with percentage and a simple text bar
- Delete an expense
- Search expenses by category
- Change the monthly budget
- Reset all expenses

## Algorithm

1. Start.
2. Load saved data if a data file exists. Otherwise ask for a valid, positive monthly budget (non-numeric input is caught).
3. Display the main menu.
4. Add Expense: take category and a positive amount, store the record, save it, and run the budget rule check.
5. Rule check: if total spent is greater than the budget, show an exceeded-budget alert. Else if total spent is 80% or more of the budget, show a warning. Otherwise show the remaining budget.
6. View Summary: loop through the expenses, aggregate amounts by category into a dictionary, print the totals, and find the highest spending category using `max()`.
7. Other options: view all, delete, search, change budget, reset.
8. Exit: print the final total spent and stop.

## Computational Feature

The main computational feature is analysis and summarization combined with rule-based alerts.

When the user selects "View Summary", the program loops through all recorded expenses and builds a dictionary that holds the total amount spent in each category. It then calculates the remaining budget and uses Python's `max()` function on the dictionary to find the highest spending category. Every time an expense is added, the program also checks the ratio of total spent to the budget and triggers an alert if the 80% or 100% threshold is crossed.

## Python Concepts Used

| Concept | Where / How It Is Used |
|---------|------------------------|
| Variables and data types | `float` for budget and amounts, `str` for categories and menu choices |
| Conditional statements | `if / elif / else` for menu routing and budget alerts |
| Loops | `while True` for the menu and for forcing valid input, `for` for aggregation |
| Lists and dictionaries | A list of dictionaries stores expense records, and a dictionary stores category totals |
| Functions | `add_expense()`, `get_total_spent()`, `get_category_totals()`, `view_summary()` and others |
| Exception handling | `try / except` blocks prevent crashes when text is typed instead of numbers |
| File handling | `json` module with `open()` to save and load data |

## How to Run

Requirements: Python 3.8 or higher. No external libraries are needed (only `json`, `os` and `datetime`).

```
python main.py
```

## Menu Options

| Option | What it does |
|--------|--------------|
| 1 | Add Expense |
| 2 | View All Expenses |
| 3 | View Summary |
| 4 | Delete Expense |
| 5 | Search by Category |
| 6 | Change Budget |
| 7 | Reset All Expenses |
| 8 | Exit |

## Sample Output

```
--- Category Breakdown ---
Food         Rs.  1000.00   66.7%  #############
Books        Rs.   500.00   33.3%  ######

Highest Spending Category: Food (Rs. 1000.00)
```

## Testing

The program was tested with:

- Normal input (valid budget and expenses)
- Boundary input (spending exactly 80% of the budget)
- Invalid input (text instead of numbers, zero, negative values, empty category)
- Budget exceeded case
- Restarting the program to check that saved data loads correctly

## Team Member Contributions (Milestone 1)

| Student | Contribution |
|---------|--------------|
| Arun (S26CSEU2492) | Computational logic for the summary feature, category aggregation dictionary, and `max()` key identification. |
| Kartike Yadav (S26CSEU2494) | Budget alert logic, 80% threshold calculation, and the global `total_spent` variable. |
| Ishaan Bhardwaj (S26CSEU2493) | Interactive `while` loop menu and `try-except` blocks for input validation. |
| Parv Girdhar (S26CSEU2497) | List-of-dictionaries schema for data storage and the core `add_expense()` function. |
| Kavya Chattha (S26CSEU2500) | Algorithm, Milestone 1 report, and the logic flow for file handling. |

## Challenges Faced and Learning

The major challenge was handling incorrect user input, because the program initially crashed when text was typed instead of numbers for amounts. This was solved with `try-except` blocks. Another difficulty was aggregating categorized data efficiently, which was solved by using dictionaries.

Through this project the team learned how to build robust interactive loops and how to apply dictionaries to summarize data.

## Future Improvements

- Charts and visualizations using matplotlib
- Monthly reports and date-wise filtering
- Separate budget limits for each category
- Graphical interface using Tkinter

## References

- Python Official Documentation (docs.python.org) for dictionary methods and exception handling
- Course material: Python Collaborative Project, Student Instructions (Course Code: 2026CSAE100)
