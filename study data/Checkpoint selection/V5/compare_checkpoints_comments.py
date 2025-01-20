# Import necessary libraries
import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
# Import the Levenshtein distance function
from Levenshtein import distance as levenshtein_distance

# Change the working directory
os.chdir("C:/Users/Admin/sciebo/Uni/Master/Masterarbeit/Modelltraining/Evaluation/V5 & 6")
os.listdir()

# Load the json files
with open("eval_cp380.json") as f:
    ep_1_output = json.load(f)

with open("eval_cp760.json") as f:
    ep_2_output = json.load(f)

with open("eval_cp1140.json") as f:
    ep_3_output = json.load(f)

with open("eval_v6_no_diff.json") as f:
    ep_no_diff_output = json.load(f)

# Combine the dictionaries from the json files
combined_dict = {}
lists = [ep_1_output, ep_2_output, ep_3_output]

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

# repeat it for the no_diff output

combined_dict_no_diff = {}
lists = [ep_no_diff_output]

# Loop through each list and combine the dictionaries
for i, lst in enumerate(lists, start=1):
    for dictionary in lst:
        for key, value in dictionary.items():
            new_key = f"{key}_{i}"
            if new_key not in combined_dict_no_diff:
                combined_dict_no_diff[new_key] = value
            else:
                if not isinstance(combined_dict_no_diff[new_key], list):
                    combined_dict_no_diff[new_key] = [combined_dict_no_diff[new_key]]
                combined_dict_no_diff[new_key].append(value)

# Sort the combined dictionary
sorted_dict = dict(sorted(combined_dict.items(), key=lambda x: int(x[0].split('_')[-1])))

# Make sure all lists in the dictionary have the same length
max_len = max([len(v) for v in sorted_dict.values()])
for k, v in sorted_dict.items():
    if len(v) < max_len:
        sorted_dict[k] = v + [None] * (max_len - len(v))

# Make sure all lists in the dictionary have the same length
max_len = max([len(v) for v in combined_dict_no_diff.values()])
for k, v in combined_dict_no_diff.items():
    if len(v) < max_len:
        combined_dict_no_diff[k] = v + [None] * (max_len - len(v))

# Convert the dictionary to a pandas DataFrame
combined_df = pd.DataFrame.from_dict(sorted_dict)
df = combined_df
del combined_df

# Convert the dictionary to a pandas DataFrame
combined_df_no_diff = pd.DataFrame.from_dict(combined_dict_no_diff)
df_no_diff = combined_df_no_diff
del combined_df_no_diff



# Sort the DataFrame
df_sorted = df.reindex(sorted(df.columns, key=lambda x: (x[:-2], int(x[-1]))), axis=1)

# Sort the DataFrame
df_sorted_no_diff = df_no_diff.reindex(sorted(df_no_diff.columns, key=lambda x: (x[:-2], int(x[-1]))), axis=1)

# Sort each column in the DataFrame
for i in range(0,len(df_sorted.columns)):
    df_sorted[df_sorted.columns[i]] = df_sorted[df_sorted.columns[i]].sort_values(ascending=False)

# Sort each column in the DataFrame

for i in range(0,len(df_sorted_no_diff.columns)):
    df_sorted_no_diff[df_sorted_no_diff.columns[i]] = df_sorted_no_diff[df_sorted_no_diff.columns[i]].sort_values(ascending=False)

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

output_distances_no_diff = {}
for col in df_sorted_no_diff.columns:
    output_distances_no_diff[col] = average_distance_list(df_sorted_no_diff[col].dropna().tolist())
output_distances_no_diff['mean'] = np.mean(list(output_distances_no_diff.values()))
output_distances_no_diff_df = pd.DataFrame.from_dict(output_distances_no_diff, orient='index')

# Save the results to an Excel file
# output_distances_df.to_excel("output_distances.xlsx")
# output_distances_no_diff_df.to_excel("output_distances_no_diff.xlsx")

# Define a function to calculate the average Levenshtein distance between two lists of strings
def average_distance_two_lists(list1, list2):
    distances = []
    for i in range(0,(len(list1))):
        for j in range(0,len(list2)):
            distances.append(levenshtein_distance(list1[i],list2[j]))
    return np.mean(distances)

# Calculate the average Levenshtein distance between each pair of columns in the DataFrame
distances_between_checkpoints = {}
for col in colnames:
    distances_between_checkpoints[col+"_1_2"] = average_distance_two_lists(df_sorted[col + '_1'].dropna().tolist(),df_sorted[col + '_2'].dropna().tolist())
    distances_between_checkpoints[col+"_1_3"] = average_distance_two_lists(df_sorted[col + '_1'].dropna().tolist(),df_sorted[col + '_3'].dropna().tolist())
    distances_between_checkpoints[col+"_2_3"] = average_distance_two_lists(df_sorted[col + '_2'].dropna().tolist(),df_sorted[col + '_3'].dropna().tolist())

