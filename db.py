import sqlite3
import os

# Database file location
DATABASE_PATH = "data/expense_tracker.db"


def create_database():
    """
    Creates the SQLite database and required tables
    if they do not already exist.
    """

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Connect to database
    connection = sqlite3.connect(DATABASE_PATH)

    # Create cursor
    cursor = connection.cursor()

    # Income Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            source TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Expense Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            payment_mode TEXT,
            date TEXT NOT NULL
        )
    """)

    # Save changes
    connection.commit()

    # Close database
    connection.close()

def add_income(amount, source, date):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO income (amount, source, date)
        VALUES (?, ?, ?)
    """, (amount, source, date))

    connection.commit()
    connection.close()

def add_expense(amount, category, description, payment_mode, date):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, payment_mode, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        amount,
        category,
        description,
        payment_mode,
        date
    ))

    connection.commit()
    connection.close()

def update_expense(
    expense_id,
    amount,
    category,
    description,
    payment_mode,
    date
):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            amount = ?,
            category = ?,
            description = ?,
            payment_mode = ?,
            date = ?
        WHERE id = ?
    """, (
        amount,
        category,
        description,
        payment_mode,
        date,
        expense_id
    ))

    connection.commit()
    connection.close()

def delete_expense(expense_id):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()

def get_all_income():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM income
        order by date DESC
            """)
    data = cursor.fetchall()
    connection.close()
    return data

def get_all_expenses():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        ORDER BY date DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data



if __name__ == "__main__":
    create_database()
#    print("✅ Database created successfully!")
 #   print(get_all_expenses())
  #  print(get_all_income())