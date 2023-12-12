import streamlit as st
from st_pages import show_pages_from_config, add_page_title


if __name__ == '__main__':
  show_pages_from_config()
 
  st.warning("""
             ## Will not be able to save/load data to/from file: 
             ### This will be added in the future this page is just a placeholder
             """)
  st.stop()