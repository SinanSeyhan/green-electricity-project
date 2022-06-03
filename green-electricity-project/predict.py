# for predicting data with trained models
import importlib

from sqlalchemy import column


class Prediction():
    def __init__(self):
        global EU_Countries
        EU_Countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus',
                        'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France',
                        'Germany',
#'Greece',
'Hungary',
'Ireland',
'Italy',
'Latvia',
'Lithuania',
'Luxembourg',
'Malta',
'Netherlands',
'Poland',
'Portugal',
'Romania',
'Slovakia',
'Slovenia',
'Spain',
'Sweden']

    def validate_EU_countries(self):
        trainer_module = importlib.import_module("green-electricity-project.trainer", package=True).Trainer()
        consumption_module = importlib.import_module("green-electricity-project.consumption", package=True).Consumption()
        df = consumption_module.get_consumption()
        temp = df[df['energy_balance']=='Finalconsumption-transportsector-energyuse']
        pred = {}
        for country in EU_Countries:

            data = temp[temp['Country']==country].loc[:, '1990':'2020'].T
            data.rename({data.columns[0]: 0}, axis=1, inplace=True)
            preproc = trainer_module.preproc(data)
            print(country)
            print(preproc)
            # model = trainer_module.initialize_model()
            # model.fit(preproc)
            # pred[country] = trainer_module.predict(horizon=10)

        return pred


if __name__=='__main__':
    #print(Prediction().validate_EU_countries())
    consumption_module = importlib.import_module("green-electricity-project.consumption", package=True).Consumption()
    df = consumption_module.get_consumption()
    temp = df[df['energy_balance']=='Finalconsumption-transportsector-energyuse']
    data = temp[temp['Country']=='Greece']
    print(temp)
