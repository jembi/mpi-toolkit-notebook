from phonetics import dmetaphone


def compare(str1, str2, level=0):

    result1 = dmetaphone(str1)
    result2 = dmetaphone(str2)
    for dm in result1:
        if dm and dm in result2:
            return True
    return False
