import pandas as pd
import streamlit as st
import plotly.express as px

from db import get_all_income, get_all_expenses


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Expense Tracker Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Your Dashboard")


# ==================================================
# 1. GET DATA FROM DATABASE
# ==================================================

expenses = get_all_expenses()
income = get_all_income()


# ==================================================
# 2. CREATE DATAFRAMES
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
# 3. CONVERT DATES
# ==================================================

if not expense_df.empty:

    expense_df["Date"] = pd.to_datetime(
        expense_df["Date"],
        errors="coerce"
    )

    expense_df = expense_df.dropna(
        subset=["Date"]
    ).copy()

    expense_df["Month"] = (
        expense_df["Date"]
        .dt.strftime("%Y-%m")
    )

else:

    # Make sure the column exists
    expense_df["Month"] = pd.Series(
        dtype="object"
    )


if not income_df.empty:

    income_df["Date"] = pd.to_datetime(
        income_df["Date"],
        errors="coerce"
    )

    income_df = income_df.dropna(
        subset=["Date"]
    ).copy()

    income_df["Month"] = (
        income_df["Date"]
        .dt.strftime("%Y-%m")
    )

else:

    # Make sure the column exists
    income_df["Month"] = pd.Series(
        dtype="object"
    )


# ==================================================
# 4. CHECK WHETHER DATA EXISTS
# ==================================================

if expense_df.empty and income_df.empty:

    st.info(
        "No income or expense data available yet."
    )

    st.stop()


# ==================================================
# 5. GET AVAILABLE MONTHS
# ==================================================

expense_months = set(
    expense_df["Month"].dropna().unique()
)

income_months = set(
    income_df["Month"].dropna().unique()
)

available_months = sorted(
    expense_months | income_months,
    reverse=True
)


if not available_months:

    st.info("No valid dates available.")

    st.stop()


# ==================================================
# 6. MONTH SELECTOR
# ==================================================

st.subheader("📅 Select Month")

selected_month = st.selectbox(
    "Month",
    available_months,
    label_visibility="collapsed"
)


# ==================================================
# 7. FILTER SELECTED MONTH
# ==================================================

selected_expenses = expense_df[
    expense_df["Month"] == selected_month
].copy()

selected_income = income_df[
    income_df["Month"] == selected_month
].copy()


# ==================================================
# 8. CALCULATE TOTALS
# ==================================================

total_income = selected_income["Amount"].sum()

total_expenses = selected_expenses["Amount"].sum()

balance = total_income - total_expenses


# ==================================================
# 9. SUMMARY CARDS
# ==================================================

st.subheader("Monthly Summary")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "💵 Total Income",
        f"₹{total_income:,.2f}"
    )


with col2:

    st.metric(
        "💸 Total Expenses",
        f"₹{total_expenses:,.2f}"
    )


with col3:

    st.metric(
        "💰 Balance",
        f"₹{balance:,.2f}"
    )


# ==================================================
# 10. EXPENSES BY CATEGORY
# ==================================================

st.subheader("🍕 Expenses by Category")


if not selected_expenses.empty:

    category_expenses = (
        selected_expenses
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_expenses,
        names="Category",
        values="Amount",
        hole=0.3
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

else:

    st.info(
        "No expenses found for the selected month."
    )


# ==================================================
# 11. MONTHLY EXPENSE TREND
# ==================================================

st.subheader("📈 Monthly Expense Trend")


if not expense_df.empty:

    monthly_expenses = (
        expense_df
        .groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    fig_monthly = px.bar(
        monthly_expenses,
        x="Month",
        y="Amount",
        labels={
            "Month": "Month",
            "Amount": "Expenses"
        }
    )

    fig_monthly.update_xaxes(
        type="category"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

else:

    st.info(
        "No expense data available yet."
    )


# ==================================================
# 12. RECENT TRANSACTIONS
# ==================================================

st.subheader("🧾 Recent Transactions")


if not selected_expenses.empty:

    recent_expenses = (
        selected_expenses
        .sort_values(
            "Date",
            ascending=False
        )
        .copy()
    )

    recent_expenses["Date"] = (
        recent_expenses["Date"]
        .dt.strftime("%d %b %Y")
    )

    recent_expenses["Amount"] = (
        recent_expenses["Amount"]
        .apply(
            lambda x: f"₹{x:,.2f}"
        )
    )

    recent_expenses = recent_expenses[
        [
            "Date",
            "Category",
            "Description",
            "Payment Mode",
            "Amount"
        ]
    ]

    st.dataframe(
        recent_expenses,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No expenses for the selected month."
    )