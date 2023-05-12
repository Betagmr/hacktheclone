import streamlit as st

from client import login, mainpage, register
from config import Page
from db import DBManager
from machine_controller import MachineController
from utils import get_machines_info


def main():
    if "page" not in st.session_state:
        st.session_state["page"] = Page.LOGIN
        st.session_state["database"] = DBManager()
        st.session_state["machine_list"] = get_machines_info()
        st.session_state["machine_controller"] = MachineController()
        st.session_state["machine_ip"] = None

    match st.session_state["page"]:
        case Page.APP:
            mainpage()
        case Page.LOGIN:
            login()
        case Page.REGISTER:
            register()


if __name__ == "__main__":
    main()
