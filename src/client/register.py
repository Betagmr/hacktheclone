import streamlit as st

from config import Page
from db import DBManager


def register() -> None:
    st.title("🎈 Register Page")
    db: DBManager = st.session_state["database"]

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    repeat_password = st.text_input("Repeat password", type="password")

    register_button = st.button("Sign Up")
    cancel_button = st.button("Cancel")

    if register_button:
        if password == repeat_password:
            exists_username = db.exists_username(username)
            if not exists_username:
                db.add_user(username, password)
                st.success("Registered")
                st.session_state["page"] = Page.LOGIN
                st.experimental_rerun()
            else:
                st.error("Username already exists")
        else:
            st.error("Passwords don't match")

    if cancel_button:
        st.session_state["page"] = Page.LOGIN
        st.experimental_rerun()
