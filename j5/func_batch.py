from netpyne.batchtools.search import ray_search

from netpyne.batchtools import runtk
import numpy

from ray import tune

params = {'synMechTau2': tune.grid_search([3.0, 5.0, 7.0]), #TODO wrapper for grid_search, sample_from, linspace?
          'connWeight' : tune.sample_from(lambda _: numpy.random.uniform(0.005, 0.15))}

batch_config = {'sge': 5, 'command': 'python init.py'}
#TODO what to do with config. consolidate it with other arguments to search?
Dispatcher = runtk.dispatchers.INETDispatcher #TODO either allow passage of a constructor or use a string
Submit = runtk.submits.ZSHSubmitSOCK

#TODO rename ray_search to search
ray_search(dispatcher_constructor = Dispatcher, #TODO pass in a run_config?
           submit_constructor=Submit,
           params = params,
           batch_config = batch_config, #
           algorithm = "variant_generator",
           concurrency = 9,
           output_path = '../batch_func',
           checkpoint_path = '../grid_func',
           label = 'func_search',
           num_samples = 3)

#TODO something like this?
"""
run_config = {´dispatcher´: ´inet´, ´submit´: ´socket´, ´command´: ´python init´}
params = {'synMechTau2': [3.0, 5.0, 7.0], # assumes list of values by default if grid search-like algo
		  #'synMechTau2': [3.0, 7.0], # assumes lower/upper bounds by default if evol-like algo
          'connWeight' : paramtypes.sample_from(lambda _: numpy.random.uniform(0.005, 0.15))} # can optionally pass any of the paramtypes (= ray.tune data types)




"""

