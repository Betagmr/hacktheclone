import streamlit as st

from config import Page
from db import DBManager
from login import login
from register import register


def app() -> None:
    username = st.session_state["username"]
    db = st.session_state["database"]
    st.title("Hack The Clone :rocket:")

    name_col, logout_col = st.columns([7.5, 1])

    with name_col:
        st.write(f"Welcome {username}!")
    with logout_col:
        logoutbutton = st.button("Logout")

    selectBox = st.selectbox(
        "Máquinas disponibles", ["Máquina 1", "Máquina 2", "Máquina 3"]
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Máquina 1")
        st.write(f"Dificultad: {':star:' * 5}")
        st.write("Estado: :red_circle:")

        cont_col1, cont_col2, cont_col3 = st.columns([1, 1, 1])
        with cont_col1:
            start_button = st.button("Start", use_container_width=True)
        with cont_col2:
            resume_button = st.button("Stop", use_container_width=True)
        with cont_col3:
            start_button = st.button("Reset", use_container_width=True)

        st.write("")

        root_field = st.text_input("Flag", placeholder="Insert flag here...")
        submit = st.button("Submit", use_container_width=True)

    with col2:
        st.write("")
        st.image("./assets/placeholder.png", use_column_width=True)

    if logoutbutton:
        st.session_state["islogged"] = Page.LOGIN
        st.experimental_rerun()


if __name__ == "__main__":
    if "islogged" not in st.session_state:
        st.session_state["islogged"] = Page.LOGIN

    if "database" not in st.session_state:
        st.session_state["database"] = DBManager()

    if st.session_state["islogged"] == Page.APP:
        app()
    elif st.session_state["islogged"] == Page.LOGIN:
        login()
    elif st.session_state["islogged"] == Page.REGISTER:
        register()
