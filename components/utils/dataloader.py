"""
Contains data classes for app that will contain main data for analysis
Currently allowed data types are TabularData
"""

import streamlit as st
import pandas as pd
import numpy as np
import io


def load_tabular_data():
  file_data = st.file_uploader('Upload Data', type=['csv', 'xlsx'])
  if file_data is not None:
    data = TabularData(file_data)
    st.write(data.name)
    st.table(data.data.head())
    return data

class TabularData:

    def __init__(self, file: io.BytesIO|None):
        self._file = file
        self._file_type = self._check_file_type()
        self._file_structure = self._infer_file_structure()
        self._data = None
        self._name = None
        self.update_data()
        self.update_name()

    def _check_file_type(self):
        return self.file.type

    def _infer_file_structure(self):
        if "mff" in self.file.name:
            return "mff"
        else:
            return "wide"

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
        self._file_structure = self._infer_file_structure()
        self.update_data()
        self.update_name()

    @property
    def file_type(self):
        return self._file_type

    def set_file_type(self, file_type):
        raise AttributeError("Cannot set file type")

    @property
    def file_structure(self):
        return self._file_structure

    def set_file_structure(self, file_structure):
        raise AttributeError("Cannot set file structure")

    def load_data(self):

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
        return data

    def make_analytic(self, data):
        if self.file_structure == 'mff':
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

        elif self.file_structure == 'wide':
            analytic_data = data
        else:
            return None
        
        return analytic_data

    @property
    def data(self):
        return self._data
    
    def set_data(self, data):
        raise ValueError("Cannot set data")

    def update_data(self):

        if self.file is None:
            return None
        
        data = self.load_data()

        analytic_data = self.make_analytic(data)

        self._data = analytic_data

