# # pandas and numpy for data management
# import pandas as pd
# import numpy as np

# bokeh libraries
from bokeh.io import curdoc
from bokeh.models import Tabs

from scripts.dynamic_model import dynamic_model_tab

tab_water_tank = dynamic_model_tab()
tabs = Tabs(tabs = [tab_water_tank])

# Put the tabs in the current document for display
curdoc().add_root(tabs)