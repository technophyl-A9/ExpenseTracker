import streamlit as st
from db import get_all_expenses, delete_expense

st.title("🗑️ Delete Expense")

expenses = get_all_expenses()

if not expenses:
    st.info("No expenses available to delete.")

else:
    expense_options = {
        f"{expense[5]} - {expense[2]} - ₹{expense[1]:.2f}": expense[0]
        for expense in expenses
    }

    selected_expense = st.selectbox(
        "Select Expense",
        list(expense_options.keys())
    )

    selected_id = expense_options[selected_expense]

    selected_data = next(
        expense for expense in expenses
        if expense[0] == selected_id
    )

    st.warning(
        f"Are you sure you want to delete "
        f"₹{selected_data[1]:.2f} spent on "
        f"{selected_data[2]}?"
    )

    confirm = st.checkbox(
        "Yes, I want to delete this expense."
    )

    if confirm:

        if st.button("🗑️ Delete Expense"):
            delete_expense(selected_id)
            st.success("Expense deleted successfully! 🎉")