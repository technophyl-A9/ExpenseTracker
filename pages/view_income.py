import streamlit as st
import pandas as pd

from db import get_all_income


st.title("💰 View Income")

income = get_all_income()

if not income:

    st.info("No income records available.")

else:

    income_df = pd.DataFrame(
        income,
        columns=[
            "ID",
            "Amount",
            "Source",
            "Date"
        ]
    )

    income_df["Amount"] = income_df["Amount"].apply(
        lambda x: f"₹{x:,.2f}"
    )

    st.dataframe(
        income_df[
            [
                "Date",
                "Source",
                "Amount"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )