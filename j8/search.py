from netpyne.batchtools.search import ray_search

from netpyne.batchtools import runtk

from ray import tune

params = {'nmda.PYR->BC' : tune.grid_search([0]),
          'nmda.PYR->OLM': tune.grid_search([0]),
          'nmda.PYR->PYR': tune.grid_search([0]),
          'ampa.PYR->BC' : tune.grid_search([0]),
          'ampa.PYR->OLM': tune.grid_search([0]),
          'ampa.PYR->PYR': tune.grid_search([0]),
          'gaba.BC->BC'  : tune.grid_search([0]),
          'gaba.BC->PYR' : tune.grid_search([0]),
          'gaba.OLM->PYR': tune.grid_search([0])}

batch_config = {'command': 'mpiexec -np 4 nrniv -python -mpi init.py'}

Dispatcher = runtk.dispatchers.INETDispatcher
Submit = runtk.submits.SHSubmitSOCK

ray_search(dispatcher_constructor = Dispatcher,
           submit_constructor=Submit,
           label = 'search',
           params = params,
           output_path = '../batch',
           checkpoint_path = '../ray',
           batch_config = batch_config,
           num_samples = 1,
           metric = 'loss',
           mode = 'min',
           algorithm = "variant_generator",
           max_concurrent = 1)