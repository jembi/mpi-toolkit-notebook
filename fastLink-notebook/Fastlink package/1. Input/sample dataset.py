import pandas as pd
import os
from rpy2.robjects import globalenv
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as r_objects
r = r_objects.r

# 2.2) Select desired datafile
def sample_dataset():

    df = pd.read_csv("https://raw.githubusercontent.com/jembi/mpi-toolkit-notebook/main/fastLink-notebook/data-200-100.csv")
    df.to_csv('sample_dataset.csv', index=False)
    print("Using sample dataset: 200 original, 100 duplicates")
    file = 'sample_dataset.csv'
    return file

# 2.3) Upload and read data
def read_dataset_other(file):

    file_flag = 0
    try:
        globalenv['csv'] = r['read.csv'](file, header=True, stringsAsFactors=False)
        col_names_r = r('colnames(csv)')
        col_names = list(col_names_r)
        r('csv[csv==""] <- NA')
        r('dfA <- csv[str_detect(csv$ID, "-aaa-"), ]')
        r('dfB <- csv[str_detect(csv$ID, "-bbb-"), ]')
        s = r('structure(list(csv = csv, dfA = dfA, dfB = dfB))')

        r('write.csv(csv, file="file.csv")')
        file = pd.read_csv('file.csv')
        try:
            os.remove('file.csv')
        except OSError:
            pass
        file_flag = 1
    except: # Add specific exception error
        message = "Cannot find such file"
        return file_flag, message

    return file_flag, file, col_names, s
