import streamlit as st
import pandas as pd
from db import get_all_expenses

st.title("My Expenses !")

expenses = get_all_expenses()
df = pd.DataFrame(
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

total_expense = df["Amount"].sum()

total_records = len(df)

average_expense = df["Amount"].mean()

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "💰 Total Expense",
        f"₹ {total_expense:.2f}"
    )

with c2:
    st.metric(
        "📋 Total Records",
        total_records
    )

with c3:
    st.metric(
        "📊 Average Expense",
        f"₹ {average_expense:.2f}"
    )

df = df[
    [
        "Date",
        "Category",
        "Description",
        "Payment Mode",
        "Amount"
    ]
]

df["Amount"] = df["Amount"].apply(lambda x: f"₹{x:.2f}")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


#st.write(expenses)
