# load modules and data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from fuzzywuzzy import fuzz
import random

os.chdir('C:/Users/Admin/sciebo/Uni/Master/Masterarbeit/Fragebogen/Zweite Version/Items')

data = json.loads(open('generated_items_nacherhebung_e4.json').read())



# Construct list for the construct names
construct_list_1 = ['need_for_closure_1_1', 'need_for_closure_2_1', 'need_for_closure_3_1', 'need_for_closure_4_1', 'need_for_closure_5_1',"o_commit_1_1"]





# function for creating df from json file
def create_df_from_json(data, construct_list):


    keys = []

    for dict in data:
        for key in dict:
            keys.append(key)





    merged_dict = {}

    for dict in data:
        merged_dict.update(dict)




    # Parse list of dicts into an dataframe

    item_df = pd.DataFrame(columns=['item', 'inverted', 'construct', 'difficulty'])

    for key in merged_dict:
        meta_data = key.split("_")
        items = merged_dict.get(key)
        inverted = meta_data[3]
        construct = meta_data[1]
        difficulty = meta_data[-3]
        tmp_data = pd.DataFrame({'item': items, 'inverted': inverted, 'construct': construct, 'difficulty': difficulty})
        item_df = pd.concat([item_df,tmp_data])
    
    # replace construct numbers with construct names
    item_df['construct'] = item_df['construct'].replace(["1","2","3","4","5","6"], construct_list)

    return item_df



df1 = create_df_from_json(data, construct_list_1)

item_df = df1


# Now read the training data and delete items that are in the train set

train_data =pd.read_csv('data_diff_fixed_190124.csv')['output'].tolist()

# Deduplicate train data
train_data = list(dict.fromkeys(train_data))

# Remove items that are in train data

def calculte_fuzzy_item_list(item,item_list):
    ratios = [fuzz.partial_token_sort_ratio(item,item_list[j]) for j in range(len(item_list))]
    return ratios


similarities = [max(calculte_fuzzy_item_list(item,train_data)) for item in item_df['item'].tolist()]


item_df['similarity'] = similarities

len(item_df['similarity'][item_df['similarity']>90])

# 40 / 472 Items sind zu ähnlich zu Trainingsdaten

item_no_train = item_df[item_df['similarity'] < 90]


# Remove items of sublists that are too similar


def remove_similar_items(df, threshold=90):
    new_df = pd.DataFrame()
    items = df['item'].tolist()

    while len(items)>0:
        ratios = [fuzz.partial_token_sort_ratio(items[0],items[j]) for j in range(len(items))]
        similar_items = [items[j] for j in range(len(items)) if ratios[j] >= threshold]
        chosen_item = random.choice(similar_items)
        new_df = pd.concat([new_df, df[df['item'] == chosen_item].sample(n=1)])
        items = [item for item in items if item not in similar_items]
    return new_df



# Loop twice to catch partial matches
item_no_train_cleaned = remove_similar_items(item_no_train,threshold=90)
item_no_train_cleaned = remove_similar_items(item_no_train_cleaned,threshold=90)

len(item_df)
len(item_no_train)
len(item_no_train_cleaned)


# Calculate the maximimum interal similarity of the items

internal_similarities = [max(calculte_fuzzy_item_list(item,item_no_train_cleaned[item_no_train_cleaned['item'] != item]['item'].tolist())) for item in item_no_train_cleaned['item'].tolist()]

item_no_train_cleaned['internal_similarity'] = internal_similarities

# rename similarity column to train similarity

item_no_train_cleaned = item_no_train_cleaned.rename(columns={'similarity': 'train_similarity'})

#


frequency_table = item_no_train_cleaned.groupby(['inverted', 'construct', 'difficulty']).size().reset_index(name='count')

#save frequency table to excel
frequency_table.to_excel('frequency_table_nv2.xlsx', index=False)

print(frequency_table)

# Save cleaned items to excel

item_no_train_cleaned.to_excel('item_no_train_cleaned_nv2.xlsx', index=False)

