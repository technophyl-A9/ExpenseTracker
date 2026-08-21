import streamlit as st


st.title("💰 Expense Tracker")

st.write(
    "Manage your income, expenses and finances from one place."
)

st.divider()


# ==================================================
# DASHBOARD
# ==================================================

st.subheader("📊 Dashboard")

st.write(
    "View your income, expenses, balance and spending analysis."
)

if st.button(
    "📊 Open Dashboard",
    use_container_width=True
):
    st.switch_page("pages/dashboard.py")


st.divider()


# ==================================================
# EXPENSES
# ==================================================

st.subheader("💸 Expenses")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("➕ Add Expense", use_container_width=True):
        st.switch_page("pages/add_expenses.py")

with col2:
    if st.button("🧾 View Expenses", use_container_width=True):
        st.switch_page("pages/view_expenses.py")

with col3:
    if st.button("✏️ Edit Expense", use_container_width=True):
        st.switch_page("pages/edit_expenses.py")

with col4:
    if st.button("🗑️ Delete Expense", use_container_width=True):
        st.switch_page("pages/delete_expenses.py")


st.divider()


# ==================================================
# INCOME
# ==================================================

st.subheader("💵 Income")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("➕ Add Income", use_container_width=True):
        st.switch_page("pages/add_income.py")

with col2:
    if st.button("🧾 View Income", use_container_width=True):
        st.switch_page("pages/view_income.py")

with col3:
    if st.button("✏️ Edit Income", use_container_width=True):
        st.switch_page("pages/edit_income.py")

with col4:
    if st.button("🗑️ Delete Income", use_container_width=True):
        st.switch_page("pages/delete_income.py")


st.divider()


# ==================================================
# REPORTS
# ==================================================

st.subheader("📈 Reports")

st.write(
    "Analyze your monthly spending and financial activity."
)

if st.button(
    "📈 Open Reports",
    use_container_width=True
):
    st.switch_page("pages/reports.py")


st.divider()

st.caption(
    "Expense Tracker • Manage your money better 💰"
)