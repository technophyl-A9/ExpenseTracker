import streamlit as st

from utils.categories import EXPENSE_CATEGORIES
from utils.auth import get_current_user_id
from db import add_expense


# ==================================================
# PAGE TITLE
# ==================================================

st.title("Add Expense")


# ==================================================
# GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:
    st.error("Please login to add an expense.")
    st.stop()


# ==================================================
# EXPENSE FORM
# ==================================================

with st.form("expense_form"):

    amount = st.number_input(
        "Amount",
        min_value=1.0,
        step=1.0
    )

    category = st.selectbox(
        "Category",
        EXPENSE_CATEGORIES
    )

    description = st.text_input(
        "Description"
    )

    payment_mode = st.selectbox(
        "Payment Mode",
        [
            "UPI",
            "Cash",
            "Credit Card",
            "Debit Card"
        ]
    )

    date = st.date_input(
        "Date"
    )

    submitted = st.form_submit_button(
        "Save Expense"
    )


# ==================================================
# SAVE EXPENSE
# ==================================================

if submitted:

    if amount <= 0:

        st.error(
            "Please enter an amount greater than 0."
        )

    else:

        add_expense(
            user_id,
            amount,
            category,
            description,
            payment_mode,
            str(date)
        )

        st.success(
            "Expense saved successfully!"
        )