from fastDamerauLevenshtein import damerauLevenshtein


def compare(str1, str2, level=2):
    
    return damerauLevenshtein(str1, str2, False) <= level


def output(name1, name2):

    return damerauLevenshtein(name1, name2, False)
