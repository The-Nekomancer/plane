import pySldWrap.sw_tools as sw_tools
from pathlib import Path

sw_tools.connect_sw("2023")  # open connection and pass Solidworks version
path = 'Port Wing Tip.SLDPRT'
# path = Path(path)  # a path object can also be used for a number of functions
model = sw_tools.open_part(path)  # open the model, link is returned
# sw_tools.close(path)  # close the model

path = 'part.SLDPRT'
model = sw_tools.open_part(path)
# the part can be edited here
sw_tools.save_model(model)
sw_tools.close(path)