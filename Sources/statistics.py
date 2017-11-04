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

def printComparaison(x_repartitions, x_name, x_possible, y_name, y_possible, total_repartition):
    print(y_name + " pourcentages globaux : ")
    for i, v in enumerate(y_possible):
        print("   " + v +  " : " + str(total_repartition[i]) + "%")
    for i, v in enumerate(x_repartitions):
        print(x_name + " " + x_possible[i] + " : ")
        for j, perc in enumerate(v):
            print("   " + y_possible[j] + " : " + str(perc) + "%")

def getLabelName(string):
    res = ""
    splitted = string.split(" ")
    for i, split_str in enumerate(splitted):
        if (i > 0):
            res += split_str.lower() + " "
    return res[:-1]

def getGraphFromComparaison(x_repartitions, x_name, x_possible, y_name, y_possible, total_repartition):
    x_name = getLabelName(x_name)
    y_name = getLabelName(y_name)
    for i, v in enumerate(x_possible):
        x_possible[i] = getLabelName(v)
    for i, v in enumerate(y_possible):
        y_possible[i] = getLabelName(v)

    plt.title("Pourcentage de " + y_name + " en fonction de " + x_name)
    width = 0.9/(len(x_repartitions)+1)
    range1 = range(len(total_repartition))
    colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]
    label = "Pourcentage de " + y_name + " dans tous le dataframe"
    plt.bar(range1, total_repartition, width=width, color=[colors[0] for i in total_repartition], label=label)
    print(x_repartitions)
    for s, x in enumerate(x_repartitions):
        rangei = [l + width*(s+1) for l in range1]
        label = "Pourcentage de " + y_name + " si " + x_name + "=" + x_possible[s]
        plt.bar(rangei, x, width=width, color=[colors[s + 1] for i in x], label=label)
    plt.xticks([r + width for r in range(len(total_repartition))], y_possible)
    plt.ylabel("Pourcentage (%)")
    plt.xlabel(y_name)
    plt.legend()
    plt.show()

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
    #printComparaison(x_repartitions, x_name, x_possible, y_name, y_possible, total_repartition)
    getGraphFromComparaison(x_repartitions, x_name, x_possible, y_name, y_possible, total_repartition)


if __name__ == "__main__":
    df_total = pd.read_table("../Data/language.csv", ",", encoding='utf-8')
    compareColumns(df_total, "2A Vowel Quality Inventories", "1A Consonant Inventories")
    compareColumns(df_total, "13A Tone", "10A Vowel Nasalization")
