from textdistance import jaro_winkler

# what is important to note is that textdistance.jaro_winkler does not apply the Winkler addition
# of js + prefix_constant * prefix_matches * (1 - js) if js < 0.7


def compare(str1, str2, level=0.85):
    str1, str2 = str1.lower(), str2.lower()
    if str1 and str2:
        return jaro_winkler(str1, str2) >= level
    return False
