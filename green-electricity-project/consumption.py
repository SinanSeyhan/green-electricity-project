import pandas as pd
import numpy as np

class Consumption():
    '''
    Prepares consumption data and replaces export entry with data from export file if necessary.
    consumption_path: path to Consumption .csv-file
    exports_path: path to Exports .csv-file
    country:
        list: select country name or 'EU' for EU as a whole, multiple countries can be passed to group them
    get_quartiles:
        if True, group consumption categories ("energy_balance") by quartiles based on consumption within the year defined in "quartile_col"
        if False, retrieve raw consumption categories
    quartiles_asc:
        if True, first quartile (1) is lowest 25 percent (cumulative sum from 0 to 25 percent, including 25 percent)
        if False, first quartile (1) is highest 25 percent (cumulative sum from 75 to 100 percent, including 75 percent)
    quartile_col: column name (year as a string) which the calculated quartiles are based on
    '''
    def __init__(self, consumption_path = 'raw_data/Consumption_Cleaned.csv', exports_path = 'raw_data/Exports_Cleaned.csv',
                 country = ['EU'],
                 get_quartiles=True,
                 quartiles_asc=True, quartile_col='2019'):

        self.unused_cats= [
            "Availableforfinalconsumption", "Finalconsumption",
            "Grosselectricityproduction", "Imports", "Inlanddemand",
            "Netelectricityproduction", "Statisticaldifferences"
        ]

        self.consumption_path = consumption_path
        self.exports_path = exports_path
        self.country = country
        self.get_quartiles = get_quartiles
        self.quartiles_asc = quartiles_asc
        self.quartile_col = quartile_col


    def get_consumption(self):
        '''
        Prepare Consumption data
        '''
        consumption_df = pd.read_csv(self.consumption_path)

        if self.country == ['EU']:
            # Delete non-EU countries
            consumption_df_selected_country = consumption_df[consumption_df['EU?']].loc[:, 'energy_balance_code':]

        else:
            # Filter selected country
            consumption_df_selected_country = consumption_df[
                consumption_df['Country'].isin(self.country)].loc[:, 'energy_balance_code':]

        # Delete unused categories (non-consumption categories of "energy_balance")
        consumption_df_selected_country = consumption_df_selected_country[
            ~consumption_df_selected_country['energy_balance'].
            isin(self.unused_cats)]

        # Replace not avaliable data (':') with np.nan and transform all values of year columns to float values
        consumption_df_float = consumption_df_selected_country.loc[:, '1990':
                                                                   '2020'].replace(to_replace=[':', ': '], value=np.nan).astype(float)

        # Merge to float transformed year columns with countries and consumption categories ("energy_balance")
        consumption_df_float_complete = pd.merge(
            consumption_df_selected_country.
            loc[:, 'energy_balance':'Alpha_2_code'],
            consumption_df_float,
            left_index=True,
            right_index=True).drop(columns='EU?')

        self.consumption_df_float_complete = consumption_df_float_complete

        return consumption_df_float_complete



    def get_exports(self):
        exports_df = pd.read_csv(self.exports_path)

        if self.country == ['EU']:
            # Delete non-EU countries
            exports_df_selected_country = exports_df[exports_df['EU?']]
        else:
            # Filter selected country
            exports_df_selected_country = exports_df[
                exports_df['Country'].isin(self.country)]

        # Delete heat export (only use electricity exports defined by 'siec' = 'E7000')
        exports_df_selected_country_elec = exports_df_selected_country[
            exports_df_selected_country['siec'] == 'E7000']
        exports_df_selected_country_elec = exports_df_selected_country.loc[:, 'partner':].drop(
            columns=['unit', 'EU?', 'Alpha_3_code'])

        # Replace not avaliable data (':') with np.nan and transform all values of year columns to float values
        exports_df_selected_country_elec_float = exports_df_selected_country_elec.loc[:, '1990':'2020'].replace(to_replace=[':', ': '], value=np.nan).astype(float)

        # Merge to float transformed year columns with countries and consumption categories ("energy_balance")
        exports_df_selected_country_elec_float_complete = pd.merge(
            exports_df_selected_country_elec.loc[:, :'Alpha_2_code'],
            exports_df_selected_country_elec_float,
            left_index=True,
            right_index=True)

        # Delete 'TOTAL' entry from 'partner' countries
        exports_df_selected_country_elec_float_complete = exports_df_selected_country_elec_float_complete[
            exports_df_selected_country_elec_float_complete['partner'] !=
            'TOTAL']

        exports_by_country = exports_df_selected_country_elec_float_complete[
            ~exports_df_selected_country_elec_float_complete['partner'].isin(
                exports_df_selected_country_elec_float_complete['Alpha_2_code']
            )]


        # Sum up all exports to of each country
        exports_by_country = exports_by_country.groupby(
            ['Alpha_2_code', 'partner']).sum()
        exports_by_country.reset_index(inplace=True)

        return exports_by_country



    def groupby_quartiles(self):
        '''
        Sort consumption categories by value and group them by quartiles
        '''
        cons_df_by_energy_bal = self.cons_df_by_energy_bal
        # Calculate percentage of each consumption category
        cons_df_by_energy_bal[self.quartile_col + '_perc'] = cons_df_by_energy_bal[self.quartile_col] / cons_df_by_energy_bal[self.quartile_col].sum() * 100

        # Create column containing the cumulative sum of the sorted percentage values
        cumulative = cons_df_by_energy_bal[self.quartile_col + '_perc'].sort_values(ascending=self.quartiles_asc).cumsum()


        if self.quartiles_asc == False:
            # Create quartiles beginning with the highest percentage including the lower boundary values
            # Add boolean column for each quartile (one hot encoded)
            cons_df_by_energy_bal[1] = cumulative >= 75
            cons_df_by_energy_bal[2] = cumulative.between(50,75,inclusive='left')
            cons_df_by_energy_bal[3] = cumulative.between(25,50,inclusive='left')
            cons_df_by_energy_bal[4] = cumulative < 25

        elif self.quartiles_asc == True:
            # Create quartiles beginning with the lowest percentage including the upper boundary values
            # Add boolean column for each quartile (one hot encoded)
            cons_df_by_energy_bal[1] = cumulative <= 25
            cons_df_by_energy_bal[2] = cumulative.between(25,50,inclusive='right')
            cons_df_by_energy_bal[3] = cumulative.between(50,75,inclusive='right')
            cons_df_by_energy_bal[4] = cumulative > 75

        self.cons_df_by_energy_bal_quartiles = cons_df_by_energy_bal.copy()

        # Inverse One Hot Encoding: Create "quartile" column and set it as index
        cons_df_by_energy_bal['quartile'] = (cons_df_by_energy_bal.iloc[:, 1:] == 1).idxmax(1)
        cons_df_by_energy_bal.set_index('quartile',inplace=True)

        # Remove "one hot encoded" Quartile Columns and group dataframe by quartile
        cons_df_by_energy_bal = cons_df_by_energy_bal.loc[:, '1990':'2020']
        cons_df_by_energy_bal = cons_df_by_energy_bal.groupby('quartile').sum()

        return cons_df_by_energy_bal


    def prepare_consumption_and_export(self):
        # load prepared consumption and export dataframes
        cons_df = self.get_consumption()
        exp_df = self.get_exports()

        # replace total summed up exports with exports to non-selected countries (don't count domestic exports!)
        cons_df_by_energy_bal = pd.DataFrame(cons_df.groupby('energy_balance').sum())
        cons_df_by_energy_bal.loc[['Exports']] = exp_df.loc[:, '1990':].sum().values

        self.cons_df_by_energy_bal = cons_df_by_energy_bal

        if self.get_quartiles == True:
            cons_df_by_energy_bal = self.groupby_quartiles()
            self.cons_df_by_energy_bal = cons_df_by_energy_bal

        return cons_df_by_energy_bal

if __name__ == "__main__":
    consumption = Consumption(quartiles_asc=False)
    cons_exp_quart_desc = consumption.prepare_consumption_and_export()
    print(cons_exp_quart_desc)
