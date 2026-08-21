import streamlit as st
from datetime import datetime

from db import get_all_income, update_income
from utils.auth import get_current_user_id


# ==================================================
# PAGE TITLE
# ==================================================

st.title("Edit Income")


# ==================================================
# 1. GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:

    st.error("Please login to edit income.")
    st.stop()


# ==================================================
# 2. GET USER'S INCOME
# ==================================================

income = get_all_income(user_id)


if not income:

    st.info("No income records available to edit.")
    st.stop()


# ==================================================
# 3. GET AVAILABLE MONTHS
# ==================================================

months = sorted(
    set(
        item[3][:7]
        for item in income
    ),
    reverse=True
)


# ==================================================
# 4. SELECT MONTH
# ==================================================

selected_month = st.selectbox(
    "Select Month",
    months
)


# ==================================================
# 5. FILTER INCOME BY MONTH
# ==================================================

month_income = [
    item
    for item in income
    if item[3][:7] == selected_month
]


if not month_income:

    st.info(
        "No income records found for the selected month."
    )
    st.stop()


# ==================================================
# 6. SELECT INCOME
# ==================================================

income_options = {
    f"{item[3]} - {item[2]} - ₹{item[1]:,.2f}":
    item[0]
    for item in month_income
}


selected_income = st.selectbox(
    "Select Income",
    list(income_options.keys())
)


selected_id = income_options[selected_income]


# ==================================================
# 7. GET SELECTED INCOME
# ==================================================

selected_data = next(
    item
    for item in month_income
    if item[0] == selected_id
)


income_id = selected_data[0]
amount = selected_data[1]
source = selected_data[2]
date = selected_data[3]


# ==================================================
# 8. EDIT FORM
# ==================================================

with st.form("edit_income_form"):

    new_amount = st.number_input(
        "Amount",
        min_value=1.0,
        value=float(amount),
        step=1.0
    )

    new_source = st.selectbox(
        "Income Source",
        [
            "Salary",
            "Freelancing",
            "Business",
            "Bonus",
            "Investment",
            "Other"
        ],
        index=(
            [
                "Salary",
                "Freelancing",
                "Business",
                "Bonus",
                "Investment",
                "Other"
            ].index(source)
            if source in [
                "Salary",
                "Freelancing",
                "Business",
                "Bonus",
                "Investment",
                "Other"
            ]
            else 0
        )
    )

    new_date = st.date_input(
        "Date",
        value=datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()
    )

    submitted = st.form_submit_button(
        "Update Income"
    )


# ==================================================
# 9. UPDATE DATABASE
# ==================================================

if submitted:

    update_income(
        user_id,
        income_id,
        new_amount,
        new_source,
        str(new_date)
    )

    st.success(
        "Income updated successfully!"
    )

    st.rerun()