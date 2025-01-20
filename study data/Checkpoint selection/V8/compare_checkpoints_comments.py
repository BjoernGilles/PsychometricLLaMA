# Import necessary libraries
import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
# Import the Levenshtein distance function
from Levenshtein import distance as levenshtein_distance

# Change the working directory
os.chdir("C:/Users/Admin/sciebo/Uni/Master/Masterarbeit/Modelltraining/Evaluation/V8")
os.listdir()

# Load the json files
with open("select_checkpoint300.json") as f:
    ep_1_output = json.load(f)

with open("select_checkpointep2.json") as f:
    ep_2_output = json.load(f)

with open("select_checkpoint293.json") as f:
    ep_3_output = json.load(f)

with open("select_checkpoint586.json") as f:
    ep_4_output = json.load(f)

with open("select_checkpoint586_ep6.json") as f:
    ep_5_output = json.load(f)




# Combine the dictionaries from the json files
combined_dict = {}
lists = [ep_1_output,ep_2_output,ep_3_output,ep_4_output,ep_5_output]

# Loop through each list and combine the dictionaries
for i, lst in enumerate(lists, start=1):
    for dictionary in lst:
        for key, value in dictionary.items():
            new_key = f"{key}_{i}"
            if new_key not in combined_dict:
                combined_dict[new_key] = value
            else:
                if not isinstance(combined_dict[new_key], list):
                    combined_dict[new_key] = [combined_dict[new_key]]
                combined_dict[new_key].append(value)

# Sort the combined dictionary
sorted_dict = dict(sorted(combined_dict.items(), key=lambda x: int(x[0].split('_')[-1])))

# Make sure all lists in the dictionary have the same length
max_len = max([len(v) for v in sorted_dict.values()])
for k, v in sorted_dict.items():
    if len(v) < max_len:
        sorted_dict[k] = v + [None] * (max_len - len(v))

# Convert the dictionary to a pandas DataFrame
combined_df = pd.DataFrame.from_dict(sorted_dict)
df = combined_df
del combined_df

# Sort the DataFrame
df_sorted = df.reindex(sorted(df.columns, key=lambda x: (x[:-2], int(x[-1]))), axis=1)

# Sort each column in the DataFrame
for i in range(0,len(df_sorted.columns)):
    df_sorted[df_sorted.columns[i]] = df_sorted[df_sorted.columns[i]].sort_values(ascending=False)

# Remove the last two characters from each column name
colnames = df_sorted.columns
colnames = [colname[:-2] for colname in colnames]
colnames = list(dict.fromkeys(colnames))

# Define a function to calculate the average Levenshtein distance for a list of strings
def average_distance_list(list_of_strings):
    distances = []
    for i in range(0,(len(list_of_strings))):
        for j in range(i+1,len(list_of_strings)):
            distances.append(levenshtein_distance(list_of_strings[i],list_of_strings[j]))
    return np.mean(distances)

# Calculate the average Levenshtein distance for each column in the DataFrame
output_distances = {}
for col in df_sorted.columns:
    output_distances[col] = average_distance_list(df_sorted[col].dropna().tolist())
output_distances['mean'] = np.mean(list(output_distances.values()))
output_distances_df = pd.DataFrame.from_dict(output_distances, orient='index')

output_distances_df.to_excel("output_distances.xlsx")

# Define a function to calculate the average Levenshtein distance between two lists of strings
def average_distance_two_lists(list1, list2):
    distances = []
    for i in range(0,(len(list1))):
        for j in range(0,len(list2)):
            distances.append(levenshtein_distance(list1[i],list2[j]))
    return np.mean(distances)



for i in range(0,len(df_sorted.columns)):
    df_sorted.columns.values[i]=df_sorted.columns.values[i].strip()

# sort every column of the dataframe by alphabetical order

df_list = []

for column in df_sorted.columns:
    df_list.append(df_sorted[column].sort_values(ascending=True))

# make sure that all lists have the same length

for i in range(0,len(df_list)):
    if len(df_list[i]) < 20:
        df_list[i]=df_list[i].append(pd.Series([None] * ((20) - len(df_list[i]))))

df_list=pd.DataFrame(df_list).transpose()

df_list.to_excel("df_sorted_items.xlsx")

# Read the original items

dataset = pd.read_csv("C:/Users/Admin/sciebo/Uni/Master/Masterarbeit/Modelltraining/V8/data_diff_fixed_190124.csv")

items = dataset['output'].tolist()

# Calculate how many generated items were in the dataset

df_list = df_list.to_dict()

def get_all_dists(str,str_list):
    return [levenshtein_distance(str,x) for x in str_list]

duplicate_items = []
distances_min_list = []

for value in df_list.values():
    for item in value.values():

        if item is None:
            distances_min_list.append(None)
            duplicate_items.append(None)
            continue

        distances_min = min(get_all_dists(item,items))
        distances_min_list.append(distances_min)
        duplicate_items.append(1 if distances_min <= 3 else 0)

df_list = pd.DataFrame(df_list)


distances_min_list_matrix = np.array(distances_min_list).reshape(20,80)
duplicate_items_matrix = np.array(duplicate_items).reshape(20,80)

distances_min_list_df = pd.DataFrame(distances_min_list_matrix)
duplicate_items_df = pd.DataFrame(duplicate_items_matrix)

distances_min_list_df = distances_min_list_df.rename(columns=dict(zip(range(0, 80), df_list.columns)))
duplicate_items_df = duplicate_items_df.rename(columns=dict(zip(range(0, 80), df_list.columns)))

distances_min_list_df.to_excel("distances_min_list.xlsx")
duplicate_items_df.to_excel("duplicate_items.xlsx")