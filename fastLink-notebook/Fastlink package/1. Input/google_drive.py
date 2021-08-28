from ipywidgets import Text

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
