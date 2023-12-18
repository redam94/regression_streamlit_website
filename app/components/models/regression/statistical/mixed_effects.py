from .ols import OLS
import streamlit as st
from linearmodels import PanelOLS, RandomEffects
from ....utils.pipelines import transform_data_element, transform_data
from ....utils.constants import TRANSFORM_DETAIL_COLUMNS, COLUMN_SETTINGS
from ....callbacks.data_frames import transform_df_callback

class MixedEffects(OLS):
  description = """
  ## Mixed Effects Model
  """
  def __init__(self, name='ME', data=None):
    super().__init__(name, data)
    self.model = RandomEffects
  
  def fit(self):
    """
    Fit model to data
    """
    if self.X_train is None or self.y_train is None:
      st.stop()
    self.fitted_model = self.model(self.y_train, self.X_train).fit()

class FixedEffects(OLS):
  description = """
  ## Fixed Effects Model
  """
  def __init__(self, name='FE', data=None):
    super().__init__(name, data)
    self.model = PanelOLS
    
  def set_params(self):
    
    columns = st.columns([.2, .8])
    with columns[0]:
      dep_var = st.selectbox('Dependent Variable', self.data.columns, index=list(self.data.columns).index(self.dep_var) if self.dep_var is not None else 0)
      self.dep_var = dep_var
    with columns[1]:
      defaults = [col for col in self.ind_var if col != self.dep_var] if self.ind_var is not None else None
      #defaults = [col for col in defaults if col in self.data.columns and col != self.dep_var]
      ind_var = st.multiselect('Independent Variables', [col for col in self.data.columns if col not in [self.dep_var]], default=defaults)
      self.ind_var = ind_var
    
    columns2 = st.columns([.5, .5])
    
    with columns2[0]:
      self.effect_1 = st.selectbox('First Effect', [None]+[col for col in self.data.columns if col not in [self.dep_var] + self.ind_var], index=0)
    
    with columns2[1]:
      self.effect_2 = st.selectbox('Second Effect', [None]+[col for col in self.data.columns if col not in [self.dep_var, self.effect_1] + self.ind_var], index=0)
      self.intercept = st.checkbox('Intercept', value=True)
    
    if self.dep_var is None or self.ind_var is None:
      st.stop()
    self.regression_data = self.data[[self.dep_var] + self.ind_var].copy()

    transform_df = transform_data_element(self.dep_var, self.ind_var, self.data)

    self.transform_df = transform_df.copy()

    self.regression_data = transform_data(self.regression_data, self.transform_df)

    self.X_train = self.regression_data.drop(columns=[self.dep_var])
    self.y_train = self.regression_data[self.dep_var]

    
    
    
  