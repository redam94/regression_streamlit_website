from .constants import TRANSFORMS, TRANSFORM_DETAIL_COLUMNS, COLUMN_SETTINGS
import streamlit as st
from .transforms import linear
from .dataloader import TabularData
from ..callbacks.data_frames import transform_df_callback
import pandas as pd


@st.cache_data
def transform_data(data, transform_df):
  transformed_data = data.copy()
  for col in data.columns:
    
    row = transform_df.loc[col].to_dict()
    transformed_col = TRANSFORMS.get(row['transformation'], linear)(data[col], **row)
    if transformed_col.shape == data[col].shape:
      transformed_data[col] = transformed_col
    else:
      transformed_data[transformed_col.columns] = transformed_col.astype(float)
      transformed_data.drop(columns=[col], inplace=True)
    
  return transformed_data


def transform_data_element(dep_var:str|list[str], ind_var:list[str], data:pd.DataFrame|TabularData) -> pd.DataFrame:
  data_transforms = pd.DataFrame(
      columns=TRANSFORM_DETAIL_COLUMNS, 
      index=list(set([dep_var]+ind_var)) if not ind_var is None else [dep_var],
    )
  if not 'old_df' in st.session_state:
    st.session_state['old_df'] = pd.DataFrame(
      columns=TRANSFORM_DETAIL_COLUMNS,
      index=data.columns,
      data=[['Linear', 0.0, 0.0, 100.0, 0, 0.0] for _ in range(len(data.columns))])
  
  for row in data_transforms.index:
    if row in st.session_state.old_df.index:
      data_transforms.loc[row] = st.session_state.old_df.loc[row]
    else:
      data_transforms.loc[row] = ['Linear', 0.0, 0.0, 100.0, 0, 0.0]
  
  data_transforms = st.data_editor(data_transforms, column_config=COLUMN_SETTINGS, key='data_transforms')
  transform_df_callback(data_transforms)

  return data_transforms