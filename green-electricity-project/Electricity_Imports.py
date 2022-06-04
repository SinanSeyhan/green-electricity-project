# Python file to get the cleaned up version of Exports Database


import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from matplotlib import pyplot as plt
import os

class Imports():
    def __init__(self):
        pass

    def overall_imports(self):
        '''
        Load the modified imports xlsx file
        '''
        pd.set_option('mode.chained_assignment', None)
        my_path = os.path.abspath(os.path.dirname(__file__))
        s_subtotals = os.path.join(my_path, '../raw_data/s_subtotals.xlsx')
        Overall_Pivot_Percent = pd.read_excel(s_subtotals, sheet_name='Overall_Pivot_Percent', header=0)

        # Change years datatypes to floats
        years=['Total_1991', 'Total_1992',
        'Total_1993', 'Total_1994', 'Total_1995', 'Total_1996', 'Total_1997',
        'Total_1998', 'Total_1999', 'Total_2000', 'Total_2001', 'Total_2002',
        'Total_2003', 'Total_2004', 'Total_2005', 'Total_2006', 'Total_2007',
        'Total_2008', 'Total_2009', 'Total_2010', 'Total_2011', 'Total_2012',
        'Total_2013', 'Total_2014', 'Total_2015', 'Total_2016', 'Total_2017',
        'Total_2018', 'Total_2019', 'Total_2020', 'Total_Total_']

        for year in years:
            Overall_Pivot_Percent[year]=pd.to_numeric(Overall_Pivot_Percent[year], errors='raise', downcast='float')

        # Filter out totals
        Overall_Percent_Country = Overall_Pivot_Percent[Overall_Pivot_Percent['EU_Partner'].str.contains('Total', case=False, na=False).any(level=0)]

        col_values = ['TRUE', 'FALSE']
        Overall_Percent_Country = Overall_Percent_Country[Overall_Percent_Country['Partner_EU'].str.contains('|'.join(col_values), case=False, na=False).any(level=0)]

        return Overall_Percent_Country

    def get_democracy(self):
        '''
        Function that gives the democracy index
        '''
        my_path = os.path.abspath(os.path.dirname(__file__))
        DEMOCRACY_INDEX_PATH = os.path.join(my_path, '../raw_data/Democracy_Index.csv')
        democracy = pd.read_csv(DEMOCRACY_INDEX_PATH)
        democracy.dropna(inplace=True)

        # remove unnecessary columns
        democracy = democracy.drop(columns=['EU?'])

        # rename columns to match import file
        democracy = democracy.rename(columns={'Country': 'Partner_country', 'Regime type': 'Regime_type'})

        # rename Partner country names to match import file
        democracy['Partner_country'].replace({'Netherlands': 'Netherlands (the)',
                              'North Macedonia': 'Republic of North Macedonia',
                              'Russia': 'Russian Federation (the)',
                              'Moldova': 'Moldova (the Republic of)'}, inplace=True)
        return democracy

    def get_overall_partners(self):
        '''
        Load the overall import partners xlsx file
        '''
        pd.set_option('mode.chained_assignment', None)
        my_path = os.path.abspath(os.path.dirname(__file__))
        s_subtotals = os.path.join(my_path, '../raw_data/s_subtotals.xlsx')
        Partners_Pivot_Percent = pd.read_excel(s_subtotals, sheet_name='Partners_Pivot_Percent', header=0)
        Partners_Pivot_Percent['Partner_country'] = Partners_Pivot_Percent['Partner_country'].str.replace(' Total', '')

        return Partners_Pivot_Percent

    def democracy_merge(self):
        '''
        Merge Partners file with Democracy index
        '''
        democracy = self.get_democracy()
        Partners_Pivot_Percent = self.get_overall_partners()
        Partners_Overall = Partners_Pivot_Percent.merge(democracy, on='Partner_country', how='left')
        Partners_Overall = Partners_Overall[Partners_Overall['Country']=='']

        # Filter to return only non-EU partner countries
        Partners_Non_EU = Partners_Overall[Partners_Overall['Partner_EU']=='FALSE']

        # clean up column names
        Partners_Non_EU.columns = Partners_Non_EU.columns.str.strip('Total_')

        # remove unnecessary columns
        Partners_Non_EU = Partners_Non_EU[['Partner_country', 'Regime_type', '1990', '1991', '1992',
       '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001',
       '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
       '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
       '2020']]

        # Melt df for visualization
        Partners_Non_EU_mod = Partners_Non_EU.melt(id_vars=['Partner_country', 'Regime_type'],
                                                   value_vars=['1990', '1991', '1992', '1993', '1994', '1995',
                                                       '1996', '1997', '1998', '1999', '2000', '2001',
                                                       '2002', '2003', '2004', '2005', '2006', '2007',
                                                       '2008', '2009', '2010', '2011', '2012', '2013',
                                                       '2014', '2015', '2016', '2017', '2018', '2019',
                                                       '2020'])

        # rename columns
        Partners_Non_EU_mod = Partners_Non_EU_mod.rename(columns={'variable': 'Year', 'value': 'Percent_total_imports'})

        # Convert values to percentages
        Partners_Non_EU_mod['Overall_Percent_Imports'] = (Partners_Non_EU_mod.Percent_total_imports * 100).astype(str)+'%'

        # Rearrange columns
        Partners_Non_EU_mod_type = Partners_Non_EU_mod[['Year', 'Regime_type', 'Partner_country', 'Percent_total_imports']]

        # Finalize df setup for visualization
        Partners_NonEU_pivot = pd.pivot_table(Partners_Non_EU_mod_type, values = 'Percent_total_imports', index = ['Year', 'Regime_type']).reset_index()

        return Partners_NonEU_pivot


    def EU_visualize(self):
        Overall_Percent_Country = self.overall_imports()

        # Create df showing only EU countries
        Overall_true = Overall_Percent_Country[Overall_Percent_Country['Partner_EU']=='TRUE Total'].rename(columns={'Partner_EU': 'EU Member'})

        # Create df showing only EU countries for 2020
        Overall_true_2020 = Overall_true[['Country', 'Total_2020']]

        # Create df showing only non-EU countries
        Overall_false = Overall_Percent_Country[Overall_Percent_Country['Partner_EU']=='FALSE Total'].rename(columns={'Partner_EU': 'Non EU Member'})

        # Create df showing only non-EU countries for 2020
        Overall_false_2020 = Overall_false[['Country', 'Total_2020']]

        # Create new column to convert values in EU df to percentages
        Overall_true_2020['Total_2020_Percentage'] = (Overall_true_2020.Total_2020 * 100).astype(str)+'%'
        Overall_true_2020 = Overall_true_2020.sort_values(by=['Total_2020'], ascending=False)

        # Convert values in non-EU df to negative values then convert to percentages
        Overall_false_2020['Total_2020'] *= -1
        Overall_false_2020['Total_2020_Percentage'] = (Overall_false_2020.Total_2020 * 100).astype(str)+'%'
        Overall_false_2020=Overall_false_2020.sort_values(by=['Total_2020'], ascending=True)

        # Create bi-directional visualization
        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)

        # Plot for Non-EU Member partners
        fig.append_trace(go.Bar(x=Overall_false_2020.Total_2020, y=Overall_false_2020.Country,
                       orientation='h', showlegend=True,
                       text=Overall_false_2020.Total_2020_Percentage,
                       name='Non-EU Member Partner',
                       marker_color='red'), 1, 1)

        # Plot for EU Member partners
        fig.append_trace(go.Bar(x=Overall_true_2020.Total_2020, y=Overall_true_2020.Country,
                       orientation='h', showlegend=True,
                       text=Overall_true_2020.Total_2020_Percentage,
                       name='EU Member Partner',
                       marker_color='blue'), 1, 2)

        # show visualization
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, categoryorder='total ascending',
                         ticksuffix=' ', showline=False)

        fig.update_traces(hovertemplate=None)

        fig.update_layout(title='Where do EU countries import electricity from: 2020',
                          margin=dict(t=80, b=0, l=70, r=40),
                          hovermode="y unified",
                          xaxis_title=' ', yaxis_title=" ",
                          plot_bgcolor='beige', paper_bgcolor='white')

        fig.update_layout(autosize=False,
                          width=900,
                          height=800,)

        return fig

    def Democracy_visualize(self):
        Partners_NonEU_pivot = self.democracy_merge()

        fig = px.line(Partners_NonEU_pivot, x='Year', y='Percent_total_imports', color='Regime_type',
             title='Percentage of Overall Imports from Non-EU Partners')
        print(Partners_NonEU_pivot)
        return fig


if __name__ == '__main__':
    Imports().Democracy_visualize()
