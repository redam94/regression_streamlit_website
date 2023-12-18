import streamlit as st

def main():
  if 'fitted_model_list' in st.session_state:
    for i, model in enumerate(st.session_state.fitted_model_list[::-1]):
      score_name, score = model.model.model_score()
      with st.expander(str(model.id)[:8] + f" {score_name}: {score:.3f}" + f" Time: {model.time}"):
        model.model.save_model(str(model.id))
        st.write(model.time)
        st.write(model.model.summary())
        st.divider()
        st.write("Data Transformation Details")
        st.write(model.model.transform_df)
        st.pyplot(model.model.plot_avm())
  

if __name__ == '__main__':
  main()

        