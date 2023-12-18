import pandas as pd
import numpy as np
import matplotlib as mpl
from typing import Optional
import streamlit as st
from streamlit import session_state as state
from uuid import uuid4



class BaseModel:
  description: str = 'No description provided'

  def __init__(self, name: str, data):
    self._uuid = uuid4()
    self.name = name
    self.fitted_model = None
    self.regression_data = None
    self.data = data
    self.transform_df = None
    self.file_loaded = False
    
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
  
  
  def set_params(self) -> None:
    pass
  
  def __str__(self) -> str:
    return f"{self.name} Model\n{self._uuid}"

  

  def __repr__(self) -> str:
    return f"BaseModel"
  