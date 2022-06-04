import streamlit as st
import importlib
'''
# Green Electricity Project
'''

st.markdown(''' ***Power Plants*** ''')
power_module = importlib.import_module("green-electricity-project.powerplants", package=True).PowerPlants()
st.plotly_chart(power_module.plot_eu_mix(), sharing='streamlit')


st.markdown(''' ***Exports*** ''')
exports_module = importlib.import_module("green-electricity-project.exports", package=True).Exports()
df_exp = exports_module.get_total_eu_exports()
df_exp

st.markdown(''' ***Democracy Index*** ''')
utils_module = importlib.import_module("green-electricity-project.utils", package=True).DemocracyIndex()
st.plotly_chart(figure_or_data=utils_module.plot_democracy_index(), sharing='streamlit')



st.markdown(''' ***Democracy Index*** ''')
imports_module = importlib.import_module("green-electricity-project.Electricity_Imports", package=True).Imports()
st.plotly_chart(figure_or_data=imports_module.EU_visualize(), sharing='streamlit')
st.plotly_chart(figure_or_data=imports_module.Democracy_visualize(), sharing='streamlit')
#imports_module.overall_imports()

# st.markdown(''' ***Model*** ''')
# validate_module = importlib.import_module("green-electricity-project.predict", package=True).Prediction()
# df_exp = validate_module.validate_EU_countries()
# df_exp
