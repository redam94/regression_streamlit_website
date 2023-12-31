import numpy as np
import pandas as pd
from ....models.basemodel import BaseModel
import statsmodels.api as sm
from typing import Optional
import matplotlib.pyplot as plt
import streamlit as st
from ....utils.pipelines import transform_data_element, transform_data
from ....utils.constants import TRANSFORM_DETAIL_COLUMNS, COLUMN_SETTINGS
from ....callbacks.data_frames import transform_df_callback
from ....utils.plotting import scatter_data

class OLS(BaseModel):
  description = """
  ## This is a standard OLS regression model makes several assumptions:
  - Linear relationship between the dependent and independent variables
  - No (sever) multicollinearity (looks like smaller sample size)
  - No autocorrelation
  - Homoscedasticity 
  - The independent variables are uncorrelated with the error term (may not be true for time series data or panel data see [here](https://timeseriesreasoning.com/contents/pooled-ols-regression-models-for-panel-data-sets/))
  - Normality of the error term
  """
  def __init__(self, name: str="OLS", data=None):
    super().__init__(name, data)

    self.model = sm.OLS
    self.fitted_model = None
    self.X_train = None
    self.y_train = None
    self.intercept = False
    
  def fit(self):
    """
    Fit model to data
    """
    if self.X_train is None or self.y_train is None:
      st.stop()
    self.fitted_model = self.model(self.y_train, self.X_train).fit('qr')
  
  def set_params(self):
    columns = st.columns([.2, .8])
    with columns[0]:
      dep_var = st.selectbox('Dependent Variable', self.data.columns)
    with columns[1]:
      ind_var = st.multiselect('Independent Variables', [col for col in self.data.columns if col not in [dep_var]])
      self.intercept = st.checkbox('Intercept', value=True)
    if dep_var is None or ind_var is None:
      st.stop()
    self.regression_data = self.data[[dep_var] + ind_var].copy()

    transform_df = transform_data_element(dep_var, ind_var, self.data)

    self.transform_df = transform_df.copy()

    self.regression_data = transform_data(self.regression_data, self.transform_df)

    self.X_train = self.regression_data.drop(columns=[dep_var])
    self.y_train = self.regression_data[dep_var]

    if self.intercept:
      self.X_train = sm.add_constant(self.X_train)

  def plot_transforms(self):

    transformed_data = self.regression_data.copy()
    transformed_data.rename(columns={col: f"{self.transform_df.loc[col]['transformation']}({col})" for col in transformed_data.columns if col in self.transform_df.index}, inplace=True)
    data = self.data.copy().join(transformed_data)
    scatter_data(data, name='Transformed Data')
  
  def plot_raw(self):
    scatter_data(self.data, name='Raw Data')

  
  def predict(self, X: Optional[pd.DataFrame | np.ndarray] = None):
    """
    Predict using fitted model
    """
    
    if self.fitted_model is None:
      raise ValueError('Model has not been fitted yet')
    
    if X is None:
      return self.fitted_model.predict(self.X_train)
    
    return self.fitted_model.predict(X)
  
  def summary(self):
    """
    Return fitted model summary
    """
    
    if self.fitted_model is None:
      raise ValueError('Model has not been fitted yet')
    
    return self.fitted_model.summary()
  
  def plot_avm(self, group: Optional[pd.Series|np.ndarray|pd.DataFrame]=None):
    """
    Plot actual vs model
    """
    model_output = self.predict()
    actual = self.y_train
    residual = self.fitted_model.resid
    
    if self.time is None:
      period = range(len(model_output))
    else:
      period = self.time
      
    fig, ax = plt.subplots(1, figsize=(16, 9))
    if self.group is None:
      ax.plot(period, model_output, color='blue', label='Model')
      ax.plot(period, actual, color='k', label='Actual')
      ax.plot(period, residual, 'o', color='red', label='Residual')
      
    else:
      ax.plot(period[self.group==group], model_output[self.group==group], color='blue', label='Model')
      ax.plot(period[self.group==group], actual[self.group==group], color='k', label='Actual')
      ax.plot(period[self.group==group], residual[self.group==group], 'o', color='red', label='Residual')
    
    return fig
  
  def plot_residual(self, period: Optional[list[float]|np.ndarray|pd.DataFrame|pd.Series] = None):
    """
    Plot residuals
    """
    residual = self.fitted_model.resid
    
    if period is None:
      period = range(len(residual))
    
    fig, ax = plt.subplots(1, figsize=(16, 9))

    ax.plot(period, residual, color='red', label='Residual')
    
    return fig  
  
  def model_score(self) -> tuple[str, float]:
    """
    Return model score
    """
    return ("R2", self.fitted_model.rsquared)
  
  def deepcopy(self):
    new_copy = OLS(self.name)
    for key, value in self.__dict__.items():
      new_copy.__dict__[key] = value
    return new_copy
