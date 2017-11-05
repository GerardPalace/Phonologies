import matplotlib.pyplot as plt
import matplotlib.lines as line
import pandas as pd
import numpy as np
import sys
from tools import progressbar, createDirFromPath
from parser import getPossibleValues

#Y a-t-il un lien entre le nombre de consones et le nombre de voyelle dans les langues ?
#Y a-t-il des liens avec d'autres phénomènes phonologiques ? Ton, nasalisation ?
#Y a-t-il des liens entre inventaire de sons et distribution géographique ?
#Y a-t-il des liens entre inventaire de sons et la morphologie des langues ?

fig_id = 0

def _getLabelName(string):
    res = ""
    splitted = string.split(" ")
    for i, split_str in enumerate(splitted):
        if (i > 0):
            res += split_str.lower() + " "
    return res[:-1]

def _drawGraph(x_repartitions, x_name, x_possible, y_name, y_possible, total_repartition, path_directory):
    global fig_id
    for i, v in enumerate(x_possible):
        x_possible[i] = _getLabelName(v)
    for i, v in enumerate(y_possible):
        y_possible[i] = _getLabelName(v)

    fig = plt.figure(figsize=(20, 10))
    title = "Comparaison " + y_name + " par " + x_name
    plt.title(title)
    width = 0.9/(len(x_repartitions))
    range1 = range(len(total_repartition))
    colors = ["#FF00FF", "#bc80bd", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#ffffb3", "#ccebc5", "#ffed6f"]
    label = ""
    for s, x in enumerate(x_repartitions):
        rangei = [l + width*s for l in range1]
        label = "Si " + x_name + " est " + x_possible[s]
        ax = plt.bar(rangei, x, width=width, color=[colors[s + 1] for i in x], label=label)
        axes = plt.gca()
        for i, rect in enumerate(ax.patches):
            rect_x = rect.get_x()
            rect_y = rect.get_height()/2
            rect_width = rect.get_width()
            plt.text(rect_x + rect_width/2, rect_y, str(int(x[i])) + "%",ha="center", va="bottom")
            if (s==0):
                plt.text(rect_x, total_repartition[i], str(int(total_repartition[i]))+ "%",ha="center", va="bottom", color=colors[0])
            axes.add_artist(line.Line2D((rect_x, rect_x + rect_width), (total_repartition[i], total_repartition[i]), color=colors[0], linewidth=2, linestyle = 'dashed'))

    plt.xticks([r + width for r in range(len(total_repartition))], y_possible)
    plt.ylabel("Pourcentage (%)")
    plt.xlabel(y_name)
    global_line = line.Line2D([], [], color=colors[0], linewidth=2, linestyle = 'dashed')
    handles, labels = plt.gca().get_legend_handles_labels()
    handles.append(global_line)
    labels.append("Parmi toutes les valeurs")
    plt.legend(handles, labels)

    fig_id = fig_id + 1
    filepath = path_directory + "/figure" + str(fig_id) + ".svg"
    createDirFromPath(filepath)
    plt.savefig(filepath)
    return fig

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

def compareColumns(dataframe, x_name, y_name, path_directory):
    x_possible = getPossibleValues(dataframe, x_name)
    x = []
    for v in x_possible:
        x.append(dataframe[dataframe[x_name] == v])
    y_possible = getPossibleValues(dataframe, y_name)
    total_repartition = _getPercentageOfColumns(dataframe, y_name, y_possible)
    x_repartitions = []
    for value in x:
        x_repartitions.append(_getPercentageOfColumns(value, y_name, y_possible))
    fig = _drawGraph(x_repartitions, _getLabelName(x_name), x_possible, _getLabelName(y_name), y_possible, total_repartition, path_directory)
    plt.close(fig)

if __name__ == "__main__":
    argc = len(sys.argv)
    if (argc < 3):
        print("Utilisation: statistics CSV_FILE PATH_DIRECTORY")
    if sys.argv[1][-4:] == ".csv":
        csv_file = sys.argv[1]
    else:
        print("Utilisation: statistics CSV_FILE PATH_DIRECTORY")
    path_directory = sys.argv[2]

    df_total = pd.read_table(csv_file, ",", encoding='utf-8')

    morphology = ["20A Fusion of Selected Inflectional Formatives", "21A Exponence of Selected Inflectional Formatives", "22A Inflectional Synthesis of the Verb",\
    "23A Locus of Marking in the Clause", "24A Locus of Marking in Possessive Noun Phrases", "25A Locus of Marking: Whole-language Typology", \
    "26A Prefixing vs. Suffixing in Inflectional Morphology", "27A Reduplication", "28A Case Syncretism", "29A Syncretism in Verbal Person/Number Marking"]

    total = len(morphology)*3 + 2
    current_progress = 0
    print("Graphics...")

    progressbar(current_progress/total)
    current_progress += 1
    compareColumns(df_total, "2A Vowel Quality Inventories", "1A Consonant Inventories", path_directory)

    progressbar(current_progress/total)
    current_progress += 1
    compareColumns(df_total, "13A Tone", "10A Vowel Nasalization", path_directory)

    for name in morphology:
        progressbar(current_progress/total)
        current_progress += 1
        compareColumns(df_total, "1A Consonant Inventories", name, path_directory)
        progressbar(current_progress/total)
        current_progress += 1
        compareColumns(df_total, "2A Vowel Quality Inventories", name, path_directory)
        progressbar(current_progress/total)
        current_progress += 1
        compareColumns(df_total, "3A Consonant-Vowel Ratio", name, path_directory)
    progressbar(1)
