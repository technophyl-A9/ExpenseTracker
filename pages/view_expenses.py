import streamlit as st
import pandas as pd

from db import get_all_expenses
from utils.categories import EXPENSE_CATEGORIES


st.title("🧾 View Expenses")


# ==================================================
# 1. GET EXPENSES
# ==================================================

expenses = get_all_expenses()


if not expenses:

    st.info("No expenses available.")
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
# 5. CATEGORY FILTER
# ==================================================

category_options = [
    "All"
] + EXPENSE_CATEGORIES

selected_category = st.selectbox(
    "🔎 Select Category",
    category_options
)


# ==================================================
# 6. APPLY MONTH FILTER
# ==================================================

filtered_expenses = expense_df.copy()


if selected_month != "All":

    filtered_expenses = filtered_expenses[
        filtered_expenses["Month"] == selected_month
    ]


# ==================================================
# 7. APPLY CATEGORY FILTER
# ==================================================

if selected_category != "All":

    filtered_expenses = filtered_expenses[
        filtered_expenses["Category"]
        == selected_category
    ]


# ==================================================
# 8. DISPLAY RESULTS
# ==================================================

st.subheader("🧾 Expense Records")


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
# 9. TOTAL
# ==================================================

if not filtered_expenses.empty:

    total = filtered_expenses["Amount"].sum()

    st.metric(
        "💰 Total Expenses",
        f"₹{total:,.2f}"
    )