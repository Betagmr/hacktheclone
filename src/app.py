import streamlit as st
from enum import Enum

class Page(int, Enum):
    LOGIN = 1
    REGISTER = 2
    APP = 3

def app() -> None:
    username = st.session_state['username']
    st.title("🎈 App Name")
    st.write(f"Hello {username}!")


def login() -> None:
    st.title("🎈 Login Page")
    st.write("Alex, Asier, Bidatz y Diego")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    loginbutton = st.button("Login")
    registerbutton = st.button("Sign Up")

    if loginbutton:
        if username == "admin" and password == "admin":
            st.success("Logged in as admin")
            st.session_state['islogged'] = Page.APP
            st.session_state['username'] = username   
            st.experimental_rerun()
        else:
            st.error("Wrong username/password")
    
    if registerbutton:
        st.session_state['islogged'] = Page.REGISTER
        st.experimental_rerun()


def register() -> None:
    st.title("🎈 Register Page")
    st.write("Alex, Asier, Bidatz y Diego")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    repeat_password = st.text_input("Repeat password", type="password")

    registerbutton = st.button("Sign Up")
    cancelbutton = st.button("Cancel")

    if registerbutton:
        if password == repeat_password:
            st.success("Registered")
            st.session_state['islogged'] = Page.LOGIN
            st.experimental_rerun()
        else:
            st.error("Passwords don't match")    

    if cancelbutton:
        st.session_state['islogged'] = Page.LOGIN
        st.experimental_rerun()


if __name__ == "__main__":
    if 'islogged' not in st.session_state:
        st.session_state['islogged'] = Page.LOGIN
    
    if st.session_state['islogged'] == Page.APP:
        app()
    elif st.session_state['islogged'] == Page.LOGIN:
        login()
    elif st.session_state['islogged'] == Page.REGISTER:
        register()