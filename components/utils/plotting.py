import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_resid(fitted_model, y_cap):
    #Plot the model's residuals against the predicted values of y
    fig, ax = plt.subplots(figsize=(5, 5))
    
    ax.set_xlabel('Predicted value of Y')
 
    ax.set_ylabel('Residual error')
 
    ax.scatter(y_cap, fitted_model.resid)
    return fig
  
def plot_avm(index, actual, predicted, residuals):
  fig, ax = plt.subplots(figsize=(10, 5))
  ax.plot(index, actual, color='k', label='Actual')
  ax.plot(index, predicted, ls='--', color='b', label='Predicted')
  ax.plot(index, residuals, ls='--', color='r', label='Residuals')
  ax.legend()
  ax.set_xlabel('Actual')
  ax.set_ylabel('Predicted')
  return fig
  
@st.cache_data
def plot_corr(data):
  fig, ax = plt.subplots(figsize=(10, 10))
  ax.imshow(data.corr(), cmap='RdYlGn', vmin=-1, vmax=1)
  ax.set_xticks(np.arange(len(data.columns)), data.columns, minor=False)
  ax.set_yticks(np.arange(len(data.columns)), data.columns, minor=False)
  with st.expander('Correlation Matrix'):
    st.pyplot(fig)


def plot_transfromed_data(transformed_data: pd.DataFrame, data: pd.DataFrame, x: list[str], y: str):
  
  fig, ax = plt.subplots(len(x)+1, figsize=(10, 5*len(x)))
  
  for i, col in enumerate(x+[y]):
    
    ax[i].scatter(data[col], transformed_data[col])
    ax[i].set_xlabel(col)
    ax[i].set_ylabel(col + ' transformed')
    
  with st.expander('Transformations'):
    st.pyplot(fig)
  
  