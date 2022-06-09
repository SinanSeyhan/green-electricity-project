import streamlit as st
import importlib
import pandas as pd
import folium
from streamlit_folium import st_folium
import os


st.title('Green Electricity')
st.subheader('Electricity, is it green or not?🤔')
st.markdown("""---""")
###########################################
## CONSUMPTION ##
###########################################

st.title('Consumption')
consumption_module = importlib.import_module(
    "green-electricity-project.consumption_viz_and_pred", package=True)

load_prepared_predictions = True

if load_prepared_predictions == False:
    option_cons = st.selectbox(
        'Select a country',
        ('EU', 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
        'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
        'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
        'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
        'Spain', 'Sweden'),
        key='option_cons')

if run:
    info = st.empty()
    info.write('Predicting the future of electricity consumption...')

    consumption = consumption_module.ConsumptionVaP(option_cons)
    consumption.run_viz_and_pred(load_prep = True)

    st.markdown(''' ****Historic Consumption 1990 - 2020**** ''')

    st.plotly_chart(consumption.fig, use_container_width=True)

    st.markdown(''' ****Prediction of selected consumption category**** ''')

    real_tot_cons_2019 = round(
        consumption.consumption_data.sum()['2015':'2019'].mean())
    pred_tot_cons_2030 = round(consumption.total_future_consumption[40])

    rise_perc = round(
        (pred_tot_cons_2030 - real_tot_cons_2019) / real_tot_cons_2019 * 100,
        2)

    if option_cons in ['Czech Republic', 'Netherlands', 'EU']:
        st.markdown(
            f'Until 2030 the total energy consumption of the <font color="red"><b>{option_cons}</b></font> will change by about',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'Until 2030 the total energy consumption of <font color="red"><b>{option_cons}</b></font> will change by about',
            unsafe_allow_html=True)

    st.markdown('<style>.big-font {font-size:50px !important;}</style>',
                unsafe_allow_html=True)
    st.markdown(
        f'<p class="big-font"><font color="red"><b>{rise_perc:+} %</b></font></p>',
        unsafe_allow_html=True)

    st.plotly_chart(consumption.fig_pred, use_container_width=True)



st.markdown("""---""")
###########################################

###############################
## PRODUCTION ##
###############################
st.title('Production')
# path = '../raw_data/Production_Cleaned.csv'
# production_module = importlib.import_module("green-electricity-project.production_viz", package=True).EuElecProduction()
# st.plotly_chart(production_module.GEP_pred_vs_Actual(), sharing='streamlit')
st.markdown("""---""")
###############################
## ENERGY MIX ##
###############################


st.title('Energy Mix of Countries')
power_module = importlib.import_module("green-electricity-project.powerplants", package=True).PowerPlants()
df = power_module.get_eu_power_plants()
# Create dropdown menu:
countries = tuple(df.country)
option = st.selectbox(label='Please select the Country you want to see: ', options=countries)

# Total generation capacity:
capa = df[df['country'] == option]['total_gw_calculated'].values[0]
st.subheader(f'Total capacity of **{option}**: ***{round(capa, 2)}*** GW')

# Pie Chart
st.header(f"{option}'s Energy Mix in Electricity")
st.plotly_chart(power_module.plot_eu_mix(option), sharing='streamlit')
st.markdown("""---""")

###########################################
=======

st.title('Consumption')

consumption_module = importlib.import_module(
    "green-electricity-project.consumption_viz_and_pred", package=True)

load_prepared_predictions = True

if load_prepared_predictions == False:
    option_cons = st.selectbox(
        'Select a country',
        ('EU', 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
        'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
        'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
        'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
        'Spain', 'Sweden'),
        key='option_cons')
>>>>>>> master

<<<<<<< HEAD
    run = st.button("Predict Future Consumption")

<<<<<<< HEAD
###########################################
## GEOLOCATION POWER PLANTS ##
###########################################
=======
    if run:
        info = st.empty()
        info.write('Predicting the future of electricity consumption...')
        consumption = consumption_module.ConsumptionVaP(option_cons)
        consumption.run_viz_and_pred(info)

    st.markdown(''' ****Historic Consumption 1990 - 2020**** ''')

    st.plotly_chart(consumption.fig, use_container_width=True)

    st.markdown(''' ****Prediction of selected consumption category**** ''')

    real_tot_cons_2019 = round(
        consumption.consumption_data.sum()['2015':'2019'].mean())
    pred_tot_cons_2030 = round(consumption.total_future_consumption[40])

    rise_perc = round(
        (pred_tot_cons_2030 - real_tot_cons_2019) / real_tot_cons_2019 * 100,
        2)

    if option_cons in ['Czech Republic', 'Netherlands', 'EU']:
        st.markdown(
            f'Until 2030 the total energy consumption of the <font color="red"><b>{option_cons}</b></font> will change by about',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'Until 2030 the total energy consumption of <font color="red"><b>{option_cons}</b></font> will change by about',
            unsafe_allow_html=True)

    st.markdown('<style>.big-font {font-size:50px !important;}</style>',
                unsafe_allow_html=True)
    st.markdown(
        f'<p class="big-font"><font color="red"><b>{rise_perc:+} %</b></font></p>',
        unsafe_allow_html=True)

    st.plotly_chart(consumption.fig_pred, use_container_width=True)


st.markdown("""---""")
###########################################

###############################
## PRODUCTION ##
###############################
st.title('Production')
path = '../raw_data/Production_Cleaned.csv'
production_module = importlib.import_module("green-electricity-project.production_viz", package=True).EuElecProduction()
st.plotly_chart(production_module.GEP_pred_vs_Actual(), sharing='streamlit')

#st.area_chart(production_module.Elec_Mix_chart())


st.markdown("""---""")
###############################
## ENERGY MIX ##
###############################


st.title('Energy Mix of Countries')
power_module = importlib.import_module("green-electricity-project.powerplants", package=True).PowerPlants()
df = power_module.get_eu_power_plants()
# Create dropdown menu:
countries = tuple(df.country)
option = st.selectbox(label='Please select the Country you want to see: ', options=countries)

# Total generation capacity:
capa = df[df['country'] == option]['total_gw_calculated'].values[0]
st.subheader(f'Total capacity of **{option}**: ***{round(capa, 2)}*** GW')

# Pie Chart
st.header(f"{option}'s Energy Mix in Electricity")
st.plotly_chart(power_module.plot_eu_mix(option), sharing='streamlit')
st.markdown("""---""")

###########################################


###########################################
## GEOLOCATION POWER PLANTS ##
###########################################

st.title('Power Plants Geolocation')

# Create dropdown menu:
df = power_module.get_geolocation()
fuel = tuple(sorted(df.primary_fuel.unique()))
option = st.selectbox(label='Please select the Fuel Type you want to see: ', options=fuel)

m = power_module.plot_folium(option)
st_folium(m, width=1000, height=800)
st.markdown("""---""")

###########################################



###############################
## IMPORTS ##
###############################

st.title(''' **Imports** ''')
imports_module = importlib.import_module("green-electricity-project.Electricity_Imports", package=True).Imports()
st.plotly_chart(figure_or_data=imports_module.EU_visualize(), sharing='streamlit')
st.markdown("""---""")

###########################################
