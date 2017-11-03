import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from parser import getPossibleValues

#Y a-t-il un lien entre le nombre de consones et le nombre de voyelle dans les langues ?
#Y a-t-il des liens avec d'autres phénomènes phonologiques ? Ton, nasalisation ?
#Y a-t-il des liens entre inventaire de sons et distribution géographique ?
#Y a-t-il des liens entre inventaire de sons et la morphologie des langues ?

def getPercentageOfColumns(dataframe, columns_name, possible_values):
    size = 0
    percentage = [0] * len(possible_values)
    for row in dataframe.itertuples(index=True, name='Pandas'):
        value = row[dataframe.columns.get_loc(columns_name) + 1]
        if pd.isnull(value) == False:
            size += 1
            for i, v in enumerate(possible_values):
                if value == v:
                    percentage[i] += 1
    for i, p in enumerate(percentage):
        percentage[i] = round(p/size * 100, 2)
    return percentage

def compareColumns(dataframe, x_name, y_name):
    x_possible = getPossibleValues(dataframe, x_name)
    x = []
    for v in x_possible:
        x.append(dataframe[dataframe[x_name] == v])
    y_possible = getPossibleValues(dataframe, y_name)
    total_repartition = getPercentageOfColumns(dataframe, y_name, y_possible)
    x_repartitions = []
    for value in x:
        x_repartitions.append(getPercentageOfColumns(value, y_name, y_possible))

    print(y_name + " pourcentages globaux : ")
    for i, v in enumerate(y_possible):
        print("   " + v +  " : " + str(total_repartition[i]) + "%")
    for i, v in enumerate(x_repartitions):
        print(x_name + " " + x_possible[i] + " : ")
        for j, perc in enumerate(v):
            print("   " + y_possible[j] + " : " + str(perc) + "%")

if __name__ == "__main__":
    df_total = pd.read_table("../Data/language.csv", ",", encoding='utf-8')
    compareColumns(df_total, "2A Vowel Quality Inventories", "1A Consonant Inventories")
    compareColumns(df_total, "13A Tone", "10A Vowel Nasalization")
