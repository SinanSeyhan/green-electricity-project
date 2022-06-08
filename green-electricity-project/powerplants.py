# Python file to get the cleaned up version of Power Plants Database
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import os
import plotly.express as px
import folium
from folium.plugins import MarkerCluster

class PowerPlants():
    def __init__(self):
        pass

    def get_power_plants(self):
        '''
        Loads the Power Plants Database. Data taken from:
        https://github.com/wri/global-power-plant-database
        '''
        # Path for Streamlit
        my_path = os.path.abspath(os.path.dirname(__file__))
        POWER_PLANTS_PATH = os.path.join(my_path, "../raw_data/Power_Plants_Cleaned.csv")

        df = pd.read_csv(POWER_PLANTS_PATH)
        return df

    def get_eu_power_plants(self):
        '''
        Function that gives the cleaned Power Plants Database

        Output:
        Gives a dataframe for 27 EU countries the energy mix in percent and in GW.
        '''
        pd.set_option('mode.chained_assignment', None)
        df = self.get_power_plants()
        df_eu = df[df['EU?']==True]
        df_eu.reset_index(drop=True, inplace=True)
        df_eu.drop(columns=['Unnamed: 0', 'EU?', 'count_distinct_fuel', 'count_distinct_name', 'count_distinct_owner',
                            'count_distinct_source', 'count_wepp_id', 'capacity_gw_wepp_id', 'count_null_generation_gwh_all',
                            'count_generation_gwh_2013', 'count_generation_gwh_2014', 'count_generation_gwh_2015',
                            'count_generation_gwh_2016', 'count_generation_gwh_2017', 'count_generation_gwh_2018',
                            'count_generation_gwh_2019', 'count_generation_data_source', 'count_estimated_generation_gwh',
                            'count_null_capacity_mw', 'count_null_longitude', 'count_null_latitude', 'count_null_name',
                            'count_null_source', 'count_null_url', 'count_null_fuel', 'count_null_owner', 'count_null_gppd_idnr',
                            'count_null_year_of_capacity_data', 'count', 'count_fuel_biomass', 'count_fuel_coal',
                            'count_fuel_cogeneration', 'count_fuel_gas', 'count_fuel_geothermal', 'count_fuel_hydro',
                            'count_fuel_nuclear', 'count_fuel_oil', 'count_fuel_other', 'count_fuel_petcoke', 'count_fuel_solar',
                            'count_fuel_storage', 'count_fuel_waste', 'count_fuel_wave_and_tidal', 'count_fuel_wind', 'iso_code'],
                            axis= 1, inplace=True)

        # Add EU total as the last row
        temp = df_eu.sum(axis=0, numeric_only=True)
        EU = dict(temp)
        EU['country'] = 'EU'
        df_eu = df_eu.append(EU, ignore_index=True)

        # Malta has all NaN values. Converted to zeros
        df_eu[df_eu['country']=='Malta'] = df_eu[df_eu['country']=='Malta'].replace(np.NaN, 0)

        # Adding Percentage to the fuel mix
        df_eu['total_gw_calculated'] = df_eu[['capacity_gw_fuel_biomass', 'capacity_gw_fuel_coal', 'capacity_gw_fuel_cogeneration',
                                            'capacity_gw_fuel_gas', 'capacity_gw_fuel_geothermal', 'capacity_gw_fuel_hydro',
                                            'capacity_gw_fuel_nuclear', 'capacity_gw_fuel_oil', 'capacity_gw_fuel_other',
                                            'capacity_gw_fuel_petcoke', 'capacity_gw_fuel_solar', 'capacity_gw_fuel_storage',
                                            'capacity_gw_fuel_waste', 'capacity_gw_fuel_wave_and_tidal', 'capacity_gw_fuel_wind']].sum(axis=1)

        # Calculating the percentages of the energy mix
        fuels = ['biomass', 'coal', 'cogeneration', 'gas', 'geothermal', 'hydro', 'nuclear', 'oil', 'other', 'petcoke',
                'solar', 'storage', 'waste', 'wave_and_tidal', 'wind']

        for fuel in fuels:
            df_eu[f'percent_{fuel}'] = round((df_eu[f'capacity_gw_fuel_{fuel}'] / df_eu['total_gw_calculated']) * 100, 2)

        # Removing 0 columns
        df_eu.drop(columns=['capacity_gw_fuel_cogeneration', 'capacity_gw_fuel_petcoke', 'capacity_gw_fuel_storage',
                    'percent_cogeneration', 'percent_petcoke', 'percent_storage'], inplace=True)

        # Getting the final structure of the dataset
        df_eu = df_eu[['country', 'total_capacity_gw','total_gw_calculated', 'max_capacity_mw',
                    'capacity_gw_fuel_biomass','capacity_gw_fuel_coal', 'capacity_gw_fuel_gas', 'capacity_gw_fuel_geothermal',
                    'capacity_gw_fuel_hydro', 'capacity_gw_fuel_nuclear', 'capacity_gw_fuel_oil', 'capacity_gw_fuel_other',
                    'capacity_gw_fuel_solar', 'capacity_gw_fuel_waste', 'capacity_gw_fuel_wave_and_tidal', 'capacity_gw_fuel_wind',
                    'percent_biomass', 'percent_coal', 'percent_gas', 'percent_geothermal', 'percent_hydro', 'percent_nuclear',
                    'percent_oil', 'percent_other', 'percent_solar', 'percent_waste', 'percent_wave_and_tidal', 'percent_wind']]

        return df_eu

    def get_eu_cluster(self, n_clusters=4):
        '''
        adds another 'cluster' column to EU countries according to their electricity generation capacity.

        inputs:
        n_clusters: int. To define the number of clusters

        '''
        # Loading dataset
        df_eu = self.get_eu_power_plants()

        # Declaring Model
        model = KMeans(n_clusters)

        # Fitting Model
        model.fit(df_eu.total_gw_calculated.to_numpy().reshape(-1, 1))

        # Prediction on the entire data
        all_predictions = model.predict(df_eu.total_gw_calculated.to_numpy().reshape(-1, 1))
        df_eu['cluster'] = all_predictions

        return df_eu

    def plot_eu_mix(self, country):
        '''
        Plots a country's Energy Mix

        country: str
        '''
        df = self.get_eu_power_plants()
        df.rename({'percent_biomass': 'Biomass',
                'percent_coal': 'Coal',
                'percent_gas': 'Gas',
                'percent_geothermal': 'Geothermal',
                'percent_hydro': 'Hydro',
                'percent_nuclear': 'Nuclear',
                'percent_oil': 'Oil',
                'percent_other': 'Other',
                'percent_solar': 'Solar',
                'percent_waste': 'Waste',
                'percent_wave_and_tidal': 'Wave and Tidal',
                'percent_wind': 'Wind'
            },axis=1, inplace=True)
        plot_df = df[df['country']==country]
        plot_df = plot_df.drop(columns=['total_capacity_gw', 'total_gw_calculated', 'max_capacity_mw', 'capacity_gw_fuel_biomass', 'capacity_gw_fuel_coal',
                                        'capacity_gw_fuel_gas', 'capacity_gw_fuel_geothermal', 'capacity_gw_fuel_hydro', 'capacity_gw_fuel_nuclear',
                                        'capacity_gw_fuel_oil', 'capacity_gw_fuel_other', 'capacity_gw_fuel_solar', 'capacity_gw_fuel_waste',
                                        'capacity_gw_fuel_wave_and_tidal', 'capacity_gw_fuel_wind'], axis=1)
        plot_df = plot_df[plot_df!=0]
        plot_df = plot_df.dropna(axis=1)
        names = list(plot_df.drop(columns='country', axis=1).columns)
        values = list(plot_df.drop(columns='country', axis=1).values[0])

        fig = px.pie(data_frame=plot_df.T,
                    values=values,
                    names=names,
                    hole=0.3,
                    color=names,
                    color_discrete_map = {'Biomass': 'darkgreen',
                                        'Coal': 'dimgray',
                                        'Gas': 'saddlebrown',
                                        'Geothermal': 'fuchsia',
                                        'Hydro': 'lightseagreen',
                                        'Nuclear': 'greenyellow',
                                        'Oil': 'darkbrown',
                                        'Other': 'white',
                                        'Solar': 'goldenrod',
                                        'Waste': 'chocolate',
                                        'Wave and Tidal': 'navy',
                                        'Wind': 'deepskyblue'},
                    width=(800),
                    height=(800)
                    )
        # Text inside the Sectors
        fig.update_traces(textposition = 'outside' , textinfo = 'percent+label')
        return fig

    def get_geolocation(self):
        '''
        Function to get the geolocation of the Power Plants inside EU
        '''
        my_path = os.path.abspath(os.path.dirname(__file__))
        POWER_PLANTS_ALL_PATH = os.path.join(my_path, "../raw_data/global_power_plant_database.csv")
        df = pd.read_csv(POWER_PLANTS_ALL_PATH, low_memory=False)

        EU_Countries = ['Belgium', 'Bulgaria', 'Czech Republic', 'Denmark', 'Germany', 'Estonia', 'Ireland',
                        'Greece', 'Spain', 'France', 'Croatia', 'Italy', 'Cyprus', 'Latvia', 'Lithuania',
                        'Luxembourg', 'Hungary', 'Malta', 'Netherlands (the)', 'Austria', 'Poland', 'Portugal',
                        'Romania', 'Slovenia', 'Slovakia', 'Finland', 'Sweden']


        df.drop(columns=['country', 'name', 'gppd_idnr', 'other_fuel1', 'other_fuel2',
                        'other_fuel3', 'commissioning_year', 'owner', 'source', 'url',
                        'geolocation_source', 'wepp_id', 'year_of_capacity_data',
                        'generation_gwh_2013', 'generation_gwh_2014', 'generation_gwh_2015',
                        'generation_gwh_2016', 'generation_gwh_2017', 'generation_gwh_2018',
                        'generation_gwh_2019', 'generation_data_source',
                        'estimated_generation_gwh_2013', 'estimated_generation_gwh_2014',
                        'estimated_generation_gwh_2015', 'estimated_generation_gwh_2016',
                        'estimated_generation_gwh_2017', 'estimated_generation_note_2013',
                        'estimated_generation_note_2014', 'estimated_generation_note_2015',
                        'estimated_generation_note_2016', 'estimated_generation_note_2017'], axis=1, inplace=True)
        df_eu = df[df['country_long'].isin(EU_Countries)]
        df_eu.reset_index(drop=True, inplace=True)
        return df_eu

    def plot_folium(self, fuel):
        '''
        Function to get the Folium Map for the Power Plants in EU
        '''
        # country_long  capacity_mw  latitude  longitude primary_fuel
        df = self.get_geolocation()
        df = df[df['primary_fuel']==fuel]
        geolocation = df.get(['latitude', 'longitude']).values.tolist()
        popups = df.get(['country_long', 'capacity_mw', 'primary_fuel']).values.tolist()
        EU_COORDINATES = (49.5260, 15.2551)

        # create empty map zoomed in on Europe
        _map = folium.Map(location=EU_COORDINATES, zoom_start=4, tiles='cartodb positron', position='centered')

        # add a marker for every record in the filtered data, use a clustered view
        MarkerCluster(locations=geolocation, popups=popups, show=True).add_to(_map)
        return _map

if __name__ == '__main__':
    #print(PowerPlants().get_geolocation())
    print(PowerPlants().plot_folium())
