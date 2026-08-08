import db
import streamlit as st

from pages.add_expenses import submitted

st.title("Add Income")

amount = st.number_input("Amount to add",
                         min_value=1.0,
                         step=1.0)

source = st.selectbox(
    "Income Source",
        [
            "Salary",
            "Freelancing",
            "Business",
            "Bonus",
            "Investment",
            "Other"
        ]
    )

date = st.date_input("Date")

submitted = st.button("Save your Income")
if submitted:
    if amount<=0:
        st.error("Please enter amount greater than 0")

    else:
        db.add_income(
            amount,
            source,
            date
        )

        st.success("Saved your Income!")