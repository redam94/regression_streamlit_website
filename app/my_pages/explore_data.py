import numpy as np
import streamlit as st
from streamlit import session_state as state
from components.utils.dataloader import TabularData
from components.datamodels.data import Wide, MFF

SUPORTED_DATA_TYPES = {
  'MFF': MFF,
  'WIDE': Wide
}

def upload_callback():
  state.file_loaded = not state.file_loaded
  if 'uploaded_data' not in state.keys():
    state.tabular_data = None
    return
  file = state.uploaded_data
  data = state.tabular_data
  if file:
    data = state.data_class(file)
  if data is None:
    return
  state.tabular_data = data

def initialize_state():
  if 'file_loaded' not in state.keys():
    state.file_loaded = False
  if 'file' not in state.keys():
    state.file = None
  if 'tabular_data' not in state.keys():
    state.tabular_data = None
  #if 'uploaded_data' not in state.keys():
  #  state.uploaded_data = None
  if 'data_type' not in state.keys():
    state.data_type = None

def upload_data() -> None:
  if not state.file_loaded:
    st.file_uploader('Upload Data', type=['csv', 'xlsx'], on_change=upload_callback, key='uploaded_data')
  else:
    st.button('Reload Data', on_click=upload_callback)

def change_data_type_callback():

  state.data_class = SUPORTED_DATA_TYPES[state.data_type]
  
def main():
  initialize_state()
  st.title('Please select and explore your data below')
  if 'tabular_data' not in state.keys() or state.tabular_data is None:
    st.selectbox('Select your data', SUPORTED_DATA_TYPES.keys(), key='data_type', on_change=change_data_type_callback)
  upload_data()
  if state.tabular_data is None:
    print("No data")
    st.stop()
  state.tabular_data.show_sample(10)
  state.tabular_data.data_info()
  state.tabular_data.plot_raw()
  

if __name__ == '__main__':
  main()