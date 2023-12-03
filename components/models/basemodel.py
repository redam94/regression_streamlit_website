import pandas as pd
import numpy as np
import matplotlib as mpl
from typing import Optional
import streamlit as st
from ..utils.dataloader import TabularData


class BaseModel:
  def __init__(self, name: str):
    self.name = name
    self.fitted_model = None
    self.data = None
    
  def save(self):
    pass
  
  def fit(self) -> None:
    pass
  
  def predict(self, X: Optional[pd.DataFrame|np.ndarray] = None) -> pd.Series|np.ndarray:
    pass
  
  def summary(self) -> pd.DataFrame:
    if self.fitted_model is None:
      raise ValueError('Model has not been fitted yet')
    
  def plot_avm(self, X: pd.DataFrame|np.ndarray, *args) -> mpl.figure.Figure:
    pass
  
  def plot_resid(self, X: pd.DataFrame|np.ndarray, *args) -> mpl.figure.Figure:
    pass
  
  def metric(self) -> dict[str, float]:
    pass
  
  def upload_data(self) -> None:
    self.data = st.file_uploader('Upload Data', type=['csv', 'xlsx'])
    if self.data is not None:
      self.data = TabularData(self.data)
      with st.expander("Data Preview", expanded=False):
        st.table(self.data.head())
      with st.expander("Data Info", expanded=False):
        st.write(self.data.describe())
      with st.expander("Scatter Plot", expanded=False):
        columns = st.columns(2)
        with columns[0]:
          y = st.selectbox('Y', self.data.columns)
          logy = st.checkbox('Log Y')
        with columns[1]:
          x = st.selectbox('X', self.data.columns)
          logx = st.checkbox('Log X')
        
        
        color = st.selectbox('Color', [None] + list(self.data.columns))

        fig, ax = mpl.pyplot.subplots(1, figsize=(10, 5))
        self.data.plot(x=x, y=y, color=self.data[color] if color is not None else None, kind='scatter', ax=ax, logy=logy, logx=logx)
        
        st.pyplot(fig)
        
  
  
  def set_params(self) -> None:
    pass
  

  

  
  