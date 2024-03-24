import os
import yaml
import streamlit_authenticator as stauth
import streamlit as st
from yaml.loader import SafeLoader
import home

# with open("./config.yaml") as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config["credentials"],
#     config["cookie"]["name"],
#     config["cookie"]["key"],
#     config["cookie"]["expiry_days"],
#     config["preauthorized"],
# )

# authenticator.login()

# if st.session_state["authentication_status"] is True:
#     home.render_page(authenticator)
# elif st.session_state["authentication_status"] is False:
#     st.error("Username/password is incorrect")
# elif st.session_state["authentication_status"] is None:
#     st.warning("Please enter your username and password")

home.render_page()
