import numpy as np
import streamlit as st
from streamlit import session_state as state
from components.utils.dataloader import TabularData
from components.datamodels.data import Wide, MFF

SUPORTED_DATA_TYPES = {
  'MFF': MFF,
  'WIDE': Wide
}

def main():
  st.title('Please select and explore your data below')
  st.selectbox('Select your data', SUPORTED_DATA_TYPES.keys(), key='data_type')
  st.file_uploader('Upload your data here', type=['csv', 'xlsx'], key='data_file')
  if 'data_file' not in state.keys() or state.data_file is None:
    st.stop()
  
  if 'data_type' not in state.keys() or state.data_type is None:
    st.stop()
    
  data = SUPORTED_DATA_TYPES[state.data_type](state.data_file)
  data.show_sample(10)
  
    
  
  
  

if __name__ == '__main__':
  main()