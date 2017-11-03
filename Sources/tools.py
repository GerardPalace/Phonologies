import os

def progressbar(ratio):
    percent = int(ratio*100)
    progress = int(ratio*10)
    progress_str = "[" + "#"*progress + " "*(10-progress)+ "]" + str(percent) + "%"
    end_print = ''
    if ratio == 1:
        end_print = '\n'
    print("\r"*len(progress_str) + progress_str, end=end_print, flush='True')

def getNumberOutOfString(str):
    nb_digit = 0
    while nb_digit<len(str) and str[nb_digit].isdigit():
        nb_digit+=1
    if nb_digit>len(str):
        nb_digit-=1
    if nb_digit!=0:
        return int(str[0:nb_digit])
    else:
        return -1

def compareQualitativeString(string):
    res = getNumberOutOfString(string)
    if (res > 0):
        return res
    else:
        return 0

def createTxT(filepath):
    split = filepath.split("/")
    pathdirectory = ""
    for i in range(len(split) - 2):
        pathdirectory += split[i] + "/"
    pathdirectory += split[-2]
    if not os.path.exists(pathdirectory):
        os.makedirs(pathdirectory)
    return open(filepath, "w", encoding='utf-8')
