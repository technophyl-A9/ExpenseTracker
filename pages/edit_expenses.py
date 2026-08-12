import streamlit as st
from db import get_all_expenses, update_expense

st.title("✏️ Edit Expense")

expenses = get_all_expenses()

if not expenses:
    st.info("No expenses available to edit.")

else:
    # Create a readable list for the dropdown
    expense_options = {
        f"{expense[5]} - {expense[2]} - ₹{expense[1]:.2f}": expense[0]
        for expense in expenses
    }

    selected_expense = st.selectbox(
        "Select Expense",
        list(expense_options.keys())
    )

    selected_id = expense_options[selected_expense]

    # Find the selected expense
    selected_data = next(
        expense for expense in expenses
        if expense[0] == selected_id
    )

    expense_id = selected_data[0]
    amount = selected_data[1]
    category = selected_data[2]
    description = selected_data[3]
    payment_mode = selected_data[4]
    date = selected_data[5]

    with st.form("edit_expense_form"):

        new_amount = st.number_input(
            "Amount",
            min_value=1.0,
            value=float(amount),
            step=1.0
        )

        categories = [
            "Food",
            "Travel",
            "Entertainment",
            "Baladoor"
        ]

        new_category = st.selectbox(
            "Category",
            categories,
            index=categories.index(category)
            if category in categories else 0
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
            index=payment_modes.index(payment_mode)
            if payment_mode in payment_modes else 0
        )

        new_date = st.date_input(
            "Date",
            value=date
        )

        submitted = st.form_submit_button(
            "✏️ Update Expense"
        )

    if submitted:

        update_expense(
            expense_id,
            new_amount,
            new_category,
            new_description,
            new_payment_mode,
            str(new_date)
        )

        st.success("Expense updated successfully! 🎉")