import pandas as pd
import numpy as np

import streamlit as st

def weibull(x, **kwargs) -> np.ndarray:
  alpha = kwargs.get('alpha', 1.0)
  beta = kwargs.get('beta', 1.0)
  index_to = kwargs.get('index_to', 100.0)
  x_ = x.copy()
  x_ = np.maximum(x_, 0.0)
  return 1 - np.exp(-(x_/index_to/alpha*100)**beta)

def log(x, **kwargs) -> np.ndarray:
  return np.log(x)

def logit(x, **kwargs) -> np.ndarray:
  return np.log(x/(1-x))

def logp1(x, **kwargs) -> np.ndarray:
  return np.log(x+1)

def expit(x, **kwargs) -> np.ndarray:
  return 1/(1+np.exp(-x))

def linear(x, **kwargs) -> np.ndarray:
  return x

def one_hot_encode(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
  return pd.get_dummies(data, drop_first=True, prefix='OHE_dummy')

