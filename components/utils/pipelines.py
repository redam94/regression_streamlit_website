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
    transformed_data[col] = TRANSFORMS.get(row['transformation'], linear)(data[col], **row)
    
  return transformed_data

def transform_data_element(dep_var:str|list[str], ind_var:list[str], data:pd.DataFrame|TabularData) -> pd.DataFrame:
  data_transforms = pd.DataFrame(
      columns=TRANSFORM_DETAIL_COLUMNS, 
      index=list(set([dep_var]+ind_var)) if not ind_var is None else [dep_var],
    )
  if 'old_df' not in st.session_state:
    st.session_state['old_df'] = pd.DataFrame(
      columns=TRANSFORM_DETAIL_COLUMNS,
      index=data.columns,
      data=[['Linear', 0.0, 0.0, 100.0, 0, 0.0] for _ in range(len(data.columns))])
  
  for row in data_transforms.index:
    if row in st.session_state.old_df.index:
      data_transforms.loc[row] = st.session_state.old_df.loc[row]
    else:
      data_transforms.loc[row] = ['Linear', 0.0, 0.0, 100.0, 0, 0.0]
  
        
  data_transforms = st.data_editor(data_transforms, column_config=COLUMN_SETTINGS)
  transform_df_callback(data_transforms)
 
  transformed_data = transform_data(data, data_transforms)
  return transformed_data