# Separate the results into three different dictionaries
distances_1_2 = {}
distances_1_3 = {}
distances_2_3 = {}
for key in distances_between_checkpoints.keys():
    if "1_2" in key:
        distances_1_2[key] = distances_between_checkpoints[key]
    elif "1_3" in key:
        distances_1_3[key] = distances_between_checkpoints[key]
    else:
        distances_2_3[key] = distances_between_checkpoints[key]

# Calculate the mean distance for each dictionary
distances_1_2['mean'] = np.mean(list(distances_1_2.values()))
distances_1_3['mean'] = np.mean(list(distances_1_3.values()))
distances_2_3['mean'] = np.mean(list(distances_2_3.values()))

# Convert the dictionaries to pandas DataFrames
distances_1_2_df = pd.DataFrame.from_dict(distances_1_2, orient='index')
distances_1_3_df = pd.DataFrame.from_dict(distances_1_3, orient='index')
distances_2_3_df = pd.DataFrame.from_dict(distances_2_3, orient='index')

# Save the results to Excel files
distances_1_2_df.to_excel("distances_1_2.xlsx")
distances_1_3_df.to_excel("distances_1_3.xlsx")
distances_2_3_df.to_excel("distances_2_3.xlsx")

# Bundle the results together
bundled_results = []
bundled_results.append(distances_1_2_df.drop('mean').values.tolist())
bundled_results.append(distances_1_3_df.drop('mean').values.tolist())
bundled_results.append(distances_2_3_df.drop('mean').values.tolist())

# Convert the bundled results to a json string
bundled_results_json = json.dumps(bundled_results)

# Save the bundled results to a json file
# with open("bundled_results.json", "w") as outfile:
#     outfile.write(bundled_results_json)




for i in range(0,len(df_sorted.columns)):
    df_sorted.columns.values[i]=df_sorted.columns.values[i].strip()

# sort every column of the dataframe by alphabetical order

df_list = []


for column in df_sorted.columns:
    df_list.append(df_sorted[column].sort_values(ascending=True))

df_list_no_diff = []

for column in df_sorted_no_diff.columns:
    df_list_no_diff.append(df_sorted_no_diff[column].sort_values(ascending=True))

# make sure that all lists have the same length

for i in range(0,len(df_list)):
    if len(df_list[i]) < 15:
        df_list[i]=df_list[i].append(pd.Series([None] * ((15) - len(df_list[i]))))




df_list=pd.DataFrame(df_list).transpose()
df_list_no_diff=pd.DataFrame(df_list_no_diff).transpose()

df_list.to_excel("df_sorted_items.xlsx")
df_list_no_diff.to_excel("df_sorted_items_no_diff.xlsx")




# Read the original items


dataset = pd.read_csv("C:/Users/Admin/sciebo/Uni/Master/Masterarbeit/Modelltraining/Evaluation/V5 & 6/data_10092023.csv")

items = dataset['output'].tolist()


# Calculate how many generated items were in the dataset

df_list = df_list.to_dict()
#df_list.pop('in_dataset')

type(df_list)


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

distances_min_list_matrix = np.array(distances_min_list).reshape(15,180)
duplicate_items_matrix = np.array(duplicate_items).reshape(15,180)

distances_min_list_df = pd.DataFrame(distances_min_list_matrix)
duplicate_items_df = pd.DataFrame(duplicate_items_matrix)

distances_min_list_df = distances_min_list_df.rename(columns=dict(zip(range(0, 180), df_list.columns)))
duplicate_items_df = duplicate_items_df.rename(columns=dict(zip(range(0, 180), df_list.columns)))

distances_min_list_df.to_excel("distances_min_list.xlsx")
duplicate_items_df.to_excel("duplicate_items.xlsx")

# repeat for no_diff
duplicate_items = []
distances_min_list = []

df_list_no_diff= df_list_no_diff.transpose().to_dict()

for value in df_list_no_diff.values():
    for item in value.values():

        if item is None:
            distances_min_list.append(None)
            duplicate_items.append(None)
            continue

        distances_min = min(get_all_dists(item,items))
        distances_min_list.append(distances_min)
        duplicate_items.append(1 if distances_min <= 3 else 0)


df_list_no_diff = pd.DataFrame(df_list_no_diff)

distances_min_list_matrix = np.array(distances_min_list).reshape(15,20)
duplicate_items_matrix = np.array(duplicate_items).reshape(15,20)

distances_min_list_df = pd.DataFrame(distances_min_list_matrix)
duplicate_items_df = pd.DataFrame(duplicate_items_matrix)

distances_min_list_df = distances_min_list_df.rename(columns=dict(zip(range(0, 20), df_list_no_diff.columns)))
duplicate_items_df = duplicate_items_df.rename(columns=dict(zip(range(0, 20), df_list_no_diff.columns)))

distances_min_list_df.to_excel("distances_min_list_no_diff.xlsx")
duplicate_items_df.to_excel("duplicate_items_no_diff.xlsx")