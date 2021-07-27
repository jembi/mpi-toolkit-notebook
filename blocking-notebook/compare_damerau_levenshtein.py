from fastDamerauLevenshtein import damerauLevenshtein


def compare(str1, str2, level=2):

    if str1.lower() == str2.lower():                # in a pure Python implementation, this would be faster
        return True
    if str1 and str2:
        return damerauLevenshtein(str1, str2, False) <= level
    return False


def output(name1, name2):

    return damerauLevenshtein(name1, name2, False)
