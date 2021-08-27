import pandas as pd
import os
import time

# Import rpy2 packages
from rpy2.robjects import globalenv
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as r_objects
import rpy2.robjects.packages as r_packages
r = r_objects.r

from ipywidgets import Dropdown, FloatSlider, Text, GridBox, Checkbox, Label, FloatRangeSlider

import matplotlib.pyplot as plt
from google.colab import auth
import gspread
from oauth2client.client import GoogleCredentials
run_count = 1

# Fastlink imports
utils = r_packages.importr('utils')
utils.chooseCRANmirror(ind=1)
pack_names = ('fastLink', 'tictoc', 'strex', 'data.table', 'csv')
names_to_install = [x for x in pack_names if not r_packages.isinstalled(x)]
if len(names_to_install) > 0:
    utils.install_packages(StrVector(names_to_install))
base = r_packages.importr('base')
stats = r_packages.importr('stats')
fastLink = r_packages.importr('fastLink')
strex = r_packages.importr('strex')
data_table = r_packages.importr('data.table')
stringr = r_packages.importr('stringr')

def touch():
    pass
