# 2.1) Pick method of uploading csv file (Always)
def upload_method():
    
    menu_1 = Dropdown(options=['Upload from google drive', 'Upload local file', "Use sample dataset"])
    return menu_1

# 2.3) Choose Unique ID and Dedupe/Linking
def upload_dataset(file):
    
    file_flag = 0
    try:
        globalenv['csv'] = r['read.csv'](file, header=True, stringsAsFactors=False)
        col_names_r = r('colnames(csv)')
        col_names = list(col_names_r)
        
        style = {'description_width': 'initial'}
        menu_1 = Dropdown(description="1. Choose your unique identifier:", style=style, options=col_names)
        layout2 = {'width': '600px'}
        menu_2 = Dropdown(layout=layout2, description="2. Are you linking records on 1 (Deduplication) or 2 (Linking) datasets:", style=style, options=["Deduplication", "Linking"])
        
        file_flag = 1
    except: # Add specific exception error
        message = "Cannot find such file"
        return file_flag, message

    return file_flag, col_names, menu_1, menu_2

# 2.4) Read data
def read_dataset(file, identifier):

    r('csv[csv==""] <- NA')
    r('dfA <- csv[str_detect(csv${0}, "-aaa-"), ]'.format(identifier))
    r('dfB <- csv[str_detect(csv${0}, "-bbb-"), ]'.format(identifier))
    s = r('structure(list(csv = csv, dfA = dfA, dfB = dfB))')

    r('write.csv(csv, file="file.csv")')
    file = pd.read_csv('file.csv')
    try:
        os.remove('file.csv')
    except OSError:
        pass

    return s, file

# 3) Capture User input (Always)
def user_input(col_names, menu_1):

    style = {'description_width': 'initial'}
    layout = {'width': '400px'}

    check_b_list = []
    for i in range(len(col_names)):
        if col_names[i] == menu_1.value:
            check_b = Checkbox(value=True, description=col_names[i], disabled=False, indent=False)
        else:
            check_b = Checkbox(value=False, description=col_names[i], disabled=False, indent=False)
        check_b_list.append(check_b)

    menu_3 = Dropdown(layout=layout, description="2. Choose your string-distance method:", style=style, options=["Jaro-Winkler", "Jaro", "Levensthein"])

    slider_label = Label(value="3. Select upper and lower bounds:")

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
    
    return check_b_list, menu_3, slider_label, slider_1

