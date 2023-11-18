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

data = pd.read_csv('./data/fake_mff.csv')[["Geography", 'Period', 'VariableValue', 'VariableName']].pivot(index=['Geography', 'Period'], columns='VariableName', values='VariableValue').reset_index()



def save_model(fitted_model, x, y, transformation_details):
  if 'fitted_model' not in st.session_state:
    st.session_state['fitted_model'] = [{'model': fitted_model, 
    'time': pd.Timestamp.now(), 
    'id': uuid4(),
    'ind': x,
    'dep': y,
    'transformation_details': transformation_details
    }]
    return
  st.session_state['fitted_model'] = (st.session_state['fitted_model'] +
   [{'model': fitted_model, 
    'time': pd.Timestamp.now(), 
    'id': uuid4(),
    'ind': x,
    'dep': y,
    'transformation_details': transformation_details
    }])

def run_regression(model:sm.OLS, cov_type:str='nonrobust'):
    # Make predictions using your regression model
    fitted_model = model.fit('qr',cov_type=cov_type)
    return fitted_model


def run_regression_app():
  # Define the user interface elements
  st.title('Regression App')
  st.write('Enter the regression parameters:')
  
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
  if intercept:
    X = sm.add_constant(X)
    
  if d:
    st.write('Regression Results:')
    
  
    fitted_model = run_regression(sm.OLS(Y, X))
    #st.write(fitted_model.summary())
    save_model(fitted_model, X, Y, transformation_details)
    #Get the predicted values of y from the fitted model
    
      
  if 'fitted_model' in st.session_state:
    for i, model in enumerate(st.session_state.fitted_model[::-1]):
      with st.expander(str(model['id'])[:8] + f" R2: {model['model'].rsquared:.3f}" + f" Time: {model['time']}", expanded=(i==0 and d)):
        st.write(model['time'])
        st.write(model['model'].summary())
        #with st.expander("AVM Plot"):
        X = model['ind']
        Y = model['dep']
        y_cap = model['model'].predict(X)
        if group == 'None':
          st.pyplot(plot_avm(range(len(Y)) if time=='None' else pd.to_datetime(data[time]), Y, y_cap, model['model'].resid))
        #st.pyplot(plot_avm(range(len(Y)) if time=='None' else time, Y, y_cap, fitted_model.resid))
    #with st.expander("Residual Plot"):
        y_cap = model['model'].predict(X)
        st.pyplot(plot_resid(model['model'], y_cap))
          
        

    
# Run the Streamlit app
if __name__ == '__main__':
  run_regression_app()
