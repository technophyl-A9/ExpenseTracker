import streamlit as st

import db
from db import add_expense


st.title("Add Expenses")

with st.form("expense_form"):
    amount = st.number_input(
        "Amount",
        min_value=1,
        step=1,)

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Entertainment",
            "Baladoor",

        ]
    )

    description = st.text_input(
        "Description",
    )

    payment_mode = st.selectbox(
        "Payment Mode",
        [
            "UPI",
            "Cash",
            "Credit Card",
            "Debit Card",
        ]
    )

    date = st.date_input("Date")

    submitted = st.form_submit_button(
        "💾 Save Expense"
    )

if submitted:
    if amount < 0 :
        st.error("Please enter amount greater than 0")

    else:
        db.add_expense(amount, category, description, payment_mode, str(date))

        st.success("Saved Expense!")

