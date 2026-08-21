import streamlit as st
import pandas as pd

from db import get_all_expenses, delete_expense


st.title("🗑️ Delete Expense")


# ==================================================
# 1. GET EXPENSES
# ==================================================

expenses = get_all_expenses()


if not expenses:

    st.info("No expenses available to delete.")
    st.stop()


# ==================================================
# 2. CREATE DATAFRAME
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
# 3. CREATE MONTH COLUMN
# ==================================================

expense_df["Month"] = (
    expense_df["Date"]
    .astype(str)
    .str.slice(0, 7)
)


# ==================================================
# 4. MONTH FILTER
# ==================================================

months = sorted(
    expense_df["Month"].unique(),
    reverse=True
)

month_options = ["All"] + months

selected_month = st.selectbox(
    "📅 Select Month",
    month_options
)


# ==================================================
# 5. FILTER BY MONTH
# ==================================================

filtered_expenses = expense_df.copy()


if selected_month != "All":

    filtered_expenses = filtered_expenses[
        filtered_expenses["Month"] == selected_month
    ]


# ==================================================
# 6. CHECK FILTERED RESULTS
# ==================================================

if filtered_expenses.empty:

    st.info(
        "No expenses found for the selected month."
    )

    st.stop()


# ==================================================
# 7. SELECT EXPENSE
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


selected_id = expense_options[selected_expense]


# ==================================================
# 8. GET SELECTED EXPENSE
# ==================================================

selected_data = filtered_expenses[
    filtered_expenses["ID"] == selected_id
].iloc[0]


# ==================================================
# 9. SHOW WARNING
# ==================================================

st.warning(
    f"Are you sure you want to delete "
    f"₹{selected_data['Amount']:,.2f} spent on "
    f"{selected_data['Category']}?"
)


# ==================================================
# 10. CONFIRMATION
# ==================================================

confirm = st.checkbox(
    "Yes, I want to delete this expense."
)


# ==================================================
# 11. DELETE
# ==================================================

if confirm:

    if st.button("🗑️ Delete Expense"):

        delete_expense(selected_id)

        st.success(
            "Expense deleted successfully! 🎉"
        )