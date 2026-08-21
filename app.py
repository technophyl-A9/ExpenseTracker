import streamlit as st


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)


home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠"
)

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="📊"
)

add_expense = st.Page(
    "pages/add_expenses.py",
    title="Add Expense",
    icon="➕"
)

view_expenses = st.Page(
    "pages/view_expenses.py",
    title="View Expenses",
    icon="🧾"
)

edit_expense = st.Page(
    "pages/edit_expenses.py",
    title="Edit Expense",
    icon="✏️"
)

delete_expense = st.Page(
    "pages/delete_expenses.py",
    title="Delete Expense",
    icon="🗑️"
)

add_income = st.Page(
    "pages/add_income.py",
    title="Add Income",
    icon="➕"
)

view_income = st.Page(
    "pages/view_income.py",
    title="View Income",
    icon="🧾"
)

edit_income = st.Page(
    "pages/edit_income.py",
    title="Edit Income",
    icon="✏️"
)

delete_income = st.Page(
    "pages/delete_income.py",
    title="Delete Income",
    icon="🗑️"
)

reports = st.Page(
    "pages/reports.py",
    title="Reports",
    icon="📈"
)


pg = st.navigation(
    {
        "": [home, dashboard, reports],

        "💸 Expenses": [
            add_expense,
            view_expenses,
            edit_expense,
            delete_expense
        ],

        "💵 Income": [
            add_income,
            view_income,
            edit_income,
            delete_income
        ]
    }
)


pg.run()