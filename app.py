import streamlit as st
from st_pages import show_pages_from_config, add_page_title
from components.utils.constants import ORGINIZATIONS



show_pages_from_config()

def main_page():
  if 'org' not in st.session_state:
    st.session_state['org'] = 'None'
  if st.session_state.org == 'None':
    st.title("Welcome! Please select an organization to get started.")
    org = st.selectbox('Organization', ORGINIZATIONS)
    st.session_state['org'] = org
  else:
    st.title("Please select a client.")
    st.session_state['client'] = st.selectbox('Client', ['Client 1', 'Client 2', 'Client 3'])
  
  
  
  


if __name__ == '__main__':
  main_page()