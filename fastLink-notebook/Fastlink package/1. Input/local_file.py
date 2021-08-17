# 2.2) Select desired datafile
def local_file(uploaded):
    file_list = list(uploaded.keys())
    file = file_list[0]
    return file
