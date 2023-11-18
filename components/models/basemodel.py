import pandas as pd
import numpy as np
from typing import Optional

class BaseModel:
  def __init__(self, name: str):
    self.name = name
    self.fitted_model = None
    
  def save(self):
    pass
  
  def fit(self, X: pd.DataFrame|np.ndarray, y: Optional[pd.Series|np.ndarray]=None):
    pass
  
  def predict(self, X: pd.DataFrame|np.ndarray):
    pass
  
  def summary(self):
    if self.fitted_model is None:
      raise ValueError('Model has not been fitted yet')
    
  