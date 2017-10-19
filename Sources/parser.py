import matplotlib.pyplot as plt
import pylatex as px
import pandas as pd
import numpy as np
import sys
import os

# Ce programme a pour but de comprendre rapidement chaque colonnes et quelles
# valeurs peuvent prendre chacune d'entres elles. Pour cela il crée un nouveau
# fichier (pour l'instant 2 un txt et un pdf) dans lequelles chaque Colonnes
# est associés à ses valeurs possibles.

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

def compareQualitativeString(a):
    res = getNumberOutOfString(a)
    if (res > 0):
        return res
    else:
        return 0

def createLateXDocument(filepath):
    if not os.path.exists("../LateX"):
        os.makedirs("../LateX")
    doc = px.Document(filepath)
    doc.preamble.append(px.Command('title', 'Description des variables quantitatives'))
    doc.preamble.append(px.Command('author', 'parser.py'))
    doc.preamble.append(px.Command('date', px.utils.NoEscape(r'\today')))
    doc.append(px.utils.NoEscape(r'\maketitle'))
    return doc

def writeLateXSection(title, content, doc):
    with doc.create(px.Section(title)):
        for value in content:
            doc.append(value + " ; ")

def writeTxtSection(title, content, file, content_per_raw):
    file.write("\n" + title +" :\n")
    i = 1
    for value in content:
        if i % content_per_raw == 0 or i > len(content):
            file.write(value+"\n")
        else:
            file.write(value + " ; ")
        i += 1
    file.write("\n")

def parseQualitativeValue(dataframe):
    lateX_file = createLateXDocument("../LateX/Description")
    txt_file = open("description.txt", "w")

    total = len(dataframe.columns)
    current_progress = 0
    for columns_name in dataframe.columns.values:
        bar_len = progressbar(current_progress/total)
        current_progress += 1
        possible_values = []
        str_values = ""
        #On retire les valeurs trop uniques ou quantitatives
        #if (c!="iso_code" and c!="countrycodes" and c!="glottocode" and c!="Name" and c!="wals_code"\
        #    and c!="genus" and c!="family"):
        for i in range(len(dataframe)):
            if (pd.isnull(dataframe.loc[i, columns_name])==False and \
                dataframe[columns_name][i] not in possible_values):
                possible_values.append(dataframe[columns_name][i])
        possible_values = sorted(possible_values, key=compareQualitativeString)
        writeLateXSection(columns_name, possible_values, lateX_file)
        writeTxtSection(columns_name, possible_values, txt_file, 20)

    lateX_file.generate_pdf(clean_tex=False, compiler='lualatex')
    progressbar(1)

def parse(filepath="../Data/language.csv", separator=","):
    df_total = pd.read_table(filepath, separator, encoding='latin-1')

    df_qualitative = df_total.select_dtypes(include=["object"])
    parseQualitativeValue(df_qualitative)

parse()
