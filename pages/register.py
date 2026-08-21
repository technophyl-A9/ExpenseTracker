import streamlit as st

from db import create_user


st.title("Create Account")

st.write("Create your Expense Tracker account.")


# ==================================================
# REGISTRATION FORM
# ==================================================

username = st.text_input(
    "Username",
    placeholder="Enter your username"
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

confirm_password = st.text_input(
    "Confirm Password",
    type="password",
    placeholder="Re-enter your password"
)


# ==================================================
# CREATE ACCOUNT
# ==================================================

if st.button(
    "Create Account",
    use_container_width=True
):

    username = username.strip()
    email = email.strip().lower()

    # ----------------------------------------------
    # Validation
    # ----------------------------------------------

    if not username:

        st.error("Please enter a username.")

    elif not email:

        st.error("Please enter your email.")

    elif not password:

        st.error("Please enter a password.")

    elif len(password) < 6:

        st.error(
            "Password must contain at least 6 characters."
        )

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    else:

        # ------------------------------------------
        # Create user
        # ------------------------------------------

        success, message = create_user(
            username,
            email,
            password
        )

        if success:

            st.success(message)

            st.info(
                "Your account has been created. "
                "Please go to Login."
            )

        else:

            st.error(message)