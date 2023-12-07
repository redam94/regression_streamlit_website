import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from uuid import uuid4

from components.utils.pipelines import transform_data
from components.utils.constants import TRANSFORM_DETAIL_COLUMNS, COLUMN_SETTINGS
from components.utils.plotting import plot_resid, plot_corr, plot_transfromed_data, plot_avm
from components.model_params import select_variables

from components.datamodels.model import SaveModel
from components.models.regression.statistical.ols import OLS
from components.models.regression.statistical.mixed_effects import MixedEffects

data = pd.read_csv('./data/fake_mff.csv')[["Geography", 'Period', 'VariableValue', 'VariableName']].pivot(index=['Geography', 'Period'], columns='VariableName', values='VariableValue').reset_index()


  
  

def save_model(fitted_model, x, y, transformation_details):
  if 'fitted_model' not in st.session_state:
    #st.session_state['fitted_model'] = [{'model': fitted_model, 
    #'time': pd.Timestamp.now(), 
    #'id': uuid4(),
    #'ind': x,
    #'dep': y,
    #'transformation_details': transformation_details
    #}]
    st.session_state['fitted_model'] = [
      SaveModel(model=fitted_model, 
                ind=x, 
                dep=y, 
                transformation_details=transformation_details, 
                time=pd.Timestamp.now(), 
                id=uuid4())
    ]
    return
  #st.session_state['fitted_model'] = (st.session_state['fitted_model'] +
  # [{'model': fitted_model, 
  #  'time': pd.Timestamp.now(), 
  #  'id': uuid4(),
  #  'ind': x,
  #  'dep': y,
  #  'transformation_details': transformation_details
  #  }])
  st.session_state['fitted_model'].append(
    SaveModel(model=fitted_model, 
                ind=x, 
                dep=y, 
                transformation_details=transformation_details, 
                time=pd.Timestamp.now(), 
                id=uuid4())
  )

def run_regression(X, y, groups, model):
    # Make predictions using your regression model
    fitted_model = model.fit(X, y, groups)
    return fitted_model


def add_trend(data, time):
  if time is None:
    return data
  
  start = data[time].min()
  trend = (data[time]-start)/np.timedelta64(1, 'D')
  trend = trend/trend.max()

  data['trend'] = trend
  

def run_regression_app():
  # Define the user interface elements
  st.title('Regression App')
  st.write('Choose Model')
  
  
  
  with st.sidebar:
    y, x, transformation_details, time, group = select_variables(data)
    intercept = st.checkbox('intercept')
    d = st.button('Run Regression') 
    st.write('Click to run regression')

  regression_data = data[[y]+x] if not x is None else data[[y]]
  transformed_data = data.copy()
  if x:
    plot_corr(regression_data)
    transformed_data = transform_data(regression_data, transformation_details)
    plot_transfromed_data(transformed_data, data, x, y)
    
  with st.expander("Data Preview", expanded=False):
    st.table(transformed_data[x].head())
  
  X = transformed_data[x]
  Y = transformed_data[y]
  group_data = None if group=='None' else data[group]
  time_data = None if time=='None' else data[time]
  
  if intercept:
    X = sm.add_constant(X)
  if d:
    st.write('Regression Results:')
    
    model =OLS('OLS')
  
    fitted_model = model.fit(X, Y, group=group_data, time=time_data)
    #st.write(fitted_model.summary())
    save_model(fitted_model, X, Y, transformation_details)
    #Get the predicted values of y from the fitted model
    
      
  if 'fitted_model' in st.session_state:
    for i, model in enumerate(st.session_state.fitted_model[::-1]):
      score_name, score = model.model.model_score()
      with st.expander(str(model.id)[:8] + f" {score_name}: {score:.3f}" + f" Time: {model.time}"):
        st.write(model.time)
        st.write(model.model.summary())
        #with st.expander("AVM Plot"):
        X = model.ind
        Y = model.dep
        
        if model.model.group is None:
          st.pyplot(model.model.plot_avm())
        else:
          groups = model.model.group.unique()
          selected_group = st.selectbox('Group', groups, key=model.id)
          y_cap = model.model.predict(X)
          st.pyplot(plot_avm(range(len(Y[data[group]==selected_group])) if time=='None' else pd.to_datetime(data[data[group]==selected_group][time]), Y[data[group]==selected_group], y_cap[data[group]==selected_group], model.model.fitted_model.resid[data[group]==selected_group]))
        #st.pyplot(plot_avm(range(len(Y)) if time=='None' else time, Y, y_cap, fitted_model.resid))
    #with st.expander("Residual Plot"):
        y_cap = model.model.predict(X)
        st.pyplot(plot_resid(model.model.fitted_model, y_cap))
          
        

    
# Run the Streamlit app
if __name__ == '__main__':
  run_regression_app()
