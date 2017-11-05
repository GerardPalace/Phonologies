from tools import progressbar, getNumberOutOfString, compareQualitativeString, createTxT
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

#Ce programme parcours le dataframe et peut :
# -> Créer une variable geoJSON dans un nouveau fichier à partir du dataframe
#    avec les colonnes demandé dans une liste. (writeGeoJSON)
# -> Faire une listes des colonnes avec pour chacune les valeurs possibles. (parseQualitativeValue)

def _writeTxtSection(title, content, file, content_per_raw):
    file.write(title)
    i = 1
    for value in content:
        if i % content_per_raw == 0 or i > len(content):
            file.write(value+"\n")
        else:
            file.write(value + ", ")
        i += 1
    file.write("\n")

def getPossibleValues(dataframe, columns_name):
    possible_values = []
    for i in range(len(dataframe)):
        if (pd.isnull(dataframe.loc[i, columns_name])==False and dataframe[columns_name][i] not in possible_values):
            possible_values.append(dataframe[columns_name][i])
    return sorted(possible_values, key=compareQualitativeString)

def writeColumnDescription(dataframe, writePossible=False):
    txt_file = createTxT("../Resultats/description.txt")
    total = len(dataframe.columns)
    current_progress = 0
    for columns_name in dataframe.columns.values:
        progressbar(current_progress/total)
        current_progress += 1
        possible_values = []
        if writePossible == True:
            possible_values = getPossibleValues(dataframe, columns_name)
        _writeTxtSection(columns_name, possible_values, txt_file, 20)
    progressbar(1)

def writeGeoJSON(dataframe, filename, columns_name):
    geoJSON_file = createTxT("../HTML/Scripts/" + filename + ".js")
    geoJSON_file.write("var coordinates = {\"type\": \"FeatureCollection\", \"features\":[")
    total = dataframe.shape[0]
    current_progress = 0
    for row in dataframe.itertuples(index=True, name='Pandas'):
        progressbar(current_progress/total)
        current_progress += 1
        values = []
        abort = False
        for name in columns_name:
            if pd.isnull(row[dataframe.columns.get_loc(name) + 1]) == False:
                values.append(row[dataframe.columns.get_loc(name) + 1])
            else:
                abort = True
                break
        if abort == False:
            properties = "\"properties\":{\"name\":\"" + row.Name + "\", "
            for i, value in enumerate(values):
                valueNumber = str(getNumberOutOfString(value))
                properties += "\"valueNumber" + str(i+1) + "\":" + valueNumber  + ", \"description" + str(i+1) + "\":\"" + value[len(valueNumber) + 1:] + "\", "
            properties += "}"
            geometry = "\"geometry\":{\"type\":\"Point\", \"coordinates\":[" + str(row.longitude) + ", " + str(row.latitude) + "]}"
            geoJSON_file.write("{\"type\":\"Feature\"," + properties + "," + geometry + "},")
    progressbar(1)
    geoJSON_file.write("]}")

if __name__ == "__main__":
    full = False
    desc = False
    for arg in sys.argv:
        if arg == "--full":
            full = True
        elif arg == "--desc":
            desc = True
    df_total = pd.read_table("../Data/language.csv", ",", encoding='utf-8')
    print("GeoJson...")
    writeGeoJSON(df_total, "coord_consonant", ["1A Consonant Inventories"])
    writeGeoJSON(df_total, "coord_vowel", ["2A Vowel Quality Inventories"])
    writeGeoJSON(df_total, "coord_ratio", ["1A Consonant Inventories", "2A Vowel Quality Inventories", "3A Consonant-Vowel Ratio"])
    if full==True:
        print("Description...")
        df_qualitative = df_total.select_dtypes(include=["object"])
        writeColumnDescription(df_qualitative, desc)
