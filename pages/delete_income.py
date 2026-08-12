import streamlit as st
from db import get_all_income, delete_income

st.title("🗑️ Delete Income")

income = get_all_income()

if not income:
    st.info("No income records available to delete.")

else:
    income_options = {
        f"{item[3]} - {item[2]} - ₹{item[1]:.2f}": item[0]
        for item in income
    }

    selected_income = st.selectbox(
        "Select Income",
        list(income_options.keys())
    )

    selected_id = income_options[selected_income]

    selected_data = next(
        item for item in income
        if item[0] == selected_id
    )

    st.warning(
        f"Are you sure you want to delete "
        f"₹{selected_data[1]:,.2f} income from "
        f"{selected_data[2]}?"
    )

    confirm = st.checkbox(
        "Yes, I want to delete this income."
    )

    if confirm:

        if st.button("🗑️ Delete Income"):

            delete_income(selected_id)

            st.success("Income deleted successfully! 🎉")