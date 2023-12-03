import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from uuid import uuid4
from components.models import IMPLEMENTED_MODELS

def main():
  st.title('Model Page')
  st.write("Select a model type")
  model_type = st.selectbox('Model Type', ['None'] + list(IMPLEMENTED_MODELS.keys()))

  if model_type == 'None':
    st.stop()
  
  model = IMPLEMENTED_MODELS[model_type](name=model_type)
  st.write(model_type)
  
  model.upload_data()
  
  if model.data is None:
    st.stop()
  
  model.set_params()


if __name__ == '__main__':
  main()
