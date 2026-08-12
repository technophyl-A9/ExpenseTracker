import streamlit as st
from db import get_all_income, update_income

st.title("✏️ Edit Income")

income = get_all_income()

if not income:
    st.info("No income records available to edit.")

else:
    # Create dropdown options
    income_options = {
        f"{item[3]} - {item[2]} - ₹{item[1]:.2f}": item[0]
        for item in income
    }

    selected_income = st.selectbox(
        "Select Income",
        list(income_options.keys())
    )

    selected_id = income_options[selected_income]

    # Get selected income record
    selected_data = next(
        item for item in income
        if item[0] == selected_id
    )

    income_id = selected_data[0]
    amount = selected_data[1]
    source = selected_data[2]
    date = selected_data[3]

    with st.form("edit_income_form"):

        new_amount = st.number_input(
            "Amount",
            min_value=1.0,
            value=float(amount),
            step=1.0
        )

        new_source = st.text_input(
            "Source",
            value=source
        )

        new_date = st.date_input(
            "Date",
            value=date
        )

        submitted = st.form_submit_button(
            "✏️ Update Income"
        )

    if submitted:

        update_income(
            income_id,
            new_amount,
            new_source,
            str(new_date)
        )

        st.success("Income updated successfully! 🎉")
