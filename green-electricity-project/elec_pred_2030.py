import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

path = '../raw_data/Electricity_Mix_2030.csv'

class EuElecMixPrediction():

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