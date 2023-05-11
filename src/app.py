from config import Page

import streamlit as st

from login import login
from register import register
from db import DBManager


def app() -> None:
    username = st.session_state["username"]
    db = st.session_state["database"]
    st.title("🎈 App Name")
    st.write(f"Hello {username}!")

    logoutbutton = st.button("Logout")
    if logoutbutton:
        st.session_state["islogged"] = Page.LOGIN
        st.experimental_rerun()


if __name__ == "__main__":
    if "islogged" not in st.session_state:
        st.session_state["islogged"] = Page.LOGIN

    if "database" not in st.session_state:
        st.session_state["database"] = DBManager()
        st.session_state["database"].create_database()

    if st.session_state["islogged"] == Page.APP:
        app()
    elif st.session_state["islogged"] == Page.LOGIN:
        login()
    elif st.session_state["islogged"] == Page.REGISTER:
        register()
