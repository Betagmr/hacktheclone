import streamlit as st

from config import Page
from db import DBManager


def login() -> None:
    st.title("🎈 Login Page")
    db: DBManager = st.session_state["database"]

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col_1, col_2 = st.columns([1, 8.5])
    with col_1:
        login_button = st.button("Login")
    with col_2:
        register_button = st.button("Sign Up")

    if login_button:
        is_valid_user = db.validate_user(username, password)
        if not is_valid_user:
            st.error("Wrong username/password")
        else:
            st.success("Logged in as user")
            st.session_state["page"] = Page.APP
            st.session_state["username"] = username
            st.experimental_rerun()

    if register_button:
        st.session_state["page"] = Page.REGISTER
        st.experimental_rerun()
