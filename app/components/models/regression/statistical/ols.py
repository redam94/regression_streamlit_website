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
  
  model_help = """
  ## OLS Model
  ### This model uses statsmodels.api.OLS to fit a linear regression model to the data.
  Instructions: 
  1. Unzip the data file
  2. Pickle load the model you made need to install the following packages:
  - statsmodels
  - pandas
  - numpy
  3. load the regression data csv file
  """
  
  def __init__(self, name: str="OLS", data=None):
    super().__init__(name, data)

    self.model = sm.OLS
    self.fitted_model = None
    self.X_train = None
    self.y_train = None
    self.intercept = False
    self.dep_var = None
    self.ind_var = None
    self.dev_var_index = 0
    self.ind_default = None
    st.session_state[str(self)+"_ind"] = []
    st.session_state[str(self)+"_dep"] = None
    
    
  def fit(self):
    """
    Fit model to data
    """
    if self.X_train is None or self.y_train is None:
      st.stop()
    self.fitted_model = self.model(self.y_train, self.X_train).fit('qr')
    
  def dep_var_callback(self):
    self.dev_var_index = 0 if st.session_state[str(self)+"_dep"] is None else list(self.data.columns).index(st.session_state[str(self)+"_dep"])
  
  def ind_var_callback(self):
    self.ind_default = [] if st.session_state[str(self)+ "_ind"] is None else st.session_state[str(self)+ "_ind"]
  
  def set_params(self):
    columns = st.columns([.2, .8])
    with columns[0]:
      self.dep_var = st.selectbox('Dependent Variable', self.data.columns, index=self.dev_var_index, on_change=self.dep_var_callback, key=str(self)+"_dep")
      
    with columns[1]:
      
      #defaults = [col for col in defaults if col in self.data.columns and col != self.dep_var]
      self.ind_var = st.multiselect('Independent Variables', [col for col in self.data.columns if col not in [self.dep_var]], default=self.ind_default, on_change=self.ind_var_callback, key=str(self)+"_ind")
      
      self.intercept = st.checkbox('Intercept', value=True)
    if self.dep_var is None or self.ind_var is None:
      st.stop()
    self.regression_data = self.data[[self.dep_var] + self.ind_var].copy()

    transform_df = transform_data_element(self.dep_var, self.ind_var, self.data)

    self.transform_df = transform_df.copy()

    self.regression_data = transform_data(self.regression_data, self.transform_df)

    self.X_train = self.regression_data.drop(columns=[self.dep_var])
    self.y_train = self.regression_data[self.dep_var]

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
  
  def plot_avm(self,period = None, group: Optional[pd.Series|np.ndarray|pd.DataFrame]=None, selected_group: Optional[str]=None):
    """
    Plot actual vs model
    """
    model_output = self.predict()
    actual = self.y_train
    residual = self.fitted_model.resid
    
    if period is None:
      period = range(len(model_output))
    
      
    fig, ax = plt.subplots(2, figsize=(16, 18))
    if group is None:
      ax[0].plot(period, model_output, color='blue', label='Model')
      ax[0].plot(period, actual, color='k', label='Actual')
      ax[1].plot(period, residual, 'o', color='red', label='Residual')
      
    else:
      ax[0].plot(period[group==selected_group], model_output[group==selected_group], color='blue', label='Model')
      ax[0].plot(period[group==selected_group], actual[group==selected_group], color='k', label='Actual')
      ax[1].plot(period[group==selected_group], residual[group==selected_group], 'o', color='red', label='Residual')
    ax[0].legend()
    ax[1].legend()
    ax[0].set_title('Actual vs Model')
    ax[1].set_title('Residual')
    ax[0].set_xlabel('Period')
    ax[1].set_xlabel('Period')
    ax[0].set_ylabel(self.dep_var)
    ax[1].set_ylabel('Residual')
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

  def save_model(self, name: str):
    """
    Save model to file
    """
    import zipfile
    import io
    import pickle
    
    temp_file = io.BytesIO()
    with zipfile.ZipFile(
        temp_file, "w", zipfile.ZIP_DEFLATED
    ) as temp_file_opened:
            # add csv files each library
            temp_file_opened.writestr(f"model.pkl", pickle.dumps(self.fitted_model))
            temp_file_opened.writestr(f"regression_data.csv", self.regression_data.to_csv(index=False))
            temp_file_opened.writestr(f"transform_df.csv", self.transform_df.to_csv(index=True))
            temp_file_opened.writestr(f"model_summary.txt", self.fitted_model.summary().as_text())
            temp_file_opened.writestr(f"README.md", self.model_help)
            
    temp_file.seek(0)
    
    st.download_button(
        label="Download Model",
        data=temp_file,
        file_name=f"{name}.zip",
        mime="application/zip",
    )
  
            
