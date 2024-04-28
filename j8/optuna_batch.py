#from pubtk.raytk.search import ray_optuna_search #the one that allows for multiobjective optimization
from netpyne.batchtools.search import ray_optuna_search #the one that allows for multiobjective optimization
from netpyne.batchtools import runtk

from ray import tune

params = {'nmda.PYR->BC' : tune.grid_search([0, 1]),
          'nmda.PYR->OLM': tune.grid_search([0]),
          'nmda.PYR->PYR': tune.grid_search([0]),
          'ampa.PYR->BC' : tune.grid_search([0]),
          'ampa.PYR->OLM': tune.grid_search([0, 1]),
          'ampa.PYR->PYR': tune.grid_search([0]),
          'gaba.BC->BC'  : tune.grid_search([0]),
          'gaba.BC->PYR' : tune.grid_search([0]),
          'gaba.OLM->PYR': tune.grid_search([0, 1])}
params = {'synMechTau2': tune.uniform(3.0, 7.0), # LB
          'connWeight' : tune.uniform(0.005, 0.15)} #UB

batch_config = {'command': 'python init.py',
                'cores': '2',
                'vmem': '16G',
                }

Dispatcher = runtk.dispatchers.INETDispatcher
Submit = runtk.submits.SGESubmitSOCK

ray_study = ray_optuna_search(dispatcher_constructor = Dispatcher,
                  submit_constructor=Submit,
                  params = params,
                  batch_config = batch_config,
                  max_concurrent = 3,
                  output_path = '../batch_optuna',
                  checkpoint_path = '../optuna',
                  label = 'optuna_search',
                  num_samples = 15,
                  metric = ['S_loss', 'M_loss'],
                  mode = ['min', 'min'])

S = ray_study.results.get_best_result('S_loss', 'min')
M = ray_study.results.get_best_result('M_loss', 'min')

study = ray_study.algo.searcher._ot_study #can call optuna vis on this.
