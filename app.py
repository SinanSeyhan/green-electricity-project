import streamlit as st
import importlib
'''
# Green Electricity Project
'''

st.markdown(''' ***Power Plants*** ''')
power_module = importlib.import_module("green-electricity-project.powerplants", package=True).PowerPlants()
df = power_module.get_eu_power_plants()
df


st.markdown(''' ***Exports*** ''')
exports_module = importlib.import_module("green-electricity-project.exports", package=True).Exports()
df_exp = exports_module.get_total_eu_exports()
df_exp

st.markdown(''' ***Model*** ''')
validate_module = importlib.import_module("green-electricity-project.predict", package=True).Prediction()
df_exp = validate_module.validate_EU_countries()
df_exp
