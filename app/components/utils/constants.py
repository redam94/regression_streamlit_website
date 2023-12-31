from .transforms import weibull, log, logit, logp1, expit, linear, one_hot_encode
import streamlit as st

TRANSFORMS = {
  "Linear": linear,
  "Weibull": weibull,
  "Log": log,
  "Logp1": logp1,
  "Logit":logit,
  "Expit":expit,
  "One Hot Encode": one_hot_encode}

TRANSFORM_DETAIL_COLUMNS = [
  'transformation',
  'alpha',
  'beta',
  'index_to',
  'lag',
  'decay'
]

TRANSFORM_DETAIL_COLUMNS_DEFAULTS = [
  'Linear',
  0.0,
  0.0,
  100.0,
  0,
  0.0
]

OPTIONS = TRANSFORMS.keys()
COLUMN_SETTINGS = {
  'transformation': st.column_config.SelectboxColumn("transformation",
    default='Linear', 
    options=TRANSFORMS.keys(),
    required=True
    ),
  'alpha': st.column_config.NumberColumn(default=0.0),
  'beta': st.column_config.NumberColumn(default=0.0),
  'index_to': st.column_config.NumberColumn(default=100.0),
  'lag': st.column_config.NumberColumn(default=0),
  'decay': st.column_config.NumberColumn(default=0.0, min_value=0.0, max_value=1.0)
  }

ORGINIZATIONS = ['None', 'Org', 'Org2']