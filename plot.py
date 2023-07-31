import pandas
import utils
import plotly.express as px
#import dash

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='bopt/o011.csv')

args, call= parser.parse_known_args()
args= dict(args._get_kwargs())
df = pandas.read_csv(args['input'])



filenames = ["batch_csv/out{}.csv".format(i) for i in range(11)]
df = pandas.concat(
    [pandas.read_csv(filename) for filename in filenames]
)
df = df.drop(['Unnamed: 0'], axis=1).reset_index(drop=True)








import utils
import ray
import pandas
import shutil
import os

import numpy
from ray import tune
from ray import air
from ray.air import session
from ray.tune.search.bayesopt import BayesOptSearch
from ray.tune.search import ConcurrencyLimiter

import argparse

## specify CLI to function
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--concurrency', default=1)
parser.add_argument('-d', '--div', nargs=3, type=float, default=[0.5, 1.5, 100])
parser.add_argument('-s', '--save', '-o', '--output', default="output/optuna")
parser.add_argument('-t', '--trials', default=100)
#parser.add_argument('-p', '--params', nargs='+', default=['PYR->BC_AMPA', 'PYR->OLM_AMPA', 'PYR->PYR_AMPA'])
parser.add_argument('-p', '--params', nargs='+', default=['Z'*80])
parser.add_argument('-g', '--greps', nargs='+', default=['Z'*80])

args, call= parser.parse_known_args()
args= dict(args._get_kwargs())

cwd = os.getcwd()
cmd_args = {
    'mpiexec': shutil.which('mpiexec'), 'cores': 4, 'nrniv': shutil.which('nrniv'),
    'python': shutil.which('python'), 'script': cwd + '/runner.py'
}

initial_params = { # weights from cfg, AMPA, GABA, NMDA
    'PYR->BC_AMPA' : 0.36e-3, "BC->BC_GABA"  : 4.5e-3 , "PYR->BC_NMDA" : 1.38e-3 ,
    'PYR->OLM_AMPA': 0.36e-3, "BC->PYR_GABA" : 0.72e-3, "PYR->OLM_NMDA": 0.7e-3  ,
    'PYR->PYR_AMPA': 0.02e-3, "OLM->PYR_GABA": 72e-3  , "PYR->PYR_NMDA": 0.004e-3,
}
