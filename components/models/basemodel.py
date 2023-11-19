import pandas as pd
import numpy as np
import matplotlib as mpl
from typing import Optional


class BaseModel:
  def __init__(self, name: str):
    self.name = name
    self.fitted_model = None
    
  def save(self):
    pass
  
  def fit(self, X: pd.DataFrame|np.ndarray, y: Optional[pd.Series|np.ndarray]=None):
    pass
  
  def predict(self, X: pd.DataFrame|np.ndarray) -> pd.Series|np.ndarray:
    pass
  
  def summary(self):
    if self.fitted_model is None:
      raise ValueError('Model has not been fitted yet')
    
  def plot_avm(self, X: pd.DataFrame|np.ndarray, *args) -> mpl.figure.Figure:
    pass
  
  def plot_resid(self, X: pd.DataFrame|np.ndarray, *args) -> mpl.figure.Figure:
    pass
  
  def metric(self) -> dict[str, float]:
    pass
  