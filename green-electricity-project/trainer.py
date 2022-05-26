# For initialzing the models
from posixpath import split
import re
import pandas as pd
import matplotlib.pyplot as plt

from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from sklearn.metrics import coverage_error



class Trainer():
    '''
    Class for ML model: Prophet
    '''
    def __init__(self):
        self.model = None

    def preproc(self, data):
        '''
        Data preprocessing for the prophet
        '''
        df = data
        df.reset_index(inplace=True)
        df.rename(columns={'index':'ds', 0: 'y'}, inplace=True)
        df['ds'] = pd.to_datetime(df['ds'], format='%Y') + pd.to_timedelta(364, unit='D')

        # Train test split:
        split = int(len(df)*0.7)

        self.train = df.iloc[:split]
        self.test = df.iloc[split:]

        return self.train, self.test


    def initialize_model(self):
        '''
        Function to initialize the Prophet model
        '''
        self.model = Prophet(seasonality_mode='multiplicative',
                            yearly_seasonality=True,
                            weekly_seasonality=False,
                            daily_seasonality=False,
                            interval_width=0.95)
        return self.model

    def fit(self, train):
        '''
        Function to train the model on a train dataset
        '''
        self.model = Trainer().initialize_model()
        self.model.fit(train)

    def predict(self, horizon=16):
        '''
        Prediction function
        '''
        future = self.model.make_future_dataframe(periods=horizon, freq='Y')
        forecast = self.model.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

        return forecast

    def cross_validate(self):
        '''
        Cross validating the model
        '''
        cv_results = cross_validation(model=model, initial=f'{365 * 20} days', horizon='365 days', period='180 days')
        df_performance = performance_metrics(cv_results)
        return df_performance

    def plot_cross_validate(self):
        '''
        Plotting function for the cross validation
        '''
        cv_results = cross_validation(model=self.model, initial=f'{365 * 20} days', horizon='365 days', period='180 days')
        plot_cross_validation_metric(cv_results, metric='mape')


if __name__ == '__main__':
    model = Trainer().initialize_model
