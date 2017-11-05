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

def writeColumnDescription(dataframe, path_directory, writePossibleValue):
    txt_file = createTxT(path_directory + "/description.txt")
    total = len(dataframe.columns)
    current_progress = 0
    for columns_name in dataframe.columns.values:
        progressbar(current_progress/total)
        current_progress += 1
        possible_values = []
        if writePossibleValue == True:
            possible_values = getPossibleValues(dataframe, columns_name)
        _writeTxtSection(columns_name, possible_values, txt_file, 20)
    progressbar(1)

def writeGeoJSON(dataframe, filename, columns_name, path_directory):
    geoJSON_file = createTxT(path_directory + "/" + filename + ".js")
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
    argc = len(sys.argv)
    if (argc < 4):
        print("Utilisation: parse.py CSV_FILE TYPE PATH_DIRECTORY...")
    if sys.argv[1][-4:] == ".csv":
        csv_file = sys.argv[1]
    else:
        print("Utilisation: parse.py CSV_FILE TYPE PATH_DIRECTORY...")
    geojson_path_directory = None
    description_path_directory = None
    full_description = False

    for i, arg in enumerate(sys.argv):
        lower = arg.lower()
        if (lower == "--geojson"):
            if i + 1 > len(sys.argv):
                print("Utilisation: parse.py CSV_FILE TYPE PATH_DIRECTORY...")
                break
            else:
                geojson_path_directory = sys.argv[i+1]
        elif (lower == "--desc" or lower == "--fdesc"):
            if i + 1 > len(sys.argv):
                print("Utilisation: parse.py CSV_FILE TYPE PATH_DIRECTORY...")
                break
            else:
                if (lower == "--fdesc"):
                    full_description = True
                description_path_directory = sys.argv[i+1]

    df_total = pd.read_table(csv_file, ",", encoding='utf-8')
    if geojson_path_directory != None:
        print("GeoJson...")
        writeGeoJSON(df_total, "coord_consonant", ["1A Consonant Inventories"], geojson_path_directory)
        writeGeoJSON(df_total, "coord_vowel", ["2A Vowel Quality Inventories"], geojson_path_directory)
        writeGeoJSON(df_total, "coord_ratio", ["1A Consonant Inventories", "2A Vowel Quality Inventories", "3A Consonant-Vowel Ratio"], geojson_path_directory)
    if description_path_directory != None:
        print("Description...")
        df_qualitative = df_total.select_dtypes(include=["object"])
        writeColumnDescription(df_qualitative, description_path_directory, full_description)
