import streamlit as st
import pandas as pd

from db import get_all_income
from utils.auth import get_current_user_id


# ==================================================
# PAGE TITLE
# ==================================================

st.title("View Income")


# ==================================================
# 1. GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:

    st.error("Please login to view your income.")
    st.stop()


# ==================================================
# 2. GET USER'S INCOME
# ==================================================

income = get_all_income(user_id)


if not income:

    st.info("No income records available.")
    st.stop()


# ==================================================
# 3. CREATE DATAFRAME
# ==================================================

income_df = pd.DataFrame(
    income,
    columns=[
        "ID",
        "Amount",
        "Source",
        "Date"
    ]
)


# ==================================================
# 4. CREATE MONTH COLUMN
# ==================================================

income_df["Month"] = (
    income_df["Date"]
    .astype(str)
    .str.slice(0, 7)
)


# ==================================================
# 5. MONTH FILTER
# ==================================================

months = sorted(
    income_df["Month"].unique(),
    reverse=True
)

month_options = ["All"] + months

selected_month = st.selectbox(
    "Select Month",
    month_options
)


# ==================================================
# 6. APPLY MONTH FILTER
# ==================================================

filtered_income = income_df.copy()


if selected_month != "All":

    filtered_income = filtered_income[
        filtered_income["Month"] == selected_month
    ]


# ==================================================
# 7. DISPLAY RESULTS
# ==================================================

st.subheader("Income Records")


if filtered_income.empty:

    st.info(
        "No income found for the selected month."
    )

else:

    display_df = filtered_income[
        [
            "Date",
            "Source",
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
# 8. TOTAL INCOME
# ==================================================

if not filtered_income.empty:

    total_income = filtered_income["Amount"].sum()

    st.metric(
        "Total Income",
        f"₹{total_income:,.2f}"
    )