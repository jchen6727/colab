from pubtk.runtk import SocketRunner
import os, sys, json

print(os.getpid())

runner = SocketRunner()

mappings = json.dumps(runner.mappings)

print(mappings)