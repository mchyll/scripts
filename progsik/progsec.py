import pickle
import base64

cookie = base64.b64decode('gANdcQAoWAYAAABtY2h5bGxxAVggAAAAYTUwZWRlYzkxNTY5YmY5MjQzNWU2OTdhYTEzYWRkZTRxAmUu')
# b%27gANdcQAoWAYAAABtY2h5bGxxAVggAAAAYTUwZWRlYzkxNTY5YmY5MjQzNWU2OTdhYTEzYWRkZTRxAmUu%27
print(pickle.loads(cookie))

