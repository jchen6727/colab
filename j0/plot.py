import pandas
import plotly.express as px
#import dash

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default='bopt/b011.csv')

args, call= parser.parse_known_args()
args= dict(args._get_kwargs())
df = pandas.read_csv(args['file'])

df['min_loss'] = df['loss'].expanding().min()

actual = { # weights from cfg, AMPA, GABA, NMDA
    'PYR->BC_AMPA' : 0.36e-3, "BC->BC_GABA"  : 4.5e-3 , "PYR->BC_NMDA" : 1.38e-3 ,
    'PYR->OLM_AMPA': 0.36e-3, "BC->PYR_GABA" : 0.72e-3, "PYR->OLM_NMDA": 0.7e-3  ,
    'PYR->PYR_AMPA': 0.02e-3, "OLM->PYR_GABA": 72e-3  , "PYR->PYR_NMDA": 0.004e-3,
}

rename = {
       'config/netParams.connParams.BC->BC_GABA.weight',
       'config/netParams.connParams.BC->PYR_GABA.weight',
       'config/netParams.connParams.OLM->PYR_GABA.weight',
       'config/netParams.connParams.PYR->BC_AMPA.weight',
       'config/netParams.connParams.PYR->BC_NMDA.weight',
       'config/netParams.connParams.PYR->OLM_AMPA.weight',
       'config/netParams.connParams.PYR->OLM_NMDA.weight',
       'config/netParams.connParams.PYR->PYR_AMPA.weight',
       'config/netParams.connParams.PYR->PYR_NMDA.weight',
}

rename = { n: n.split('.')[2] for n in rename if n in df.columns}

params = rename.values()

df.rename(rename, axis=1, inplace=True)

def expanding_idxmin(df, col):
    curr = 0
    for i in range(len(df)):
        if df[col][i] < df[col][0:i].min():
            yield i
            curr = i
        else:
            yield curr

for param in params:
    df['MIN_{}'.format(param)] = df[param][expanding_idxmin(df, 'loss')].reset_index(drop=True)

for param in ['PYR', 'BC', 'OLM']:
    df['MIN_{}'.format(param)] = df[param][expanding_idxmin(df, 'loss')].reset_index(drop=True)


fig = px.scatter(df, x=df.index, y='loss')

fig.add_scatter(x=df.index, y=df['min_loss'], mode='lines', name='min_loss')

fig.show()