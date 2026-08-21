import streamlit as st
from datetime import datetime

from db import get_all_expenses, update_expense
from utils.categories import EXPENSE_CATEGORIES


st.title("✏️ Edit Expense")


# ==================================================
# 1. GET EXPENSES
# ==================================================

expenses = get_all_expenses()


if not expenses:

    st.info("No expenses available to edit.")
    st.stop()


# ==================================================
# 2. GET AVAILABLE MONTHS
# ==================================================

months = sorted(
    set(
        expense[5][:7]
        for expense in expenses
    ),
    reverse=True
)


# ==================================================
# 3. SELECT MONTH
# ==================================================

selected_month = st.selectbox(
    "📅 Select Month",
    months
)


# ==================================================
# 4. FILTER EXPENSES BY MONTH
# ==================================================

month_expenses = [
    expense
    for expense in expenses
    if expense[5][:7] == selected_month
]


# ==================================================
# 5. SELECT EXPENSE
# ==================================================

expense_options = {
    f"{expense[5]} - {expense[2]} - ₹{expense[1]:.2f}":
    expense[0]
    for expense in month_expenses
}


selected_expense = st.selectbox(
    "Select Expense",
    list(expense_options.keys())
)


selected_id = expense_options[selected_expense]


# ==================================================
# 6. GET SELECTED EXPENSE
# ==================================================

selected_data = next(
    expense
    for expense in month_expenses
    if expense[0] == selected_id
)


expense_id = selected_data[0]
amount = selected_data[1]
category = selected_data[2]
description = selected_data[3]
payment_mode = selected_data[4]
date = selected_data[5]


# ==================================================
# 7. EDIT FORM
# ==================================================

with st.form("edit_expense_form"):

    new_amount = st.number_input(
        "Amount",
        min_value=1.0,
        value=float(amount),
        step=1.0
    )

    new_category = st.selectbox(
        "Category",
        EXPENSE_CATEGORIES,
        index=(
            EXPENSE_CATEGORIES.index(category)
            if category in EXPENSE_CATEGORIES
            else 0
        )
    )

    new_description = st.text_input(
        "Description",
        value=description or ""
    )

    payment_modes = [
        "UPI",
        "Cash",
        "Credit Card",
        "Debit Card"
    ]

    new_payment_mode = st.selectbox(
        "Payment Mode",
        payment_modes,
        index=(
            payment_modes.index(payment_mode)
            if payment_mode in payment_modes
            else 0
        )
    )

    new_date = st.date_input(
        "Date",
        value=datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()
    )

    submitted = st.form_submit_button(
        "✏️ Update Expense"
    )


# ==================================================
# 8. UPDATE DATABASE
# ==================================================

if submitted:

    update_expense(
        expense_id,
        new_amount,
        new_category,
        new_description,
        new_payment_mode,
        str(new_date)
    )

    st.success(
        "Expense updated successfully! 🎉"
    )