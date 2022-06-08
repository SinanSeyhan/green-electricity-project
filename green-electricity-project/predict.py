# for predicting data with trained models
import importlib
import pandas as pd


class Prediction():
    def __init__(self):
        global EU_Countries
        EU_Countries = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL',
                        'ES', 'FI', 'FR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU',
                        'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']

    def validate_EU_countries(self):
        trainer_module = importlib.import_module("green-electricity-project.trainer", package=True).Trainer()
        consumption_module = importlib.import_module("green-electricity-project.consumption", package=True).Consumption()
        df = consumption_module.get_consumption()
        temp = df[df['energy_balance']=='Finalconsumption-transportsector-energyuse']
        pred = {}

        eu_df = pd.DataFrame(temp.groupby('Alpha_2_code').sum().sum())
        split = trainer_module.split(eu_df, year='2018')[0]
        model = trainer_module.initialize_model()
        model.fit(split)
        pred['EU'] = trainer_module.predict(horizon=13)[['ds', 'yhat']]

        for country in EU_Countries:

            data = temp[temp['Alpha_2_code']==country].loc[:, '1990':'2020'].T
            data.rename({data.columns[0]: 0}, axis=1, inplace=True)

            split = trainer_module.split(data, year='2018')[0]
            model = trainer_module.initialize_model()
            model.fit(split)
            pred[country] = trainer_module.predict(horizon=13)[['ds', 'yhat']]

        #result = pd.DataFrame.from_dict(pred, columns=pred.keys())

        return pred


if __name__=='__main__':
    print(Prediction().validate_EU_countries())
