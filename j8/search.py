from netpyne.batchtools.search import ray_search
from netpyne.batchtools import submits
from netpyne.batchtools import dispatchers
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

# use batch_shell_config if running directly on the machine
batch_shell_config = {'command': 'mpiexec -np 4 nrniv -python -mpi init.py',}

# use batch_sge_config if running on a
batch_sge_config = {
    'queue': 'cpu.q',
    'cores': 5,
    'vmem': '4G',
    'realtime': '00:30:00',
    'command': 'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py'}

batch_config = batch_shell_config

Dispatcher = dispatchers.INETDispatcher
Submit = submits.SHSubmitSOCK


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
           max_concurrent = 4)