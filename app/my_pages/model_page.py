import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from uuid import uuid4
from components.models import IMPLEMENTED_MODELS
from components.datamodels import SaveModel
from streamlit import session_state as ss

def save_model(fitted_model, x, y, transformation_details):
  if 'fitted_model_list' not in st.session_state:
    #st.session_state['fitted_model'] = [{'model': fitted_model, 
    #'time': pd.Timestamp.now(), 
    #'id': uuid4(),
    #'ind': x,
    #'dep': y,
    #'transformation_details': transformation_details
    #}]
    ss['fitted_model_list'] = [
      SaveModel(model=fitted_model, 
                time=pd.Timestamp.now(), 
                id=uuid4())
    ]
    return
  ss['fitted_model_list'].append(
    SaveModel(model=fitted_model,
                time=pd.Timestamp.now(), 
                id=uuid4())
  )

def model_type_callback():
  ss['model_type'] = st.session_state.model_type
  if 'tabular_data' not in ss.keys() or ss.tabular_data is None:
    ss['tabular_data'] = None
  ss['model'] = IMPLEMENTED_MODELS[ss.model_type](name='', data=ss.tabular_data)
def change_model_type_callback():
  ss['model_type'] = 'None'
  ss['model'] = None
  
def fit_model_callback():
  ss.model.fit()
  save_model(ss.model, ss.model.X_train, ss.model.y_train, ss.model.transform_df)
  ss.model = ss.model.deepcopy()

MODEL_OPTIONS = list(IMPLEMENTED_MODELS.keys())
def main():
  
  if 'model' not in ss.keys():
    ss['model'] = None
  if 'model_type' not in ss.keys():
    ss['model_type'] = MODEL_OPTIONS[0]
  
  st.title('Model Page')
  
  default_index = MODEL_OPTIONS.index(ss.model_type) if ss.model_type in MODEL_OPTIONS else 0
  if ss.model_type is 'None':
    model_type = st.selectbox('Select a model type', MODEL_OPTIONS, index=default_index, key='model_type', on_change=model_type_callback)
  else:
    st.button('Change Model', on_click=change_model_type_callback)
  
  if ss.model is None:
    st.stop()

  
  
  st.markdown(ss.model.description)
  st.title(ss.model.name)

 
  if ss.model.data is None:
    st.stop()
  
  #ss.model.show_sample(10)
  #ss.model.data_info()
  #ss.model.plot_raw()
  ss.model.set_params()
  ss.model.plot_transforms()

  st.button('Fit Model', on_click=fit_model_callback)
    
  if ss.model.fitted_model is None:
    st.stop()
  
  st.write(ss.model.summary())


  


if __name__ == '__main__':
  main()
