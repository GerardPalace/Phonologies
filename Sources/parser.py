import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import pylatex as px

#Ce programme a pour but de comprendre rapidement chaque colonnes et quelles
#valeurs peuvent prendre chacune d'entres elles. Pour cela il crée un nouveau
#fichier (a terme LateX) dans lequelles chaque Colonnes est associés à ses
#valeurs possibles.

def progressbar(ratio):
    percent = int(ratio*100)
    progress = int(ratio*10)
    strbar = "[" + "#"*progress + " "*(10-progress)+ "]" + str(percent) + "%"
    print("\r"*len(strbar) + strbar, end='', flush='True')


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

def compareQualitativeString(a):
    res = getNumberOutOfString(a)
    if (res > 0):
        return res
    else:
        return 0

def writeLateXSection(title, content, doc):
    with doc.create(px.Section(title)):
        for value in content:
            doc.append(value + " ; ")

def parse(filepath="../Data/language.csv", separator=","):
    df = pd.read_table(filepath, separator, encoding='latin-1')

    df_quali = df.select_dtypes(include=["object"])

    description_doc = px.Document("../LateX/Description")
    description_doc.create(px.Section("Variables Qualitatives\n"))

    #descr_file = open("description.txt", "w")
    total = len(df.columns)
    current = 0
    for c in df_quali.columns.values:
        progressbar(current/total)
        current+=1
        possible_values = []
        str_values = ""
        #On retire les valeurs trop uniques ou quantitatives
        if (c!="iso_code" and c!="countrycodes" and c!="glottocode" and c!="Name" and c!="wals_code"\
            and c!="genus" and c!="family"):
            for i in range(len(df_quali)):
                if (pd.isnull(df_quali.loc[i, c])==False and df_quali[c][i] not in possible_values):
                    possible_values.append(df_quali[c][i])
            possible_values = sorted(possible_values, key=compareQualitativeString)
            writeLateXSection(c, possible_values, description_doc)
            #descr_file.write("\n"+ c+" :\n")
            #for value in possible_values:
            #    if c=="genus" or c=="family":
            #        descr_file.write(value+" ; ")
            #    else:
            #        descr_file.write(value+"\n")
    description_doc.generate_pdf(clean_tex=False, compiler='lualatex')
    description_doc.generate_tex()

    progressbar(1)
    print("")

parse()
