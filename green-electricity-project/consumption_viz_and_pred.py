import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import widgets
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import importlib
import streamlit as st

#os.chdir('/home/armin/code/SinanSeyhan/green-electricity-project')
consumption_module = importlib.import_module(
    "green-electricity-project.consumption", package=True)
trainer_module = importlib.import_module("green-electricity-project.trainer",
                                         package=True)

class ConsumptionVaP():
    def __init__(self, country = 'EU') -> None:
        self.country = country

    def get_consumption_data(self):
        consumption = consumption_module.Consumption(country=[self.country])
        consumption_data = consumption.prepare_consumption_and_export()
        self.consumption_data = consumption_data

        return consumption_data

    def show_historic_consumption(self, content = 'all'):
        if content == 'top5':
            self.fig = px.line(self.consumption_data.sort_values('2019', ascending=False).head(5).T, height=1000, labels={
                     "index": "Year",
                     "value": "GWh"})
        elif content == 'all':
            self.fig = px.line(self.consumption_data.sort_values(
                '2019', ascending=False).T,
                               height=1000,
                               labels={
                                   "index": "Year",
                                   "value": "GWh"
                               })
        elif content == 'sum':
            self.fig = px.line(pd.DataFrame(self.consumption_data.sum().T),
                               height=1000,
                               labels={
                                   "index": "Year",
                                   "value": "GWh"
                               })

        self.fig.update_layout(hoverlabel_namelength=-1,
            legend=dict(yanchor="top", x=0, xanchor="left", y=-0.2, title='Consumption Category'))

        #self.fig.show()

    def predict_future_consumption(self, info=None):
        self.trainer_list = []
        self.forecast_list = []

        bar = st.progress(0)
        for i in range(self.consumption_data.shape[0]):
            if info is not None:
                info.write(f'Predicting consumption of {self.consumption_data.index[i]}')

            self.trainer_list.append(trainer_module.Trainer())

            self.consumption_data_preproc = pd.DataFrame(self.consumption_data.iloc[i])
            self.consumption_data_preproc.columns = [0]

            self.consumption_data_preproc = self.trainer_list[i].split(self.consumption_data_preproc, '2019')

            self.trainer_list[i].fit(self.trainer_list[i].train)
            self.forecast_list.append(self.trainer_list[i].predict())

            bar.progress((i+1) / self.consumption_data.shape[0])

        self.get_total_future_consumption()

        if info is not None:
            info.write('Predictions successfull!')
        return self.forecast_list

    def get_total_future_consumption(self):
        total_future_consumption = []
        for i in self.forecast_list[0]['yhat'].index:
            total_cons_list = []
            for j in self.forecast_list:
                total_cons_list.append(j['yhat'][i])
            total_future_consumption.append(sum(total_cons_list))

        self.total_future_consumption = total_future_consumption

        return total_future_consumption

    def show_future_consumption(self):
        self.fig_pred = go.Figure()
        # self.fig_pred.add_traces(
        #     go.Scatter(x=self.forecast['ds'],
        #                y = self.forecast['yhat_upper'],
        #                line = dict(color='rgb(0,0,255,0)'),
        #                showlegend=False,
        #                name='Upper bundary'))

        # self.fig_pred.add_traces(
        #     go.Scatter(x=self.forecast['ds'],
        #                y=self.forecast['yhat_lower'],
        #                line=dict(color='rgb(0,0,255,0)'),
        #                fill='tonexty',
        #                showlegend=False,
        #                name='Lower bundary'))

        self.fig_pred.add_trace(
            go.Scatter(x=list(self.forecast_list[0]['ds']),
                       y=list(self.total_future_consumption),
                       line=dict(color='rgb(255,150,150)'),
                       showlegend=False,
                       name=f'Prediction TOTAL'))

        self.fig_pred.add_trace(
            go.Scatter(x=list(
                self.forecast_list[0].ds[:self.consumption_data.shape[1]]),
                       y=list(self.consumption_data.sum().values),
                       line=dict(color='rgb(255,0,0)'),
                       showlegend=False,
                       name=f'Real TOTAL'))

        for i in range(len(self.consumption_data.index)):
            cat = self.consumption_data.index[i]

            self.fig_pred.add_trace(
                go.Scatter(x=list(self.forecast_list[i]['ds']),
                        y=list(self.forecast_list[i]['yhat']),
                        line=dict(color='rgb(255,150,150)'),
                        showlegend=False, name=f'Prediction {cat}', visible=False))

            self.fig_pred.add_trace(
                go.Scatter(x=list(
                    self.forecast_list[0].ds[:self.consumption_data.shape[1]]),
                           y=list(self.consumption_data.loc[cat].values),
                           line=dict(color='rgb(255,0,0)'),
                           showlegend=False,
                           name=f'Real {cat}',
                           visible=False))


        self.fig_pred.update_yaxes(rangemode = 'nonnegative')

        cats_doubled = [val for val in self.consumption_data.index for _ in (0, 1)]
        cats_doubled.insert(0, 'TOTAL')
        cats_doubled.insert(0, 'TOTAL')

        list_cat = []
        for i in range(len(cats_doubled)):
            if i%2 == 0:
                visible_ind = [False] * len(cats_doubled)
                visible_ind[i] = True
                visible_ind[i+1] = True

                list_cat.append(
                    dict(label=cats_doubled[i],
                        method='update',
                        args=[{
                            'visible': visible_ind
                        }, {
                            'title': cats_doubled[i],
                            'showlegend': True
                        }]))


        self.fig_pred.update_layout(
            hoverlabel_namelength=-1,
            updatemenus=[go.layout.Updatemenu(active=0, buttons=list_cat)],
            width=800,
            height=600,
        )

        self.fig_pred.update_layout(updatemenus=[dict(font = {'color': 'rgb(0,255,127)'}, x=0.1, xanchor="left", y=1.1, yanchor="top")])

        #self.fig_pred.show()

    def run_viz_and_pred(self, info=None):
        self.get_consumption_data()
        self.show_historic_consumption()
        self.predict_future_consumption(info)
        self.show_future_consumption()


if __name__ == "__main__":
    consumption_eu = ConsumptionVaP('EU')
    consumption_eu.run_viz_and_pred()
