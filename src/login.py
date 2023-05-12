import streamlit as st
from db import DBManager

from config import Page


def login() -> None:
    st.title("🎈 Login Page")
    db: DBManager = st.session_state["database"]

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    loginbutton = st.button("Login")
    registerbutton = st.button("Sign Up")

    if loginbutton:
        is_valid_user = db.validate_user(username, password)
        if not is_valid_user:
            st.error("Wrong username/password")
        else:
            st.success("Logged in as user")
            st.session_state["islogged"] = Page.APP
            st.session_state["username"] = username
            st.experimental_rerun()

    if registerbutton:
        st.session_state["islogged"] = Page.REGISTER
        st.experimental_rerun()
