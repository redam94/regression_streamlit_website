import streamlit as st

def transform_df_callback(df):
  for row in df.index:
    if row in st.session_state.old_df.index:
      st.session_state.old_df.loc[row] = df.loc[row]