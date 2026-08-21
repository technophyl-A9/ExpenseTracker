import streamlit as st

from utils.auth import get_current_user_id, logout_user
from db import get_all_income, get_all_expenses


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Expense Tracker",
    layout="wide"
)


# ==================================================
# GET CURRENT USER
# ==================================================

user_id = get_current_user_id()

if user_id is None:
    st.error("Please login to continue.")
    st.stop()


# ==================================================
# GET USER DETAILS
# ==================================================

username = st.session_state.get(
    "username",
    "User"
)

email = st.session_state.get(
    "email",
    ""
)


# ==================================================
# GET USER DATA
# ==================================================

income = get_all_income(user_id)
expenses = get_all_expenses(user_id)


# ==================================================
# CALCULATE TOTALS
# ==================================================

total_income = sum(
    item[1]
    for item in income
)

total_expenses = sum(
    item[1]
    for item in expenses
)

balance = total_income - total_expenses


# ==================================================
# HEADER
# ==================================================

col1, col2 = st.columns(
    [5, 1]
)

with col1:

    st.title(
        f"Welcome back, {username}"
    )

    st.write(
        "Manage your income and expenses "
        "from one place."
    )


with col2:

    with st.popover(
        f"👤 {username}",
        use_container_width=True
    ):

        st.subheader("Profile")

        st.write(
            f"**Username:** {username}"
        )

        st.write(
            f"**Email:** {email}"
        )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            logout_user()

            st.rerun()
# ==================================================
# SUMMARY
# ==================================================

st.subheader("Financial Overview")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Income",
        f"₹{total_income:,.2f}"
    )


with col2:

    st.metric(
        "Total Expenses",
        f"₹{total_expenses:,.2f}"
    )


with col3:

    st.metric(
        "Balance",
        f"₹{balance:,.2f}"
    )


# ==================================================
# QUICK ACTIONS
# ==================================================

st.subheader("Quick Actions")

col5, col6, = st.columns(2)
col1, col2, col3, col4 = st.columns(4)

with col5:

    if st.button(
        "Dashboard",
        use_container_width=True
    ):

        st.switch_page(
            "pages/dashboard.py"
        )

with col6:

    if st.button(
        "Reports",
        use_container_width=True
    ):

        st.switch_page(
            "pages/reports.py"
        )



with col1:

    if st.button(
        "Add Expense",
        use_container_width=True
    ):

        st.switch_page(
            "pages/add_expenses.py"
        )


with col2:

    if st.button(
        "View Expenses",
        use_container_width=True
    ):

        st.switch_page(
            "pages/view_expenses.py"
        )


with col3:

    if st.button(
        "Add Income",
        use_container_width=True
    ):

        st.switch_page(
            "pages/add_income.py"
        )


with col4:

    if st.button(
        "View Income",
        use_container_width=True
    ):

        st.switch_page(
            "pages/view_income.py"
        )
