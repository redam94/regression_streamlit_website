from ....models.basemodel import BaseModel
import statsmodels.api as sm

class MixedEffects(BaseModel):
  def __init__(self, name: str):
    super().__init__(name)
    self.model = sm.MixedLM
    self.fitted_model = None
  
  def fit(self, X, y, groups, *args, **kwargs):
    self.model = self.model(y, X, groups)
    self.fitted_model = self.model.fit(*args, **kwargs)
    return self
  
  def predict(self, X):
    return self.fitted_model.predict(exog=X)
  
  def summary(self):
    return self.fitted_model.summary()