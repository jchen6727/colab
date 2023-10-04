import pandas
import plotly
import plotly.express as px

def expanding_idxmin(df, col):
    curr = 0
    for i in range(len(df)):
        if df[col][i] < df[col][0:i].min():
            yield i
            curr = i
        else:
            yield curr

ALGOS = ["bayesopt", "blendsearch", "cfo", "optuna", "random"]

TARGET = { # targets and weights from cfg
    'loss': 0,
    'PYR': 3.33875,
    'BC': 19.725,
    'OLM': 3.47,
    'PYR->BC_AMPA' : 0.36e-3, "BC->BC_GABA"  : 4.5e-3 , "PYR->BC_NMDA" : 1.38e-3 ,
    'PYR->OLM_AMPA': 0.36e-3, "BC->PYR_GABA" : 0.72e-3, "PYR->OLM_NMDA": 0.7e-3  ,
    'PYR->PYR_AMPA': 0.02e-3, "OLM->PYR_GABA": 72e-3  , "PYR->PYR_NMDA": 0.004e-3,
}

rename = {
       'BC->BC_GABA',
       'BC->PYR_GABA',
       'OLM->PYR_GABA',
       'PYR->BC_AMPA',
       'PYR->BC_NMDA',
       'PYR->OLM_AMPA',
       'PYR->OLM_NMDA',
       'PYR->PYR_AMPA',
       'PYR->PYR_NMDA',
}

rename = { "config/netParams.connParams.{}.weight".format(n): n for n in rename}

def create_plots(algo):
    df = pandas.read_csv("{}250.csv".format(algo))
    try:
        df = df[TARGET.keys()]
    except:
        df.rename(rename, axis=1, inplace=True)
        df = df[TARGET.keys()]

    for param in TARGET.keys():
        df['BEST_{}'.format(param)] = df[param][expanding_idxmin(df, 'loss')].reset_index(drop=True)
    deltas = df[df['BEST_loss'].diff() != 0].index.tolist()
    for param in TARGET.keys():
        fig = px.scatter(df, x=df.index, y=param)
        best_str = "BEST_{}".format(param)
        fig.add_scatter(x=df.index, y=df[best_str], mode='lines', name=best_str)
        for delta in deltas:
            fig.add_vline(delta)
        fig.add_hline(TARGET[param])
        fig.write_html("plots/{}__{}.html".format(algo, param))

"""
for algo in ALGOS:
    create_plots(algo)
"""

create_plots("random")





