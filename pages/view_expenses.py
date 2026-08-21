import streamlit as st
import pandas as pd

from db import get_all_expenses
from utils.categories import EXPENSE_CATEGORIES
from utils.auth import get_current_user_id


# ==================================================
# PAGE TITLE
# ==================================================

st.title("View Expenses")


# ==================================================
# 1. GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:

    st.error("Please login to view your expenses.")
    st.stop()


# ==================================================
# 2. GET USER EXPENSES
# ==================================================

expenses = get_all_expenses(user_id)


if not expenses:

    st.info("No expenses available.")
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
# 6. CATEGORY FILTER
# ==================================================

category_options = [
    "All"
] + EXPENSE_CATEGORIES

selected_category = st.selectbox(
    "Select Category",
    category_options
)


# ==================================================
# 7. APPLY FILTERS
# ==================================================

filtered_expenses = expense_df.copy()


# Month filter
if selected_month != "All":

    filtered_expenses = filtered_expenses[
        filtered_expenses["Month"]
        == selected_month
    ]


# Category filter
if selected_category != "All":

    filtered_expenses = filtered_expenses[
        filtered_expenses["Category"]
        == selected_category
    ]


# ==================================================
# 8. DISPLAY RESULTS
# ==================================================

st.subheader("Expense Records")


if filtered_expenses.empty:

    st.info(
        "No expenses found for the selected filters."
    )

else:

    display_df = filtered_expenses[
        [
            "Date",
            "Category",
            "Description",
            "Payment Mode",
            "Amount"
        ]
    ].copy()

    # Format amount
    display_df["Amount"] = (
        display_df["Amount"]
        .apply(
            lambda x: f"₹{x:,.2f}"
        )
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 9. TOTAL EXPENSES
# ==================================================

if not filtered_expenses.empty:

    total = filtered_expenses["Amount"].sum()

    st.metric(
        "Total Expenses",
        f"₹{total:,.2f}"
    )