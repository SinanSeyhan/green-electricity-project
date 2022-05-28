# Python file to get the cleaned up version of Exports Database
import pandas as pd
import numpy as np

class Exports():
    def __init__(self):
        pass

    def get_exports(self):
        '''
        Load the complete export csv file.
        '''
        EXPORTS_PATH = '../raw_data/ElecExportsByPartnerCountry.csv'
        temp = pd.read_csv(EXPORTS_PATH)
        return temp

    def get_eu_exports(self):
        '''
        Function that gives the EU countries exports.
        '''
        COUNTRIES_PATH = '../raw_data/CountryCodes.csv'
        temp = Exports().get_exports()

        # 27 EU Countries
        EU_Countries = ['Belgium', 'Bulgaria', 'Czechia', 'Denmark', 'Germany', 'Estonia', 'Ireland',
                        'Greece', 'Spain', 'France', 'Croatia', 'Italy', 'Cyprus', 'Latvia', 'Lithuania',
                        'Luxembourg', 'Hungary', 'Malta', 'Netherlands (the)', 'Austria', 'Poland', 'Portugal',
                        'Romania', 'Slovenia', 'Slovakia', 'Finland', 'Sweden']

        countries = pd.read_csv(COUNTRIES_PATH, encoding = 'unicode_escape')
        countries.rename({'Alpha_2_code':'partner'}, axis=1, inplace=True)
        countries.drop(columns=['Numeric'], axis=1, inplace=True)
        countries.dropna(inplace=True)

        # Filtering for Electricity
        exports = temp[temp['siec']=='E7000']

        # Merging with countries DataFrame for partner country
        exports = exports.merge(countries, on='partner', how='left')
        exports.drop(columns=['Alpha_3_code'], axis=1, inplace=True)
        exports.rename({'Country': 'partner_country'}, axis=1, inplace=True)
        exports = exports[['freq', 'siec', 'partner', 'partner_country', 'unit', 'Alpha_2_code',
                            '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
                            '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
                            '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                            '2017', '2018', '2019', '2020']]

        # Merging with countries DataFrame for country
        countries = pd.read_csv(COUNTRIES_PATH, encoding = 'unicode_escape')
        countries.drop(columns=['Numeric'], axis=1, inplace=True)
        countries.dropna(inplace=True)
        exports = exports.merge(countries, on='Alpha_2_code', how='left')
        exports.drop(columns=['Alpha_3_code', 'freq', 'siec'], axis=1, inplace=True)
        exports.rename({'Country': 'country'}, axis=1, inplace=True)
        exports = exports[['partner', 'partner_country', 'unit', 'country', 'Alpha_2_code',
                            '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
                            '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
                            '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                            '2017', '2018', '2019', '2020']]

        # Filtering EU Countries
        exports['EU?'] = exports['country'].isin(EU_Countries)
        exports = exports[['partner', 'partner_country', 'unit', 'Alpha_2_code', 'country', 'EU?',
                            '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
                            '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
                            '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
                            '2018', '2019', '2020', ]]

        exports = exports[exports['EU?']==True]

        # Downcasting the numerical values
        years = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
                '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
                '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                '2017', '2018', '2019', '2020']
        for year in years:
            exports[year] = pd.to_numeric(exports[year], errors='raise', downcast='float')

        return exports

    def get_total_exports(self):
        '''
        Gives total exports per country
        '''
        exports = Exports().get_exports()
        exports_grouped = exports.groupby(by='country').sum()
        return exports_grouped
