from config.db import fetch_one
import streamlit as st
import datetime

# get user 
def authenticate_user(username, password):

    query = "SELECT * FROM users WHERE username = %s"
    user = fetch_one(query, (username,))

    if not user:
        return None

    # simple check (for now)
    if password == user["password"]:
        user.pop("password", None)
        return user

    return None

# login 
def show_login(cookie_manager):
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Sales Intelligence Hub</h1>", unsafe_allow_html=True)
    st.header("Login") 
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)

        if user:
            # session (for current run)
            st.session_state.logged_in = True
            st.session_state.user = user
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=2)
            cookie_manager['user_id'] = user['user_id']
            cookie_manager.save()
            st.rerun()
        else:
            st.error("Invalid username or password")

