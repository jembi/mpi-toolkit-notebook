from textdistance import jaccard


def compare(str1, str2, level=0.85):

    str1, str2 = str1.lower(), str2.lower()

    if str1 and str2:
        return jaccard.similarity(str1, str2) >= level
    return False


def output(name1, name2):

    return jaccard.similarity(name1, name2)
