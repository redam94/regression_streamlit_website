import numpy as np
import pandas as pd
from ....models.basemodel import BaseModel
import statsmodels.api as sm

class OLS(BaseModel):
  def __init__(self, name: str):
    super().__init__(name)
    self.model = sm.OLS
    self.fitted_model = None
  
  def fit(self, X, y, *args, **kwargs):
    self.model = self.model(y, X)
    self.fitted_model = self.model.fit(*args, **kwargs)
    return self
  
  def predict(self, X: pd.DataFrame | np.ndarray):
    return self.fitted_model.predict(X)
  
  def summary(self):
    if self.fitted_model is None:
      raise ValueError('Model has not been fitted yet')
    return self.fitted_model.summary()