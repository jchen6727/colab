from netpyne.batchtools import specs
from netpyne.batchtools import comm
from netpyne import sim
from cfg import cfg
from netParams import netParams
import json


sim.createSimulateAnalyze(netParams=netParams,
                          simConfig=cfg)

rates = sim.analysis.popAvgRates(show=False)

#inputs = specs.get_mappings()
#out_json = json.dumps({**inputs, **rates})

out_json = json.dumps(rates)

#TODO put all of this in a single function.
comm.initialize()
comm.send(out_json)
comm.close()


