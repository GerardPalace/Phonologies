import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

#Ce programme a pour but d'écrire un fichier décrivant les colonnes et les différentes valeurs possible

df = pd.read_table("../Data/language.csv", ',')

modal_value_file = open("modal_value", "w")
for c in df.columns.values:
    possible_values = []
    str_values = ""
    #On retire les valeurs trop uniques ou quantitatives
    if (c!="latitude" and c!="longitude" and c!="wals_code" \
    and c!="iso_code" and c!="glottocode" and c!="Name" and c!="countrycodes"):
        for i in range(len(df)):
            if (df[c][i]!=None and df[c][i] not in possible_values):
                possible_values.append(df[c][i])
                str_values += str(df[c][i]) + " ; "
        if (str_values!=""):
            modal_value_file.write(c + " : " + str_values + "\n\n")
