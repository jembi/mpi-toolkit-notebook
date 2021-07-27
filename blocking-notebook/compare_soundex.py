def compare(str1, str2, level=0):
    return convert_to_soundex(str1) == convert_to_soundex(str2)


def convert_to_soundex(name, length=4):
    if not name:
        return "0"*length

    output = [0] * length
    output[0], name = name[0].upper(), name[1:].lower()

    soundex_dic = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                   ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}
    silent_char = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    index = 1
    memory_letter = 0
    for char in name:
        if index > length - 1:
            break
        if char not in silent_char:
            for group, value in soundex_dic.items():
                if char in group:
                    if value != memory_letter:
                        output[index] = value
                        index += 1
                        memory_letter = value
        else:
            memory_letter = 0

    return format_soundex(output)


def format_soundex(soundex_list):
    name = ""
    for char in soundex_list:
        name += str(char)
    return name


def output(name):

    return convert_to_soundex(name)
