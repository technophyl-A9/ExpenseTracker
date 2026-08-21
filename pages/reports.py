import streamlit as st
import pandas as pd
import plotly.express as px

from db import get_all_expenses, get_all_income


st.title("📊 Expense Reports")


# GET DATA FROM DATABASE

expenses = get_all_expenses()
income = get_all_income()

# CREATE DATAFRAMES

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


# --------------------------------------------------
# HANDLE EMPTY DATA
# --------------------------------------------------

if expense_df.empty and income_df.empty:

    st.info("No income or expense data available yet.")
    st.stop()


# --------------------------------------------------
# CONVERT DATES
# --------------------------------------------------

if not expense_df.empty:
    expense_df["Date"] = pd.to_datetime(expense_df["Date"])

if not income_df.empty:
    income_df["Date"] = pd.to_datetime(income_df["Date"])


# --------------------------------------------------
# GET AVAILABLE MONTHS
# --------------------------------------------------

expense_months = set()

income_months = set()

if not expense_df.empty:
    expense_months = set(
        expense_df["Date"].dt.strftime("%Y-%m").unique()
    )

if not income_df.empty:
    income_months = set(
        income_df["Date"].dt.strftime("%Y-%m").unique()
    )


available_months = sorted(
    expense_months | income_months,
    reverse=True
)


# --------------------------------------------------
# MONTH SELECTOR
# --------------------------------------------------

selected_month = st.selectbox(
    "📅 Select Month",
    available_months
)


# --------------------------------------------------
# FILTER SELECTED MONTH
# --------------------------------------------------

if not expense_df.empty:

    selected_expenses = expense_df[
        expense_df["Date"].dt.strftime("%Y-%m") == selected_month
    ]

else:

    selected_expenses = pd.DataFrame(
        columns=expense_df.columns
    )


if not income_df.empty:

    selected_income = income_df[
        income_df["Date"].dt.strftime("%Y-%m") == selected_month
    ]

else:

    selected_income = pd.DataFrame(
        columns=income_df.columns
    )


# --------------------------------------------------
# CALCULATE TOTALS
# --------------------------------------------------

total_income = selected_income["Amount"].sum()

total_expenses = selected_expenses["Amount"].sum()

savings = total_income - total_expenses


# --------------------------------------------------
# SUMMARY CARDS
# --------------------------------------------------

st.subheader("📌 Monthly Summary")

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
        "💰 Savings",
        f"₹{savings:,.2f}"
    )


# --------------------------------------------------
# SAVINGS PERCENTAGE
# --------------------------------------------------

if total_income > 0:

    savings_percentage = (
        savings / total_income
    ) * 100

    st.metric(
        "📈 Savings Percentage",
        f"{savings_percentage:.2f}%"
    )

else:

    st.info("No income recorded for this month.")


# --------------------------------------------------
# CATEGORY BREAKDOWN
# --------------------------------------------------

st.subheader("📊 Expense by Category")


if not selected_expenses.empty:

    category_expenses = (
        selected_expenses
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Amount",
            ascending=False
        )
    )

    st.dataframe(
        category_expenses,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # CATEGORY CHART
    # --------------------------------------------------

    fig = px.pie(
        category_expenses,
        names="Category",
        values="Amount",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No expenses recorded for the selected month."
    )


# --------------------------------------------------
# HIGHEST SPENDING CATEGORY
# --------------------------------------------------

if not selected_expenses.empty:

    highest_category = (
        selected_expenses
        .groupby("Category")["Amount"]
        .sum()
        .idxmax()
    )

    highest_category_amount = (
        selected_expenses
        .groupby("Category")["Amount"]
        .sum()
        .max()
    )

    st.subheader("🔝 Highest Spending Category")

    st.write(
        f"**{highest_category}** — "
        f"₹{highest_category_amount:,.2f}"
    )


# --------------------------------------------------
# TRANSACTION SUMMARY
# --------------------------------------------------

st.subheader("🧾 Transaction Summary")

expense_count = len(selected_expenses)

income_count = len(selected_income)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Expense Transactions",
        expense_count
    )

with col2:

    st.metric(
        "Income Transactions",
        income_count
    )