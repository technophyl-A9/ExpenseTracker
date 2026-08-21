import sqlite3
import os
import hashlib
import secrets


# ==================================================
# DATABASE CONFIGURATION
# ==================================================

DATABASE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "expense_tracker.db"
)


# ==================================================
# CREATE DATABASE AND TABLES
# ==================================================

def create_database():

    os.makedirs(
        os.path.dirname(DATABASE_PATH),
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # ------------------------------------------------
    # Income Table
    # ------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            source TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # ------------------------------------------------
    # Expense Table
    # ------------------------------------------------

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

    # ------------------------------------------------
    # Users Table
    # ------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    # Add user_id columns
    add_user_id_columns()


# ==================================================
# ADD USER ID COLUMNS
# ==================================================

def add_user_id_columns():

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # ------------------------------------------------
    # Expenses
    # ------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(expenses)"
    )

    expense_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "user_id" not in expense_columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN user_id INTEGER
        """)

    # ------------------------------------------------
    # Income
    # ------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(income)"
    )

    income_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "user_id" not in income_columns:

        cursor.execute("""
            ALTER TABLE income
            ADD COLUMN user_id INTEGER
        """)

    connection.commit()
    connection.close()


# ==================================================
# PASSWORD HASHING
# ==================================================

def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(
    password,
    stored_hash
):

    try:

        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return secrets.compare_digest(
            password_hash.hex(),
            hash_hex
        )

    except (ValueError, TypeError):

        return False


# ==================================================
# CREATE USER
# ==================================================

def create_user(
    username,
    email,
    password
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    try:

        password_hash = hash_password(
            password
        )

        cursor.execute("""
            INSERT INTO users
            (
                username,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
        """, (
            username,
            email,
            password_hash
        ))

        user_id = cursor.lastrowid

        # --------------------------------------------
        # Check number of users
        # --------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
        """)

        user_count = cursor.fetchone()[0]

        # --------------------------------------------
        # Assign existing old data to first user
        # --------------------------------------------

        if user_count == 1:

            cursor.execute("""
                UPDATE expenses
                SET user_id = ?
                WHERE user_id IS NULL
            """, (user_id,))

            cursor.execute("""
                UPDATE income
                SET user_id = ?
                WHERE user_id IS NULL
            """, (user_id,))

        connection.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError as error:

        error_message = str(error).lower()

        if "username" in error_message:

            return False, "Username already exists."

        if "email" in error_message:

            return False, "Email already exists."

        return False, "Unable to create account."

    finally:

        connection.close()


# ==================================================
# AUTHENTICATE USER
# ==================================================

def authenticate_user(
    email,
    password
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            email,
            password_hash
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    if user is None:

        return None

    if verify_password(
        password,
        user[3]
    ):

        return {
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }

    return None


# ==================================================
# INCOME FUNCTIONS
# ==================================================

def add_income(
    user_id,
    amount,
    source,
    date
):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO income
        (
            user_id,
            amount,
            source,
            date
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        amount,
        source,
        date
    ))

    connection.commit()
    connection.close()

def update_income(
    user_id,
    income_id,
    amount,
    source,
    date
):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE income
        SET
            amount = ?,
            source = ?,
            date = ?
        WHERE id = ?
        AND user_id = ?
    """, (
        amount,
        source,
        date,
        income_id,
        user_id
    ))

    connection.commit()
    connection.close()

def delete_income(user_id, income_id):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM income
        WHERE id = ?
        AND user_id = ?
    """, (
        income_id,
        user_id
    ))

    connection.commit()
    connection.close()
def get_all_income(user_id):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            source,
            date
        FROM income
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))

    data = cursor.fetchall()

    connection.close()

    return data
# ==================================================
# EXPENSE FUNCTIONS
# ==================================================

def add_expense(
    user_id,
    amount,
    category,
    description,
    payment_mode,
    date
):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (
            user_id,
            amount,
            category,
            description,
            payment_mode,
            date
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        amount,
        category,
        description,
        payment_mode,
        date
    ))

    connection.commit()
    connection.close()


def get_all_expenses(user_id):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            category,
            description,
            payment_mode,
            date
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))

    data = cursor.fetchall()

    connection.close()

    return data


def update_expense(
    user_id,
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
        AND user_id = ?
    """, (
        amount,
        category,
        description,
        payment_mode,
        date,
        expense_id,
        user_id
    ))

    connection.commit()
    connection.close()


def delete_expense(user_id, expense_id):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (
        expense_id,
        user_id
    ))

    connection.commit()
    connection.close()
# ==================================================
# DATABASE INITIALIZATION
# ==================================================

if __name__ == "__main__":

    create_database()

    print(
        "Database initialized successfully."
    )