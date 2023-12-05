import pandas as pd
import numpy as np
import matplotlib as mpl
from typing import Optional
import streamlit as st
from streamlit import session_state as state
from ..utils.dataloader import TabularData


class BaseModel:
  description: str = 'No description provided'

  def __init__(self, name: str):
    self.name = name
    self.fitted_model = None
    self.regression_data = None
    self.data = None
    self.transform_df = None
    
  def save(self):
    pass
  
  def fit(self) -> None:
    pass
  
  def predict(self, X: Optional[pd.DataFrame|np.ndarray] = None) -> pd.Series|np.ndarray:
    pass
  
  def summary(self) -> pd.DataFrame:
    if self.fitted_model is None:
      raise ValueError('Model has not been fitted yet')
    
  def plot_raw(self):
    pass

  def plot_transforms(self):
    pass

  def plot_avm(self, X: pd.DataFrame|np.ndarray, *args) -> mpl.figure.Figure:
    pass
  
  def plot_resid(self, X: pd.DataFrame|np.ndarray, *args) -> mpl.figure.Figure:
    pass
  
  def metric(self) -> dict[str, float]:
    pass
  
  def upload_data(self) -> None:
    self.data = st.file_uploader('Upload Data', type=['csv', 'xlsx'])
    if self.data is None:
      st.stop()
    
    self.data = TabularData(self.data)
    
    
    
  def show_sample(self, rows: int):
    with st.expander("Data Preview", expanded=False):
      st.table(self.data.sample(rows))
  
  def data_info(self):
    with st.expander("Data Info", expanded=False):
      st.write(self.data.describe())
  
  def _scatter_data(self, data:pd.DataFrame, name: str = 'Scatter Plot'):
    with st.expander(name, expanded=False):
      columns = st.columns(2)
      with columns[0]:
        y = st.selectbox('Y', data.columns, key=f"{name}_y")
        logy = st.checkbox('Log Y', key=f"{name}_logy")
      with columns[1]:
        x = st.selectbox('X', data.columns, key=f"{name}_x")
        logx = st.checkbox('Log X', key=f"{name}_logx")
        
        
      color = st.selectbox('Color', [None] + list(data.columns), key=f"{name}_color")

      fig, ax = mpl.pyplot.subplots(1, figsize=(10, 5))
      data.plot(x=x, y=y, color=data[color] if color is not None else None, kind='scatter', ax=ax, logy=logy, logx=logx)
        
      st.pyplot(fig)

  
  def set_params(self) -> None:
    pass
  

  

  
  