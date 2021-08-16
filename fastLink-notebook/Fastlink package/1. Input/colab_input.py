from ipywidgets import Dropdown, Checkbox, Label, FloatRangeSlider

import pandas as pd
import os
from rpy2.robjects import globalenv
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as r_objects
import rpy2.robjects.packages as r_packages
r = r_objects.r

#Fastlink imports
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

# 2.1) Pick method of uploading csv file (Always)
def upload_method():

    menu_1 = Dropdown(options=['Upload from google drive', 'Upload local file', "Use sample dataset"])
    return menu_1


# 3) Capture User input (Always)
def user_input(col_names):

    style = {'description_width': 'initial'}
    layout = {'width': '400px'}
    menu_1 = Dropdown(description="1. Choose your unique identifier:", style=style, options=col_names)

    check_b_label = Label(value="2. Choose desired fields to exclude:")

    check_b_list = []
    for i in range(len(col_names)):
        if col_names[i] == menu_1.value:
            check_b = Checkbox(value=True, description=col_names[i], disabled=False, indent=False)
        else:
            check_b = Checkbox(value=False, description=col_names[i], disabled=False, indent=False)
        check_b_list.append(check_b)

    menu_2 = Dropdown(layout=layout, description="3. Choose your string-distance method:", style=style, options=["Jaro-Winkler", "Jaro", "Levensthein"])

    slider_label = Label(value="4. Select upper and lower bounds:")

    slider_1 = FloatRangeSlider(
        value=[0.88, 0.94],
        min=0,
        max=1,
        step=0.01,
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
    )

    return menu_1, check_b_label, check_b_list, menu_2, slider_label, slider_1

