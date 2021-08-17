from ipywidgets import Text
import pandas as pd
import os
from rpy2.robjects import globalenv
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as r_objects
r = r_objects.r

# 2.2) Select desired datafile
def upload_google_drive():

    style = {'description_width': 'initial'}
    layout = {'width': '400px'}
    file_name = Text(
        style=style,
        layout=layout,
        value='data-50-25.csv',
        description='Enter file name:',
        disabled=False)
    folder_name = Text(
        style=style,
        layout=layout,
        value='/content/drive/MyDrive/Data Generator/',
        description='Enter folder directory:',
        disabled=False)
    return file_name, folder_name
