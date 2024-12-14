# personalfinancemanagement-application
Finance Tracking App
A simple Python-based finance tracking application that helps users register, log in, manage transactions (income and expenses), set budgets for different categories, and generate financial reports. This application uses an SQLite database to store user information, transactions, and budgets.
Features
User Registration and Login: Allows users to register, log in, and manage their accounts securely.
Transaction Management: Users can add, update, and delete transactions (income or expenses).
Budget Management: Users can set and check their budgets for various categories (e.g., "Food", "Entertainment").
Financial Reports: Generate income, expense, and savings reports for a specific month or year.
Technologies Used
SQLite: Lightweight, file-based relational database used to store user data, transactions, and budgets.
Python: The application is written in Python and uses standard libraries like sqlite3 for database interaction and hashlib for password hashing.
Unit Testing: The code includes unit tests to verify that key functionality works as expected.
Setup and Installation
Prerequisites
Python 3.x (preferably 3.6 or later)
sqlite3 (comes pre-installed with Python)
Installation Steps
Clone the repository or download the script to your local machine.

bash
git clone <repo-url>
cd <repo-directory>
Install Dependencies (if any additional dependencies are added in the future, though the current version uses only Python's built-in libraries).

Run the Application: You can run the Python script directly:
python finance_app.py
Database Schema
The application uses an SQLite database (finance.db) with the following schema:
1. Users Table
Stores the user information, including a hashed password for security.
sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT);
2. Transactions Table
Stores all income and expense transactions for each user.

sql
Copy code
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,  -- 'income' or 'expense'
    category TEXT,
    amount REAL,
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
3. Budgets Table
Stores the budget limits for various categories (e.g., "Food", "Rent").

sql
Copy code
CREATE TABLE IF NOT EXISTS budgets (
    user_id INTEGER,
    category TEXT,
    amount REAL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
How to Use
1. Register a New User
To register a new user, you need to call the register_user function. The password is hashed before being stored in the database for security.
2. Login a User
Log in with the username and password. If the credentials are correct, the function will return the user_id.
3. Add a Transaction
You can add either an income or an expense. The transaction is saved in the transactions table.
4. Set a Budget
You can set a budget for a specific category (e.g., "Food", "Entertainment"). If a budget already exists, it will be replaced.
5. Check Budget
To check the remaining budget for a category, use the check_budget function. It shows the total budget, total expenses, and the remaining balance.
6. Generate a Financial Report
You can generate a report for a specific month or year. The report includes the total income, total expenses, and the resulting savings.
Unit Tests
The application includes a set of unit tests to verify the core functionality:

User Registration and Login: Test if users can register and log in.
Transaction Management: Test if transactions can be added correctly.
Budget Management: Test if budgets are set and checked correctly.
Report Generation: Test if reports are generated correctly for a specific period.
To run the tests, use:
bash
python -m unittest test_finance_app.py
Closing the Database
After performing operations, it's important to close the database connection. This is typically done in your main application code after you’re done interacting with the database:
Contributing
Feel free to fork the repository and submit pull requests with improvements or bug fixes. You can contribute by:

Adding new features or enhancing the existing ones.
Fixing bugs or improving the performance of the application.
Writing additional unit tests to cover more scenarios.
License
This project is licensed under the MIT License – see the LICENSE file for details.

Support
If you have any issues or questions, feel free to open an issue on the GitHub repository or reach out via email.

This README gives a comprehensive guide to understanding and using the Finance Tracking App. It includes instructions for installation, usage, examples, and contributing to the project.




