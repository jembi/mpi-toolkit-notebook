# 2.2) Select desired datafile
def sample_dataset():

    df = pd.read_csv("https://raw.githubusercontent.com/jembi/mpi-toolkit-notebook/main/fastLink-notebook/data-200-100.csv")
    df.to_csv('sample_dataset.csv', index=False)
    print("Using sample dataset: 200 original, 100 duplicates")
    file = 'sample_dataset.csv'
    return file
