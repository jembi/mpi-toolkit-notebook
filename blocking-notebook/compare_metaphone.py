from phonetics import metaphone


def compare(str1, str2, level=0):

    return metaphone(str1) == metaphone(str2)


def output(name):

    return metaphone(name)
