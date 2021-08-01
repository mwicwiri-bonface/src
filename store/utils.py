from random import randint


def generate_code(minlength=9, maxlength=9, uselower=False, useupper=True, usenumbers=False, usespecial=False):
    charset = ''
    if uselower:
        charset += "abcdefghijklmnopqrstuvwxyz"
    if useupper:
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if usenumbers:
        charset += "123456789"
    if usespecial:
        charset += "~@#$%^*()_+-={}|]["
    if minlength > maxlength:
        length = randint(maxlength, minlength)
    else:
        length = randint(minlength, maxlength)
    key = ''
    for i in range(0, length):
        key += charset[(randint(0, len(charset) - 1))]
    return key
