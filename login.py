import streamlit as st

def login():
    st.set_page_config(page_title="Login")
    st.title("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar Sesión"):
        if username == "admin" and password == "123":
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.experimental_rerun()
