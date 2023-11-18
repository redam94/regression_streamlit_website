import streamlit as st
import pandas as pd


from .utils.constants import TRANSFORM_DETAIL_COLUMNS, COLUMN_SETTINGS
from .callbacks.data_frames import transform_df_callback

def model_params():
  pass


def select_variables(data):
  
  time = st.selectbox('Time', ['None']+list(data.columns))
  group = st.selectbox('Group', ['None']+list(data.columns))
  
  y = st.selectbox('Dependent Variable', data.columns)
  x = st.multiselect('Independent Variable', data.columns)
  
  test = pd.DataFrame(
  columns=TRANSFORM_DETAIL_COLUMNS, 
    index=[y]+x if not x is None else [y],
  )
  if 'old_df' not in st.session_state:
    st.session_state['old_df'] = pd.DataFrame(
      columns=TRANSFORM_DETAIL_COLUMNS,
      index=data.columns,
      data=[['Linear', 0.0, 0.0, 100.0, 0, 0.0] for _ in range(len(data.columns))])
  
  for row in test.index:
    if row in st.session_state.old_df.index:
      test.loc[row] = st.session_state.old_df.loc[row]
    else:
      test.loc[row] = ['Linear', 0.0, 0.0, 100.0, 0, 0.0]
  
        
  test = st.data_editor(test, column_config=COLUMN_SETTINGS, on_change=transform_df_callback, args=(test,))
  
  transform_df_callback(test)
  
  return y, x, test, time, group