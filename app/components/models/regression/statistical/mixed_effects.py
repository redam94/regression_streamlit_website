from ....models.basemodel import BaseModel
import streamlit as st
import statsmodels.api as sm
from ....utils.pipelines import transform_data_element, transform_data
from ....utils.constants import TRANSFORM_DETAIL_COLUMNS, COLUMN_SETTINGS
from ....callbacks.data_frames import transform_df_callback

class MixedEffects(BaseModel):
  def __init__(self, name: str):
    super().__init__(name)
    self.model = sm.MixedLM
    self.fitted_model = None
  
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

    self.X_train = self.regression_data[ind_var]
    self.y_train = self.regression_data[dep_var]

    if self.intercept:
      self.X_train = sm.add_constant(self.X_train)

  def fit(self, X, y, groups, *args, **kwargs):
    self.model = self.model(y, X, groups)
    self.fitted_model = self.model.fit(*args, **kwargs)
    return self
  
  def predict(self, X):
    return self.fitted_model.predict(exog=X)
  
  def summary(self):
    return self.fitted_model.summary()