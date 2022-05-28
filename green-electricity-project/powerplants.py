# Python file to get the cleaned up version of Power Plants Database
import pandas as pd
import numpy as np

class PowerPlants():
    def __init__(self):
        pass

    def get_power_plants(self):
        POWER_PLANTS_PATH = '../raw_data/Power_Plants_Cleaned.csv'
        df = pd.read_csv(POWER_PLANTS_PATH)
        return df

    def get_eu_power_plants(self):
        '''
        Function that gives the cleaned Power Plants Database
        '''
        pd.set_option('mode.chained_assignment', None)
        df = PowerPlants().get_power_plants()
        df_eu = df[df['EU?']==True]
        df_eu.reset_index(drop=True, inplace=True)
        df_eu.drop(columns=['Unnamed: 0',
                            'EU?',
                            'count_distinct_fuel',
                            'count_distinct_name',
                            'count_distinct_owner',
                            'count_distinct_source',
                            'count_wepp_id',
                            'capacity_gw_wepp_id',
                            'count_null_generation_gwh_all',
                            'count_generation_gwh_2013',
                            'count_generation_gwh_2014',
                            'count_generation_gwh_2015',
                            'count_generation_gwh_2016',
                            'count_generation_gwh_2017',
                            'count_generation_gwh_2018',
                            'count_generation_gwh_2019',
                            'count_generation_data_source',
                            'count_estimated_generation_gwh',
                            'count_null_capacity_mw',
                            'count_null_longitude',
                            'count_null_latitude',
                            'count_null_name',
                            'count_null_source',
                            'count_null_url',
                            'count_null_fuel',
                            'count_null_owner',
                            'count_null_gppd_idnr',
                            'count_null_year_of_capacity_data',
                            'count',
                            'count_fuel_biomass',
                            'count_fuel_coal',
                            'count_fuel_cogeneration',
                            'count_fuel_gas',
                            'count_fuel_geothermal',
                            'count_fuel_hydro',
                            'count_fuel_nuclear',
                            'count_fuel_oil',
                            'count_fuel_other',
                            'count_fuel_petcoke',
                            'count_fuel_solar',
                            'count_fuel_storage',
                            'count_fuel_waste',
                            'count_fuel_wave_and_tidal',
                            'count_fuel_wind',
                            'iso_code'], inplace=True)

        # Malta has all NaN values. Converted to zeros
        df_eu[df_eu['country']=='Malta'] = df_eu[df_eu['country']=='Malta'].replace(np.NaN, 0)

        # Adding Percentage to the fuel mix
        df_eu['total_gw_calculated'] = df_eu[['capacity_gw_fuel_biomass',
                                            'capacity_gw_fuel_coal',
                                            'capacity_gw_fuel_cogeneration',
                                            'capacity_gw_fuel_gas',
                                            'capacity_gw_fuel_geothermal',
                                            'capacity_gw_fuel_hydro',
                                            'capacity_gw_fuel_nuclear',
                                            'capacity_gw_fuel_oil',
                                            'capacity_gw_fuel_other',
                                            'capacity_gw_fuel_petcoke',
                                            'capacity_gw_fuel_solar',
                                            'capacity_gw_fuel_storage',
                                            'capacity_gw_fuel_waste',
                                            'capacity_gw_fuel_wave_and_tidal',
                                            'capacity_gw_fuel_wind']].sum(axis=1)

        fuels = ['biomass',
                'coal',
                'cogeneration',
                'gas',
                'geothermal',
                'hydro',
                'nuclear',
                'oil',
                'other',
                'petcoke',
                'solar',
                'storage',
                'waste',
                'wave_and_tidal',
                'wind']

        for fuel in fuels:
            df_eu[f'percent_{fuel}'] = round((df_eu[f'capacity_gw_fuel_{fuel}'] / df_eu['total_gw_calculated']) * 100, 2)

        # Removing 0 columns
        df_eu.drop(columns=['capacity_gw_fuel_cogeneration', 'capacity_gw_fuel_petcoke', 'capacity_gw_fuel_storage',
                    'percent_cogeneration', 'percent_petcoke', 'percent_storage'], inplace=True)

        # Getting the final structure of the dataset
        df_eu = df_eu[['country', 'total_capacity_gw','total_gw_calculated', 'max_capacity_mw',
                    'capacity_gw_fuel_biomass','capacity_gw_fuel_coal', 'capacity_gw_fuel_gas', 'capacity_gw_fuel_geothermal',
                    'capacity_gw_fuel_hydro', 'capacity_gw_fuel_nuclear',
                    'capacity_gw_fuel_oil', 'capacity_gw_fuel_other',
                    'capacity_gw_fuel_solar', 'capacity_gw_fuel_waste',
                    'capacity_gw_fuel_wave_and_tidal', 'capacity_gw_fuel_wind',
                    'percent_biomass', 'percent_coal', 'percent_gas', 'percent_geothermal', 'percent_hydro',
                    'percent_nuclear', 'percent_oil', 'percent_other', 'percent_solar',
                    'percent_waste', 'percent_wave_and_tidal', 'percent_wind']]
        return df_eu


if __name__ == '__main__':
    print(PowerPlants().get_eu_power_plants())