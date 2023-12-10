import streamlit as st
import pandas as pd
import numpy as np
import io
from ...utils.plotting import scatter_data
class TabularDataBase:
  
  def __init__(self, file: io.BytesIO|None):
    self._file = file
    self._file_type = self._check_file_type()
    self._data = None
    self._name = None
    self.update_data()
    self.update_name()
  
  def show_sample(self, rows: int):
    if self._data is None:
      return
    sample = self._data.sample(rows)
      
    with st.expander("Data Preview", expanded=False):
      st.table(sample)
  
  def data_info(self):
    if self._data is None:
      return
    with st.expander("Data Info", expanded=False):
      st.write(self._data.describe())
  
  def __getattr__(self, name):
    if self.data is None:
      st.stop()
    
    atter = getattr(self.data, name)
    
    def method(*args, **kwargs):
      return atter(*args, **kwargs)
    
    if callable(atter):
        return method
    else:
        return atter
    
  def _check_file_type(self):
    try:
      return self.file.type
    except AttributeError:
      return 'text/' + self.file.name.split('.')[-1]
    
  def plot_raw(self):
    scatter_data(self.data, name='Raw Data')
    
  @property
  def name(self):
    return self._name

  @property
  def file(self):
      return self._file

  def update_name(self):
    if self.file is None:
      return
    self._name = self.file.name

  def set_file(self, file: io.BytesIO|None):
    self._file = file
    self._file_type = self._check_file_type()
    self.update_data()
    self.update_name()
      
  @property
  def file_type(self):
    return self._file_type

  def set_file_type(self, file_type):
    raise AttributeError("Cannot set file type")
  
  def load_data(self):
    try:
      if self.file is None:
        return None
      if self.file_type == 'text/xlsx':
        data = pd.read_excel(self.file)
      elif self.file_type == 'text/csv':
        data = pd.read_csv(self.file)
      elif self.file_type == 'text/txt':
        data = pd.read_csv(self.file, sep='\t')
      else:
        raise ValueError("File type not recognized")
    except Exception as e:
      return None
      
    return data
  
  
  @property
  def data(self):
    return self._data
    
  def set_data(self, data):
    raise ValueError("Cannot set data")

  def update_data(self):

    if self.file is None:
      return None
    
    self._data = self.load_data()
        
  def __getitem__(self, key):
    return self.data[key]

  def __setitem__(self, key, value):
    self.data[key] = value
    
  

class MFF(TabularDataBase):

    def __init__(self, file: io.BytesIO|None):
        super().__init__(file)

    def make_analytic(self, data):
        if data is not None:
            analytic_data = data.pivot_table(
                index=[
                    'Geography', 'Period', 
                    'Product', 'Campaign', 
                    'Outlet'
                    ],
                columns='VariableName',
                values='VariableValue'
                ).reset_index()
            analytic_data['Period'] = pd.to_datetime(analytic_data['Period'])
        else:
            return None
        return analytic_data

    def update_data(self):
        if self.file is None:
            return None
        data = self.load_data()
        analytic_data = self.make_analytic(data)
        self._data = analytic_data
        
class Wide(TabularDataBase):
  
  def __init__(self, file: io.BytesIO|None):
    super().__init__(file)
    
  