import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

#Ce programme a pour but d'écrire un fichier décrivant les columns

dLanguage = pd.read_table("../Datas/language.csv", ',', index_col=0)

for row in dLanguage.itertuples(index=True, name='Pandas'):
    print (row)

#for a in list(dLanguage.columns.values):
#    print(a)
#    for ()
