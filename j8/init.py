from netpyne.batchtools import specs
from netpyne.batchtools import comm
from netpyne import sim
from netParams import netParams, cfg
import json

comm.initialize()

sim.createSimulate(netParams=netParams,
                          simConfig=cfg)

#comm.pc.barrier()
#sim.gatherData()
if comm.is_host():
    results = sim.analysis.popAvgRates(show=False)

#inputs = specs.get_mappings()
#out_json = json.dumps({**inputs, **rates})

    results['PYR_loss'] = (results['PYR'] - 3.33875)**2
    results['BC_loss']  = (results['BC']  - 19.725 )**2
    results['OLM_loss'] = (results['OLM'] - 3.470  )**2
    out_json = json.dumps(results)

    print(out_json)
    print(comm.is_host())
#TODO put all of this in a single function.
    comm.send(out_json)
    comm.close()
