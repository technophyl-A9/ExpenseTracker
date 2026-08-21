import streamlit as st
import pandas as pd

from db import get_all_expenses, delete_expense
from utils.auth import get_current_user_id


# ==================================================
# PAGE TITLE
# ==================================================

st.title("Delete Expense")


# ==================================================
# 1. GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:

    st.error("Please login to delete expenses.")
    st.stop()


# ==================================================
# 2. GET USER'S EXPENSES
# ==================================================

expenses = get_all_expenses(user_id)


if not expenses:

    st.info("No expenses available to delete.")
    st.stop()


# ==================================================
# 3. CREATE DATAFRAME
# ==================================================

expense_df = pd.DataFrame(
    expenses,
    columns=[
        "ID",
        "Amount",
        "Category",
        "Description",
        "Payment Mode",
        "Date"
    ]
)


# ==================================================
# 4. CREATE MONTH COLUMN
# ==================================================

expense_df["Month"] = (
    expense_df["Date"]
    .astype(str)
    .str.slice(0, 7)
)


# ==================================================
# 5. MONTH FILTER
# ==================================================

months = sorted(
    expense_df["Month"].unique(),
    reverse=True
)

month_options = ["All"] + months

selected_month = st.selectbox(
    "Select Month",
    month_options
)


# ==================================================
# 6. FILTER BY MONTH
# ==================================================

filtered_expenses = expense_df.copy()


if selected_month != "All":

    filtered_expenses = filtered_expenses[
        filtered_expenses["Month"] == selected_month
    ]


# ==================================================
# 7. CHECK FILTERED RESULTS
# ==================================================

if filtered_expenses.empty:

    st.info(
        "No expenses found for the selected month."
    )

    st.stop()


# ==================================================
# 8. SELECT EXPENSE
# ==================================================

expense_options = {
    f"{expense['Date']} - "
    f"{expense['Category']} - "
    f"₹{expense['Amount']:.2f}":
    expense["ID"]
    for _, expense in filtered_expenses.iterrows()
}


selected_expense = st.selectbox(
    "Select Expense",
    list(expense_options.keys())
)


selected_id = expense_options[
    selected_expense
]


# ==================================================
# 9. GET SELECTED EXPENSE
# ==================================================

selected_data = filtered_expenses[
    filtered_expenses["ID"] == selected_id
].iloc[0]


# ==================================================
# 10. SHOW EXPENSE DETAILS
# ==================================================

st.write("### Expense Details")

st.write(
    f"**Date:** {selected_data['Date']}"
)

st.write(
    f"**Category:** {selected_data['Category']}"
)

st.write(
    f"**Description:** {selected_data['Description']}"
)

st.write(
    f"**Payment Mode:** {selected_data['Payment Mode']}"
)

st.write(
    f"**Amount:** ₹{selected_data['Amount']:,.2f}"
)


# ==================================================
# 11. DELETE WARNING
# ==================================================

st.warning(
    f"Are you sure you want to delete "
    f"₹{selected_data['Amount']:,.2f} spent on "
    f"{selected_data['Category']}?"
)


# ==================================================
# 12. CONFIRMATION
# ==================================================

confirm = st.checkbox(
    "Yes, I want to delete this expense."
)


# ==================================================
# 13. DELETE EXPENSE
# ==================================================

if confirm:

    if st.button(
        "Delete Expense",
        type="primary"
    ):

        delete_expense(
            user_id,
            selected_id
        )

        st.success(
            "Expense deleted successfully!"
        )

        st.rerun()