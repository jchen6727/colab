from netpyne.batchtools.search import ray_search

from netpyne.batchtools import runtk

from ray import tune

params = {'synMechTau2': tune.grid_search([3.0, 5.0, 7.0]), # must sample each element from this list
          'connWeight' : tune.choice([0.005, 0.01, 0.15])} #randomly sampled from this list

batch_config = {'command': 'python init.py'}

Dispatcher = runtk.dispatchers.INETDispatcher
Submit = runtk.submits.ZSHSubmitSOCK

ray_search(dispatcher_constructor = Dispatcher,
           submit_constructor=Submit,
           params = params,
           batch_config = batch_config,
           concurrency = 6,
           output_path = '../batch_rand',
           checkpoint_path = '../rand',
           label = 'rand_search',
           num_samples = 2)


"""
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│ Trial name        status         connWeight     synMechTau2     iter     total time (s) │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ run_fa6b2_00000   TERMINATED          0.01                3        1            1.82939 │
│ run_fa6b2_00001   TERMINATED          0.15                5        1            1.83799 │
│ run_fa6b2_00002   TERMINATED          0.005               7        1            1.82532 │
│ run_fa6b2_00003   TERMINATED          0.005               3        1            1.78317 │
│ run_fa6b2_00004   TERMINATED          0.005               5        1            1.83142 │
│ run_fa6b2_00005   TERMINATED          0.005               7        1            1.83018 │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
"""