from .constants import TRANSFORMS
import streamlit as st
from .transforms import linear


def transform_data(data, transform_df):
  transformed_data = data.copy()
  for col in data.columns:
    row = transform_df.loc[col].to_dict()
    transformed_data[col] = TRANSFORMS.get(row['transformation'], linear)(data[col], **row)
    
  return transformed_data