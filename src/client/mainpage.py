import streamlit as st

from config import Page
from machine_controller import MachineController
from utils import MachineInfo


def render_header(username: str) -> None:
    st.title("Hack The Clone :rocket:")

    name_col, logout_col = st.columns([7.5, 1])
    with name_col:
        st.write(f"Welcome {username}!")
    with logout_col:
        logout_button = st.button("Logout")

    if logout_button:
        st.session_state["page"] = Page.LOGIN
        st.experimental_rerun()


def render_machine_info(
    selected_machine: MachineInfo,
    state: str,
    machine_ip: str,
    mc_controller: MachineController,
) -> tuple[str, bool]:
    st.header(selected_machine.display_name)
    st.write(f"Difficulty: {':star:' * 5}")
    st.write(f"State: {state}")
    error = None
    success = None

    cont_col1, cont_col2, cont_col3 = st.columns([1, 1, 1])
    with cont_col1:
        start_button = st.button("Start", use_container_width=True)
        if start_button:
            if not machine_ip:
                image = mc_controller.build_image(selected_machine.container_path)
                container = mc_controller.run_machine(image)
                st.session_state["machine_ip"] = mc_controller.get_container_ip(container)
                st.experimental_rerun()
            else:
                error = "Machine already running - Stop it first"

    with cont_col2:
        stop_button = st.button("Stop", use_container_width=True)
        if stop_button:
            if machine_ip:
                container = mc_controller.stop_running_machine()
                mc_controller.delete_stopped_machine(container)
                st.session_state["machine_ip"] = None
                st.experimental_rerun()
            else:
                error = "No machine running - Start one first"

    with cont_col3:
        reset_button = st.button("Reset", use_container_width=True)
        if reset_button:
            if machine_ip:
                container = mc_controller.reset_running_machine()
                st.session_state["machine_ip"] = mc_controller.get_container_ip(container)
                st.experimental_rerun()
            else:
                error = "No machine running - Start one first"

    if error:
        st.error(error)

    if success:
        st.success(success)

    st.write("")
    root_field = st.text_input("Flag", placeholder="Insert flag here...")
    submit = st.button("Submit", use_container_width=True)

    return root_field, submit


def mainpage() -> None:
    username = st.session_state["username"]
    db = st.session_state["database"]
    mc_controller = st.session_state["machine_controller"]
    machine_list = st.session_state["machine_list"]
    machine_ip = st.session_state["machine_ip"]
    state = "🟢" if machine_ip else "🔴"

    render_header(username)

    select_box = st.selectbox(
        "Available machines",
        sorted([machine.container_name for machine in machine_list]),
        disabled=machine_ip is not None,
    )
    selected_machine = next(
        machine for machine in machine_list if machine.container_name == select_box
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        root_field, submit = render_machine_info(
            selected_machine,
            state,
            machine_ip,
            mc_controller,
        )
    with col2:
        st.write("")
        if selected_machine.image:
            st.image(str(selected_machine.image), use_column_width=True)
        else:
            st.image("./assets/placeholder.png", use_column_width=True)

    if machine_ip:
        st.info(f"Machine IP: {machine_ip}", icon="🤖")

    if submit:
        if root_field == selected_machine.flag:
            st.success("Flag is correct!")
        else:
            st.error("Flag is incorrect!")
