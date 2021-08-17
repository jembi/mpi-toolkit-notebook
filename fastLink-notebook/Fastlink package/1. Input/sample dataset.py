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

# 2.2) Select desired datafile
def sample_dataset():

    df = pd.read_csv("https://raw.githubusercontent.com/jembi/mpi-toolkit-notebook/main/fastLink-notebook/data-200-100.csv")
    df.to_csv('sample_dataset.csv', index=False)
    print("Using sample dataset: 200 original, 100 duplicates")
    file = 'sample_dataset.csv'
    return file
