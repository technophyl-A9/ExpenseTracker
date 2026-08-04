import streamlit as st

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
    st.success("Saved Expense!")
