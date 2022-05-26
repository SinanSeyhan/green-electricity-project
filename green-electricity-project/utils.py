# For all utilization functions

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
