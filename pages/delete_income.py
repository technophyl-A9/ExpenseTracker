import streamlit as st

from db import get_all_income, delete_income
from utils.auth import get_current_user_id


# ==================================================
# PAGE TITLE
# ==================================================

st.title("Delete Income")


# ==================================================
# 1. GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:

    st.error("Please login to delete income.")
    st.stop()


# ==================================================
# 2. GET USER'S INCOME
# ==================================================

income = get_all_income(user_id)


if not income:

    st.info("No income records available to delete.")
    st.stop()


# ==================================================
# 3. SELECT INCOME
# ==================================================

income_options = {
    f"{item[3]} - {item[2]} - ₹{item[1]:,.2f}":
    item[0]
    for item in income
}


selected_income = st.selectbox(
    "Select Income",
    list(income_options.keys())
)


selected_id = income_options[selected_income]


# ==================================================
# 4. GET SELECTED INCOME
# ==================================================

selected_data = next(
    item
    for item in income
    if item[0] == selected_id
)


# ==================================================
# 5. SHOW INCOME DETAILS
# ==================================================

st.write("### Income Details")

st.write(
    f"**Date:** {selected_data[3]}"
)

st.write(
    f"**Source:** {selected_data[2]}"
)

st.write(
    f"**Amount:** ₹{selected_data[1]:,.2f}"
)


# ==================================================
# 6. DELETE WARNING
# ==================================================

st.warning(
    f"Are you sure you want to delete "
    f"₹{selected_data[1]:,.2f} income from "
    f"{selected_data[2]}?"
)


# ==================================================
# 7. CONFIRMATION
# ==================================================

confirm = st.checkbox(
    "Yes, I want to delete this income."
)


# ==================================================
# 8. DELETE INCOME
# ==================================================

if confirm:

    if st.button(
        "Delete Income",
        type="primary"
    ):

        delete_income(
            user_id,
            selected_id
        )

        st.success(
            "Income deleted successfully!"
        )

        st.rerun()