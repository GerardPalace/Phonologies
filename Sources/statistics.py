import matplotlib.pyplot as plt
import matplotlib.lines as line
import pandas as pd
import numpy as np
import sys
from parser import getPossibleValues

#Y a-t-il un lien entre le nombre de consones et le nombre de voyelle dans les langues ?
#Y a-t-il des liens avec d'autres phénomènes phonologiques ? Ton, nasalisation ?
#Y a-t-il des liens entre inventaire de sons et distribution géographique ?
#Y a-t-il des liens entre inventaire de sons et la morphologie des langues ?

def _getLabelName(string):
    res = ""
    splitted = string.split(" ")
    for i, split_str in enumerate(splitted):
        if (i > 0):
            res += split_str.lower() + " "
    return res[:-1]

def _drawGraph(x_repartitions, x_name, x_possible, y_name, y_possible, total_repartition):
    for i, v in enumerate(x_possible):
        x_possible[i] = _getLabelName(v)
    for i, v in enumerate(y_possible):
        y_possible[i] = _getLabelName(v)

    plt.figure(figsize=(10, 6))
    title = "Comparaison " + y_name + " par " + x_name
    plt.title(title)
    width = 0.9/(len(x_repartitions))
    range1 = range(len(total_repartition))
    colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]
    label = "Parmi toutes les valeurs"
    for s, x in enumerate(x_repartitions):
        rangei = [l + width*s for l in range1]
        label = "Si " + x_name + " est " + x_possible[s]
        plt.bar(rangei, x, width=width, color=[colors[s + 1] for i in x], label=label)
    axes = plt.gca()
    x1 = width-(width*3)/2
    x2 = width+(width*3)/2
    for rep in total_repartition:
        axes.add_artist(line.Line2D((x1, x2), (rep, rep), color=colors[0], linewidth=2, linestyle = 'dashed'))
        x1 = x2+0.1
        x2 = x2+(width*3)+0.1
    plt.xticks([r + width for r in range(len(total_repartition))], y_possible)
    plt.ylabel("Pourcentage (%)")
    plt.xlabel(y_name)
    plt.legend()
    plt.savefig("../Resultats/" + title + ".png")

def _getPercentageOfColumns(dataframe, columns_name, possible_values):
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

def compareColumns(dataframe, x_name, y_name, alt_x_name="", alt_y_name="", show=False):
    if alt_x_name == "":
        alt_x_name = x_name
    if alt_y_name == "":
        alt_y_name = y_name
    x_possible = getPossibleValues(dataframe, x_name)
    x = []
    for v in x_possible:
        x.append(dataframe[dataframe[x_name] == v])
    y_possible = getPossibleValues(dataframe, y_name)
    total_repartition = _getPercentageOfColumns(dataframe, y_name, y_possible)
    x_repartitions = []
    for value in x:
        x_repartitions.append(_getPercentageOfColumns(value, y_name, y_possible))
    _drawGraph(x_repartitions, alt_x_name, x_possible, alt_y_name, y_possible, total_repartition)
    if show == True:
        plt.show()

if __name__ == "__main__":
    show = False
    for arg in sys.argv:
        if arg=="--show":
            show = True
    df_total = pd.read_table("../Data/language.csv", ",", encoding='utf-8')
    compareColumns(df_total, "2A Vowel Quality Inventories", "1A Consonant Inventories", "inventaire de voyelles", "inventaire de consones", show)
    compareColumns(df_total, "13A Tone", "10A Vowel Nasalization", "système de tons", "nasalisation des voyelles", show)
