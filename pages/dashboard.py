import pandas as pd
import streamlit as st
import plotly.express as px


from db import get_all_income, get_all_expenses

st.title("Your Dashboard")

expenses = get_all_expenses()
income = get_all_income()

income_df = pd.DataFrame(
        income,
        columns=["ID","Amount", "source", "Date"]
)


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

expense_df["Date"] = pd.to_datetime(expense_df["Date"])

# Convert Date columns to datetime
expense_df["Date"] = pd.to_datetime(expense_df["Date"])
income_df["Date"] = pd.to_datetime(income_df["Date"])


# Now create the available months
expense_months = expense_df["Date"].dt.strftime("%Y-%m").unique()
income_months = income_df["Date"].dt.strftime("%Y-%m").unique()

available_months = sorted(
    set(expense_months) | set(income_months),
    reverse=True
)

# Month selector
if available_months:

    selected_month = st.selectbox(
        "📅 Select Month",
        available_months
    )

else:
    selected_month = None
    st.info("No income or expense data available.")

if selected_month:

    selected_expenses = expense_df[
        expense_df["Date"].dt.strftime("%Y-%m") == selected_month
    ]

    selected_income = income_df[
        income_df["Date"].dt.strftime("%Y-%m") == selected_month
    ]

#group all expenses by month
monthly_expenses = (
    expense_df
    .groupby(expense_df["Date"].dt.to_period("M"))["Amount"]
    .sum()
    .reset_index()
)



#group all expenses by category  and calculate total amount
category_expenses = (
    selected_expenses
    .groupby("Category")["Amount"]
    .sum()
    .reset_index()
)

total_expense = selected_expenses["Amount"].sum()

total_income = selected_income["Amount"].sum()

balance = total_income - total_expense


c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Income", total_income)

with c2:
    st.metric("Total Expenses", total_expense)

with c3:
    st.metric("Balance", balance)


#Expenses chart
st.subheader("Your Expenses!")

if not category_expenses.empty:

    fiq = px.pie(category_expenses,
                 names = "Category",
                 values = "Amount",
                 hole = 0.3
    )

    st.plotly_chart(fiq, use_container_width=True)

else:
    st.info("No expenses found!")

#monthly expenses cgart
st.subheader("📈 Monthly Expense Trend")

if not expense_df.empty:

    monthly_expenses = (
        expense_df
        .assign(Month=expense_df["Date"].dt.strftime("%Y-%m"))
        .groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        monthly_expenses,
        x="Month",
        y="Amount",
        labels={
            "Month": "Month",
            "Amount": "Expenses"
        }
    )

    fig.update_xaxes(type="category")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No expense data available yet.")


st.subheader(' Recent Transactions')

if not selected_expenses.empty:

    recent_expenses = selected_expenses.sort_values(
        "Date",
        ascending=False
    ).copy()

    recent_expenses["Date"] = (
        recent_expenses["Date"]
        .dt.strftime("%d %b %Y")
    )

    recent_expenses["Amount"] = (
        recent_expenses["Amount"]
        .apply(lambda x: f"₹{x:,.2f}")
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
    st.info("No expenses for the selected month.")