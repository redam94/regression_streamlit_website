import streamlit as st
from st_pages import show_pages_from_config, add_page_title
from components.utils.connections import conn
from st_files_connection import FilesConnection
from pydantic import BaseModel

class ProjectForm:
  orginazation: str


st.session_state['connection']: FilesConnection = conn

def list_of_dirs(directory_dict: dict[str, str]) -> list[str]:
  dirs = [folder['name'].split('/')[-1] for folder in directory_dict if folder['type'] == 'directory']
  return dirs
  
def get_orgs():
  org_list = conn.fs.listdir("regressions_app_filestore")
  orgs = list_of_dirs(org_list)
  return orgs

def go_back():
  st.session_state.show_project_creation_form = False

def project_creation_form(org: str, client: str):
  
  if org is None or client is None:
    st.session_state.show_project_creation_form = False
    
  with st.form('New Project'):
    cols = st.columns(2)
    with cols[0]:
      st.subheader(f'Organization:\n{org}')
    
    with cols[1]:
      st.subheader(f"Client:\n{client}")
    
    st.text_input("Project Name", key="project_name")
    new_cols = st.columns(2)
    with new_cols[0]:
      st.form_submit_button("Back", on_click=go_back)
    with new_cols[1]:
      st.form_submit_button("Create Project", on_click=write_project, args=(org, client, st.session_state.project_name))

def write_project(org, client, name):
  if name == '':
    st.session_state.show_project_creation_form = False
    return
  conn.fs.mkdir(f'regressions_app_filestore/{org}/{client}/{name}')
  st.session_state.show_project_creation_form = False

def create_project():
  org = st.session_state['org']
  client = st.session_state['client']
  if org is None or client is None:
    st.session_state.project_warning = True
    st.session_state.show_project_creation_form = False
  else:
    st.session_state.project_warning = False
    st.session_state.show_project_creation_form = True

def get_clients():

  selected_org = st.session_state['org']

  if selected_org is None:
    return []

  else:
    client_dirs = conn.fs.listdir(f'regressions_app_filestore/{selected_org}')
    client_list = list_of_dirs(client_dirs)

  return client_list
    
def initialize_session_state():
  if 'client' not in st.session_state:
    st.session_state['client'] = None
  if 'org' not in st.session_state:
    st.session_state['org'] = None
  if 'project_warning' not in st.session_state:
    st.session_state['project_warning'] = False
  if 'show_project_creation_form' not in st.session_state:
    st.session_state['show_project_creation_form'] = False
  
def save_org(selected_org):
  st.session_state.org = selected_org

def main_page():
  
  #st.write(folder_list)
  
  orgs = get_orgs()
  
  st.title("Welcome!")
  cols = st.columns(2)
  with cols[0]:
    st.selectbox('Organization', orgs, index=None, key='org')
    

    
  with cols[1]:
    st.selectbox('Client', get_clients(), index=None, key='client')

  st.selectbox('Project', [], index=None, key='project')
  
  st.button("Create New Project", on_click=create_project)
  if st.session_state.project_warning:
    st.warning("Must select Orginazation and client first")
  
  





if __name__ == '__main__':
  show_pages_from_config()
  initialize_session_state()
  if not st.session_state.show_project_creation_form or st.session_state.client is None or st.session_state.org is None:
    main_page()
  else:
    project_creation_form(st.session_state.org, st.session_state.client)