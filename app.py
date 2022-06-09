import streamlit as st
import importlib
import pandas as pd
import folium
from streamlit_folium import st_folium


st.title('Green Electricity')
st.subheader('Electricity, is it green or not?🤔')

###############################
        ## IMPORTS ##
###############################

st.markdown("""---""")
st.title(''' **Imports** ''')
imports_module = importlib.import_module("green-electricity-project.Electricity_Imports", package=True).Imports()
st.plotly_chart(figure_or_data=imports_module.EU_visualize(), sharing='streamlit')

###########################################




###############################
        ## ENERGY MIX ##
###############################

st.markdown("""---""")
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

<<<<<<< HEAD
=======
###########################################




###########################################
        ## GEOLOCATION POWER PLANTS ##
###########################################
>>>>>>> 9b7b4a322d12ceecb7812b8b6121a2c1d20337bf

st.title('Power Plants Geolocation')

# Create dropdown menu:
df = power_module.get_geolocation()
fuel = tuple(sorted(df.primary_fuel.unique()))
option = st.selectbox(label='Please select the Fuel Type you want to see: ', options=fuel)

m = power_module.plot_folium(option)
st_folium(m, width=1000, height=800)
st.markdown("""---""")

<<<<<<< HEAD
st.title('Consumption')
consumption_module = importlib.import_module(
    "green-electricity-project.consumption_viz_and_pred", package=True)

option_cons = st.selectbox(
    'Select a country',
    ('EU', 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
     'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
     'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
     'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
     'Spain', 'Sweden'),
    key='option_cons')

run = st.button("Predict Future Consumption")

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
=======
st.title(''' ***Consumption*** ''')
consumption_module = importlib.import_module("green-electricity-project.consumption", package=True).Consumption()
df = consumption_module.prepare_consumption_and_export()

st.markdown("""---""")

###########################################



>>>>>>> 9b7b4a322d12ceecb7812b8b6121a2c1d20337bf

# st.markdown("""---""")
# st.markdown(''' **Model** ''')
# trainer_module = importlib.import_module("green-electricity-project.trainer", package=True).Trainer()
# consumption_module = importlib.import_module("green-electricity-project.consumption", package=True).Consumption()
# df = consumption_module.get_consumption()
# temp = df[df['energy_balance']=='Finalconsumption-transportsector-energyuse']
# pred = {}

# eu_df = pd.DataFrame(temp.groupby('Alpha_2_code').sum().sum())
# split = trainer_module.split(eu_df, year='2018')[0]
# model = trainer_module.initialize_model()
# model.fit(split)
# pred = trainer_module.predict(horizon=13)[['ds', 'yhat']]
# df = pd.DataFrame.from_dict(pred)
# df

# st.plotly_chart((df.ds, df.yhat))
# st.plotly_chart(split)
# st.markdown("""---""")
