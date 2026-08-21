import streamlit as st

from db import add_income
from utils.auth import get_current_user_id


# ==================================================
# PAGE TITLE
# ==================================================

st.title("Add Income")


# ==================================================
# 1. GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:

    st.error("Please login to add income.")
    st.stop()


# ==================================================
# 2. INCOME FORM
# ==================================================

with st.form("income_form"):

    amount = st.number_input(
        "Amount",
        min_value=1.0,
        step=1.0
    )

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

    date = st.date_input(
        "Date"
    )

    submitted = st.form_submit_button(
        "Save Income"
    )


# ==================================================
# 3. SAVE INCOME
# ==================================================

if submitted:

    if amount <= 0:

        st.error(
            "Please enter an amount greater than 0."
        )

    else:

        add_income(
            user_id,
            amount,
            source,
            str(date)
        )

        st.success(
            "Income saved successfully!"
        )