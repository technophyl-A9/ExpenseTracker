import streamlit as st


def login_user(user):

    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["username"] = user["username"]
    st.session_state["email"] = user["email"]


def logout_user():

    st.session_state.clear()


def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


def get_current_user_id():

    return st.session_state.get(
        "user_id"
    )