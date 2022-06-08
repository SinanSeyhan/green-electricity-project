import streamlit as st
import importlib
import pandas as pd
import folium
from streamlit_folium import st_folium

'''
# ***Green Electricity Project***

TODO:

- HEROKU Connection

- Prediction Consumption Chart

- Energy Mix Chart with country filtering - DONE!

- Exports Chart

-

'''
st.markdown("""---""")
st.title(''' **Democracy Index** ''')
imports_module = importlib.import_module("green-electricity-project.Electricity_Imports", package=True).Imports()
st.plotly_chart(figure_or_data=imports_module.EU_visualize(), sharing='streamlit')
#st.plotly_chart(figure_or_data=imports_module.Democracy_visualize(), sharing='streamlit')


#st.markdown(''' ***Predicting Production*** ''')



# ENERGY MIX
st.markdown("""---""")
st.title('Energy Mix')
power_module = importlib.import_module("green-electricity-project.powerplants", package=True).PowerPlants()
df = power_module.get_eu_power_plants()
# Create dropdown menu:
countries = tuple(df.country)
option = st.selectbox(label='Please select the Country you want to see: ', options=countries)

# Total generation capacity:
capa = df[df['country']==option]['total_gw_calculated'].values[0]
st.subheader(f'Total capacity of **{option}**: ***{round(capa, 2)}*** GW')

# Pie Chart
st.header(f"{option}'s Energy Mix in Electricity")
st.plotly_chart(power_module.plot_eu_mix(option), sharing='streamlit')
st.markdown("""---""")

st.title('Power Plants Geolocation')
m = power_module.plot_folium()
st_folium(m)
st.markdown("""---""")

st.title(''' ***Consumption*** ''')
consumption_module = importlib.import_module("green-electricity-project.consumption", package=True).Consumption()
df = consumption_module.prepare_consumption_and_export()
df
st.markdown("""---""")


st.markdown("""---""")
st.markdown(''' **Model** ''')
trainer_module = importlib.import_module("green-electricity-project.trainer", package=True).Trainer()
consumption_module = importlib.import_module("green-electricity-project.consumption", package=True).Consumption()
df = consumption_module.get_consumption()
temp = df[df['energy_balance']=='Finalconsumption-transportsector-energyuse']
pred = {}

eu_df = pd.DataFrame(temp.groupby('Alpha_2_code').sum().sum())
split = trainer_module.split(eu_df, year='2018')[0]
model = trainer_module.initialize_model()
model.fit(split)
pred = trainer_module.predict(horizon=13)[['ds', 'yhat']]
df = pd.DataFrame.from_dict(pred)
df

st.plotly_chart((df.ds, df.yhat))
st.plotly_chart(split)
st.markdown("""---""")
