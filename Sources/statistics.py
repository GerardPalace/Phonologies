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
        percentage[i] = p/size * 100
    print(percentage)
    return percentage

def consonant_vowel_graph(dataframe):
    vowel_small = dataframe[dataframe["2A Vowel Quality Inventories"] == "1 Small (2-4)"]
    vowel_average = dataframe[dataframe["2A Vowel Quality Inventories"] == "2 Average (5-6)"]
    vowel_large = dataframe[dataframe["2A Vowel Quality Inventories"] == "3 Large (7-14)"]
    vowels = [vowel_small, vowel_average, vowel_large]

    consonant_possible = getPossibleValues(dataframe, "1A Consonant Inventories")
    getPercentageOfColumns(dataframe, "1A Consonant Inventories", consonant_possible)
    for vowel in vowels:
        getPercentageOfColumns(vowel, "1A Consonant Inventories", consonant_possible)

if __name__ == "__main__":
    df_total = pd.read_table("../Data/language.csv", ",", encoding='utf-8')
    consonant_vowel_graph(df_total)
