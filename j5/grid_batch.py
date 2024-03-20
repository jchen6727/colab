from netpyne.batchtools.search import ray_search

from netpyne.batchtools import runtk

from ray import tune#TODO remove

params = {'synMechTau2': tune.grid_search([3.0, 5.0, 7.0]), #TODO default? grid search?
          'connWeight' : tune.grid_search([0.005, 0.01, 0.15])} #LB, UP


batch_config = {'command': 'python init.py'}

Dispatcher = runtk.dispatchers.INETDispatcher
Submit = runtk.submits.ZSHSubmitSOCK

ray_search(dispatcher_constructor = runtk.dispatchers.INETDispatcher,
           submit_constructor=runtk.dispatchers.ZSHSubmitSOCK,
           params = params,
           batch_config = batch_config,
           algorithm = "variant_generator",
           concurrency = 9,
           output_path = '../batch',
           checkpoint_path = '../grid',
           label = 'grid_search')


"""
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ Trial name        status         synMechTau2     connWeight     iter     total time (s) │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ run_22d01_00000   TERMINATED               3          0.005        1            2.2493  │
│ run_22d01_00001   TERMINATED               3          0.01         1            2.30802 │
│ run_22d01_00002   TERMINATED               3          0.15         1            2.25716 │
│ run_22d01_00003   TERMINATED               5          0.005        1            2.26481 │
│ run_22d01_00004   TERMINATED               5          0.01         1            2.2588  │
│ run_22d01_00005   TERMINATED               5          0.15         1            2.247   │
│ run_22d01_00006   TERMINATED               7          0.005        1            2.26577 │
│ run_22d01_00007   TERMINATED               7          0.01         1            2.26621 │
│ run_22d01_00008   TERMINATED               7          0.15         1            2.25301 │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
"""