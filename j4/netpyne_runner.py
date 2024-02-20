import site
site.addsitedir('/content/drive/MyDrive/venv/lib/python3.10/site-packages')

from pubtk.runtk import NetpyneRunner

specs = NetpyneRunner()

cfg = specs.get_SimConfig()

cfg.duration = 1*1e3
cfg.dt = 0.025

specs.set_mappings('cfg')

timesteps = cfg.duration / cfg.dt