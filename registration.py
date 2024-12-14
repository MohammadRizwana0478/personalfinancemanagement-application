import sqlite3
import hashlib
import unittest

# Database connection setup
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Create the users, transactions, and budgets tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')
conn.commit()

# cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER,
#                     type TEXT,  # 'income' or 'expense'
#                     category TEXT,
#                     amount REAL,
#                     date TEXT,
#                     FOREIGN KEY (user_id) REFERENCES users (id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    type TEXT,  -- 'income' or 'expense'
                    category TEXT,
                    amount REAL,
                    date TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id))''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                    user_id INTEGER,
                    category TEXT,
                    amount REAL,
                    FOREIGN KEY (user_id) REFERENCES users (id))''')
conn.commit()

# User Registration
def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")

# User Login
def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()
    if user:
        print(f"Login successful! Welcome {username}.")
        return user[0]  # Returning user_id
    else:
        print("Invalid credentials.")
        return None

# Add Transaction
def add_transaction(user_id, transaction_type, category, amount, date):
    try:
        cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                       (user_id, transaction_type, category, amount, date))
        conn.commit()
        print(f"{transaction_type.capitalize()} added successfully!")
    except sqlite3.Error as e:
        print(f"Error adding transaction: {e}")

# Set Budget
def set_budget(user_id, category, amount):
    try:
        cursor.execute("REPLACE INTO budgets (user_id, category, amount) VALUES (?, ?, ?)", (user_id, category, amount))
        conn.commit()
        print(f"Budget for {category} set to ${amount}.")
    except sqlite3.Error as e:
        print(f"Error setting budget: {e}")

# Check Budget
def check_budget(user_id, category):
    try:
        cursor.execute("SELECT amount FROM budgets WHERE user_id=? AND category=?", (user_id, category))
        budget = cursor.fetchone()
        
        if budget:
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id=? AND category=? AND type='expense'", (user_id, category))
            total_expense = cursor.fetchone()[0] or 0
            remaining_budget = budget[0] - total_expense
            print(f"Budget: ${budget[0]} | Spent: ${total_expense} | Remaining: ${remaining_budget}")
        else:
            print("No budget set for this category.")
    except sqlite3.Error as e:
        print(f"Error checking budget: {e}")

# Generate Report
def generate_report(user_id, year, month=None):
    try:
        query = "SELECT type, category, amount FROM transactions WHERE user_id=? AND strftime('%Y', date)=? "
        params = [user_id, str(year)]

        if month:
            query += "AND strftime('%m', date)=? "
            params.append(str(month).zfill(2))

        cursor.execute(query, params)
        transactions = cursor.fetchall()

        income, expenses = 0, 0
        for transaction in transactions:
            if transaction[0] == 'income':
                income += transaction[2]
            else:
                expenses += transaction[2]

        savings = income - expenses

        print(f"Report for {month}/{year}:" if month else f"Report for {year}:")
        print(f"Total Income: ${income:.2f}")
        print(f"Total Expenses: ${expenses:.2f}")
        print(f"Total Savings: ${savings:.2f}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Register a new user and login
    register_user("Rizwana", "securepassword123")
    user_id = login_user("Rizwana", "securepassword123")

    if user_id:
        # Add transactions
        add_transaction(user_id, "income", "Salary", 2000, "2024-12-09")
        add_transaction(user_id, "expense", "Food", 150, "2024-12-10")
        add_transaction(user_id, "expense", "Rent", 800, "2024-12-11")

        # Set and check budget
        set_budget(user_id, "Food", 500)
        check_budget(user_id, "Food")

        # Generate report for the month
        generate_report(user_id, 2024, 12)

    # Close the connection when done
    conn.close()

# Unit tests for functionality (simplified)
class TestFinanceApp(unittest.TestCase):

    def test_registration(self):
        register_user("test_user", "password123")
        self.assertTrue(login_user("test_user", "password123"))

        with self.assertRaises(ValueError):
            register_user("test_user", "newpassword")

    def test_add_transaction(self):
        add_transaction(1, 'income', 'Salary', 2000, '2024-12-09')
        self.assertEqual(generate_report(1, 2024, 12)[0], 2000)

    def test_no_income_transaction(self):
        self.assertEqual(generate_report(1, 2024, 11)[0], 0)

if __name__ == '__main__':
    unittest.main()
