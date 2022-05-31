# import code
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

path = '../raw_data/Production_Cleaned.csv'

class EuElecProduction():

    def __init__(self, path):
        self.df = None
        self.path = path

    def get_data(self):
        '''Function to Import relevant files and complete preprocessing
        Open EU Electricity production file and inspect'''
        self.df = pd.read_csv(self.path, encoding = 'unicode_escape')

    def EU_production(self):
        '''Filtering Energy Production data to EU-27 Countries only and to (also excluding the
        UK from EU) + adding 3 letter country codes'''

        countries = pd.read_csv('../raw_data/CountryCodes.csv', encoding = 'unicode_escape')
        self.df = self.df.merge(countries, on='Alpha_2_code', how='left')

        '''Create a dataframe for EU countries along with alpha-2-code'''

        EU_countries = pd.DataFrame.from_dict([{'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany': 'DE', 'Estonia': 'EE', 'Ireland': 'IE', 'Greece': 'EL',
                        'Spain': 'ES', 'France': 'FR', 'Croatia': 'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT', 'Luxembourg': 'LU', 
                        'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal': 'PT', 'Romania': 'RO', 'Slovenia': 'SI',
                        'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'}])

        EU_countries = EU_countries.T.reset_index()
        EU_countries.rename(columns={'index': 'EU_country', 0: 'Alpha_2_code'}, inplace=True)
        self.df['EU?'] = self.df['Alpha_2_code'].isin(EU_countries['Alpha_2_code'])
        EU_production = self.df.loc[self.df['EU?'] == True]
        return EU_production

    def EU_production_annual(EU_production):
        '''To see if there are null or duplicate values this far and to get to GEP, NEP for EU'''
        # EU_production.isna().sum().sum()#null values
        # sum(EU_production.duplicated()) # (no duplicate value = zero) THESE 2 COMMANDS WORK ONLY ON JUPYTER NOTEBOOK

        #Filtering by Total Energy production using EU_production['operator'] = Total, ignoring 'PRR_AUTO', 'PRR_MAIN'
        EU_production_annual = EU_production.loc[EU_production['operator'] == 'TOTAL']

        #Filtering by Total Electricity production using EU_production_annual['unit'] == 'GWH', ignoring heat and others
        EU_production_annual = EU_production_annual.loc[EU_production_annual['unit'] == 'GWH']
        columns = ['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000',
                '2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
                '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']

        # EU_production_annual_missing_val = EU_production_annual.groupby('Alpha_2_code').aggregate(lambda serie: serie.eq(': ').sum())
        # missing_production_data_countries = EU_production_annual_missing_val[EU_production_annual_missing_val.sum(axis=1) != 0]

        return EU_production_annual, columns
    
    def EU_Total_Elec_production(EU_production_annual, columns):
        #EU Annual Electricity Production
        EU_production_annual[columns]= EU_production_annual[columns].apply(pd.to_numeric, errors = 'coerce')
        EU_production_annual.loc['EU_Total'] = EU_production_annual[columns].sum()
        EU_Total_Elec_production = EU_production_annual
        return EU_Total_Elec_production

    def EU_Total_NEP(EU_production_annual, columns):
        #Adding EU Total NEP by year as a separate dataframe (for easy further analysis)
        EU_Total_NEP = EU_production_annual.loc[EU_production_annual['nrg_bal'] == 'NEP']
        EU_Total_NEP = pd.DataFrame(EU_production_annual[columns].sum())
        EU_Total_NEP = EU_Total_NEP.rename(columns={0:'NEP'})
        return EU_Total_NEP

    def EU_Total_GEP(EU_production_annual, columns):
        #Adding EU Total GEP by year as a separate dataframe (for easy further analysis)
        EU_Total_GEP = EU_production_annual.loc[EU_production_annual['nrg_bal'] == 'GEP']
        EU_Total_GEP = pd.DataFrame(EU_production_annual[columns].sum())
        EU_Total_GEP = EU_Total_GEP.rename(columns={0:'GEP'})
        return EU_Total_GEP

    def GEP_vs_NEP(EU_production_annual):
        #EU Electricity Production Comparision: GEP vs NEP
        EU_production_annual_nrg_bal = EU_production_annual.groupby('nrg_bal').sum()
        EU_production_annual_nrg_bal.reset_index(inplace=True)
        mask = EU_production_annual_nrg_bal.loc[:, '1990':'2020'] == 0
        plt.figure(figsize=(10,5))
        sns.heatmap(EU_production_annual_nrg_bal.loc[:, '1990':'2020'], yticklabels=EU_production_annual_nrg_bal['nrg_bal'], mask=mask, cmap="viridis")
        EU_production_annual_nrg_bal.set_index('nrg_bal').loc[:, '1990':'2020'].T.plot(figsize=(10,5))
        plt.show()

    def Germany_analysis(EU_production_annual):
        '''Electricity Production analysis by country (example: Germany)'''
        Elec_production_germany = EU_production_annual[EU_production_annual['Alpha_2_code'] == 'DE']
        Gross_Net_Elec_Prod_Germany = Elec_production_germany.groupby(Elec_production_germany['nrg_bal']).sum()
        return Gross_Net_Elec_Prod_Germany

    def EU_production_annual_totals(EU_production_annual):

        #Converting all data to floats to do math on them
        EU_production_annual_float = EU_production_annual.loc[:, '1990':'2020'].replace(': ',np.nan).astype(float)
        EU_production_annual_float = pd.merge(EU_production_annual.loc[:, :'Alpha_2_code'], EU_production_annual_float, left_index=True, right_index=True)
        EU_production_annual_totals = EU_production_annual_float.groupby('Alpha_2_code').sum()
        return EU_production_annual_totals

    def EU_Elec_1990_to_2020(EU_production_annual_totals):
        #Heatmaps Comparison of Electricity Production 
        mask = EU_production_annual_totals.loc[:, '1990':'2020'] == 0
        plt.figure(figsize=(20,15))
        sns.heatmap(EU_production_annual_totals.loc[:, '1990':'2020'], yticklabels=EU_production_annual_totals['Alpha_2_code'], mask=mask, cmap="viridis")
        plt.show()

    

    def groupby_quartiles(df, columnname, quartiles_asc):
        '''Group EU Electricity producing countries by quartiles'''
        df[columnname + '_perc'] = df[columnname]/df[columnname].sum()*100
        cumulative = df[columnname + '_perc'].sort_values(ascending=quartiles_asc).cumsum()
        
        if quartiles_asc == False:
            df['highest_quartile'] = cumulative >= 75
            df['2nd_highest_quartile'] = cumulative.between(50,75, inclusive='left')
            df['2nd_lowest_quartile'] = cumulative.between(25,50, inclusive='left')
            df['lowest_quartile'] = cumulative < 25
        
        elif quartiles_asc == True:
            df['lowest_quartile'] = cumulative <= 25
            df['2nd_lowest_quartile'] = cumulative.between(25,50, inclusive='right')
            df['2nd_highest_quartile'] = cumulative.between(50,75, inclusive='right')
            df['highest_quartile'] = cumulative > 75
        
        df['quartile'] = (df.iloc[:, 1:] == 1).idxmax(1)
        df.set_index('quartile',inplace=True)
        
        df = df.loc[:,'1990':'2020']
        df = df.groupby('quartile').sum()
        
        return df
    
    # def groupby_quartiles_2020(df, columnname, quartiles_asc):
    #     EU_Elec_prod_NEP_Quartiles = EuElecProduction.groupby_quartiles(EU_Elec_prod_NEP, '2020', quartiles_asc=True)





if __name__ == '__main__':
    preproccer = EuElecProduction(path)
    preproccer.get_data()
    EU_countries = EuElecProduction.EU_countries()
    EU_production = preproccer.EU_production()
    EU_production_annual, columns = preproccer.EU_production_annual(EU_production)
