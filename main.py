import streamlit as st
from auth.login import show_login
from config.db import fetch_one
from streamlit_cookies_manager import CookieManager

# Initialize the manager without a password
cookies = CookieManager()

# Wait for the component to load
if not cookies.ready():
    st.stop()

# st.write(dict(cookies))

# Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None


user_cookie = cookies.get("user_id")
if not st.session_state.logged_in and user_cookie:
    user = fetch_one("SELECT * FROM users WHERE user_id = %s", (int(user_cookie),))
    if user:
        user.pop("password", None)
        st.session_state.logged_in = True
        st.session_state.user = user

# Routing
if not st.session_state.logged_in:
    st.navigation([st.Page(lambda:show_login(cookies), title="Login")]).run()
else:
    pg = st.navigation([
        st.Page("views/dashboard.py", title="Dashboard"),
        # st.Page("views/other.py", title="Other"),
        st.Page("views/add_sale.py", title="Add Sale"),
        st.Page('views/add_payment.py',title="Add Payment"),
        st.Page('views/common_query.py',title="Common Queries")
    ])
    pg.run()

    # logout
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        del cookies["user_id"]
        cookies.save()
        st.rerun()
