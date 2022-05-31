# For all utilization functions
import pandas as pd
import plotly.express as px
import seaborn as sns

class Plot():
    def __init__(self):
        pass
    def plotly(self):

        data = sns.load_dataset('tips')
        tips = px.data.tips()
        fig = px.scatter(tips, x="total_bill", y="tip", size="size", color="smoker")
        fig.show()

class DemocracyIndex():
    def __init__(self):
        pass

    def get_democracy_index(self):
        '''
        Gives the democracy index of the countries.
        Data taken from: https://en.wikipedia.org/wiki/Democracy_Index
        Country: Name of the country

        Regime Type: Type of democracy in the country

        EU?: Whether the country is in EU27
        '''

        pd.set_option('mode.chained_assignment', None)
        DEMOCRACY_INDEX_PATH = '../raw_data/Democracy_Index.csv'
        df = pd.read_csv(DEMOCRACY_INDEX_PATH)

        return df

    def get_eu_democracy_index(self):
        '''
        Gives the democracy index of the 27 EU countries.
        Data taken from: https://en.wikipedia.org/wiki/Democracy_Index
        Country: Name of the country

        Regime Type: Type of democracy in the country
        '''

        temp = DemocracyIndex().get_democracy_index()
        df_eu = temp[temp['EU?']==True]
        df_eu.drop(columns=['EU?'], axis=1, inplace=True)

        return df_eu
