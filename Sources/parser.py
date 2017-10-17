import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math

#Ce programme a pour but de comprendre rapidement chaque colonnes et quelles
#valeurs peuvent prendre chacune d'entres elles. Pour cela il crée un nouveau
#fichier (a terme LateX) dans lequelles chaque Colonnes est associés à ses
#valeurs possibles.

def progressbar(ratio):
    percent = int(ratio*100)
    progress = int(ratio*10)
    strbar = "[" + "#"*progress + " "*(10-progress)+ "]" + str(percent) + "%"
    print("\r"*len(strbar) + strbar, end='', flush='True')

df = pd.read_table("../Data/language.csv", ',')

modal_value_file = open("modal_value", "w")
total = len(df.columns)
current = 0
for c in df.columns.values:
    progressbar(current/total)
    current+=1
    possible_values = []
    str_values = ""
    #On retire les valeurs trop uniques ou quantitatives
    if (c!="latitude" and c!="longitude" and c!="wals_code" \
    and c!="iso_code" and c!="glottocode" and c!="Name" and c!="countrycodes"):
        for i in range(len(df)):
            if (pd.isnull(df.loc[i, c])==False and df[c][i] not in possible_values):
                possible_values.append(df[c][i])
        possible_values.sort()
        modal_value_file.write("\n"+ c+" :\n")
        for value in possible_values:
            if c=="genus" or c=="family":
                modal_value_file.write(value+" ; ")
            else:
                modal_value_file.write(value+"\n")
progressbar(1)
print("")
