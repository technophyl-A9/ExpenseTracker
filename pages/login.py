import streamlit as st

from db import authenticate_user
from utils.auth import login_user


st.title("Login")

st.write(
    "Login to your Expense Tracker account."
)


email = st.text_input(
    "Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your password"
)


if st.button(
    "Login",
    use_container_width=True
):

    email = email.strip().lower()

    if not email:

        st.error("Please enter your email.")

    elif not password:

        st.error("Please enter your password.")

    else:

        user = authenticate_user(
            email,
            password
        )

        if user:

            login_user(user)

            st.rerun()

        else:

            st.error(
                "Invalid email or password."
            )