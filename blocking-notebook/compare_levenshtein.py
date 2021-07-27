def compare(str1, str2, level=2):
    if len(str1) * len(str2) == 0:
        return False
    return edit_distance(str1, str2) <= level


def edit_distance(seq1, seq2):                           # returns Levenshtein distance between two strings

    seq1 = seq1.upper()
    seq2 = seq2.upper()

    if seq1 == seq2:
        return 0

    grid = [[0 for a in range(len(seq2) + 1)] for b in range(len(seq1) + 1)]

    for i in range(1, len(seq2) + 1):
        grid[0][i] = i
    for j in range(1, len(seq1) + 1):
        grid[j][0] = j
    for i, x in enumerate(seq2, 1):  # i and j are the index values
        for j, y in enumerate(seq1, 1):
            if x == y:
                grid[j][i] = grid[j - 1][i - 1]
            else:
                grid[j][i] = min(grid[j - 1][i - 1], grid[j][i - 1], grid[j - 1][i]) + 1

    return grid[-1][-1]


def output(name1, name2):

    return edit_distance(name1, name2)
