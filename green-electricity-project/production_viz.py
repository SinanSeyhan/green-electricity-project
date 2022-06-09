import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import importlib
import os
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


path = '../raw_data/Production_Cleaned.csv'

class EuElecProduction():

    def __init__(self, path):
        self.df = None
        self.path = path
        self.columns = ['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000',
                '2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
                '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']

    def get_data(self):
        '''Function to Import relevant files and complete preprocessing
        Open EU Electricity production file and inspect'''
        self.df = pd.read_csv(self.path, encoding = 'unicode_escape')

    def EU_production_annual(self):
        '''Filtering Energy Production data to EU-27 Countries only and to (also excluding the
        UK from EU) + adding 3 letter country codes'''

        countries = pd.read_csv('raw_data/CountryCodes.csv', encoding = 'unicode_escape')
        countries.drop(columns=['Numeric'], inplace=True)
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
        EU_production_annual = EU_production.loc[EU_production['unit'] == 'GWH']
        EU_production_annual = EU_production_annual.loc[EU_production_annual['operator'] == 'TOTAL']
        EU_production_annual = EU_production_annual.loc[EU_production_annual['plants'] == 'TOTAL']
        EU_production_annual = EU_production_annual.loc[EU_production_annual['siec'] == 'TOTAL']
        
        return EU_production_annual

    # def EU_Total_Elec_production(self):
    #     #EU Annual Electricity Production
    #     EU_production_annual =  self.EU_production_annual()
    #     EU_production_annual[self.columns]= EU_production_annual[self.columns].apply(pd.to_numeric, errors = 'coerce')
    #     EU_Total_Elec_production = EU_production_annual.groupby('nrg_bal').sum()
    #     EU_Total_Elec_production = EU_Total_Elec_production.reset_index(inplace=True)
    #     return EU_Total_Elec_production
    
    def EU_Total_Elec_nrg_bal(self):
        EU_production_annual =  self.EU_production_annual()
        EU_production_annual[self.columns]= EU_production_annual[self.columns].apply(pd.to_numeric, errors = 'coerce')
        EU_Total_Elec_nrg_bal = EU_production_annual.groupby('nrg_bal').sum()
        return EU_Total_Elec_nrg_bal
            
    def EU_GEP_pred(self):
        '''Predicting EU Electricity production upto 2030 using FB prophet'''
        EU_Total_Elec_nrg_bal =  self.EU_Total_Elec_nrg_bal()
        df_GEP = EU_Total_Elec_nrg_bal.loc[EU_Total_Elec_nrg_bal['nrg_bal']== 'GEP']
        GEP_data = pd.DataFrame(df_GEP[self.columns].sum(numeric_only=True, axis=0))
        os.chdir('/Users/pratimas/code/SinanSeyhan/green-electricity-project')
        trainer = importlib.import_module("green-electricity-project.trainer", package=True).Trainer()
        train, test = trainer.split(GEP_data, year='2018')
        model = trainer.initialize_model()
        model.fit(train)
        pred = trainer.predict(horizon=13)[['ds', 'yhat']]   
        return pred, train
        
    def EU_Elec_mix_2030(self):
        '''Target EU Energy Mix in Electricity production upto 2030'''
        EU_Elec_mix_2030 = pd.read_csv('raw_data/Electricity_mix_2030.csv', encoding = 'unicode_escape')
        pred = self.pred()
        used_pred = pred.iloc[25:41]
        final_mix = EU_Elec_mix_2030.mul(used_pred.yhat);
        return final_mix
          
    def GEP_pred_vs_Actual(self):
        pred =  self.pred()
        train = self.train()
        fig = px.line(pred, x=pred.ds, y=pred.yhat, labels={
                     'ds': 'Years',
                     'yhat': 'GEP in TWh'
                 },title="EU GEP Actual vs Prediction")
        fig.add_trace(go.Scatter(x = pred.ds, y = train.y, showlegend=False))
        return fig
    
    def Elec_Mix_chart(self):
        chart_data = self.final_mix()
        st.area_chart(chart_data)

    def Germany_analysis(self):
        '''Electricity Production analysis by country (example: Germany)'''
        Elec_production_germany = EU_production_annual[EU_production_annual['Alpha_2_code'] == 'DE']
        Gross_Net_Elec_Prod_Germany = Elec_production_germany.groupby(Elec_production_germany['nrg_bal']).sum()
        return Gross_Net_Elec_Prod_Germany
    
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
