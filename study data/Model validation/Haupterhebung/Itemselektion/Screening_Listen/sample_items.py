import pandas as pd
import numpy as np
import os
from sklearn.metrics import cohen_kappa_score
import krippendorff as kd 

Warning("Please change the path to the path where the data is stored on your computer")
os.chdir(r"PATH\study_data\Fragebogen\Haupterhebung\Itemselektion\Screening_Listen")

# Import data from excel file
data_1 = pd.read_excel("Item_screening_reviewer1.xlsx", sheet_name="Sheet1")
data_2 = pd.read_excel("Item_screening_reviewer2.xlsx", sheet_name="Sheet1")
data_3 = pd.read_excel("Item_screening_reviewer3.xlsx", sheet_name="Sheet1")




# Replace NaN with 0
data_1.valid_content=data_1.valid_content.replace(np.nan, 0)
data_2.valid_content=data_2.valid_content.replace(np.nan, 0)
data_3.valid_content=data_3.valid_content.replace(np.nan, 0)

# calculate interrater agreement for 3 raters using fleiss kappa
rater_data= (np.array([data_1.valid_content,data_2.valid_content,data_3.valid_content]))

kd.alpha(rater_data, level_of_measurement='nominal')
# 0.49







# select item with agreement
data_1.valid_content=data_1.valid_content.astype(int)
data_2.valid_content=data_2.valid_content.astype(int)
data_3.valid_content=data_3.valid_content.astype(int)

valid = [(data_1.valid_content[i]==1 & data_2.valid_content[i]==1 & data_3.valid_content[i]==1) for i in range(len(data_1.valid_content))]

np.count_nonzero(valid)/len(data_1)
# 554 valid items from 693
# 520 valid items from 693 with 3 raters

valid_items = data_1[valid]


# Create a list of all permutations of the variables: construct, inverted, difficulty

construct = valid_items.construct.unique()
inverted = valid_items.inverted.unique()
difficulty = valid_items.difficulty.unique()

# Create a list of all permutations of the variables: construct, inverted, difficulty
from itertools import product
all_permutations = list(product(construct, inverted, difficulty))

len(all_permutations)

# randomely sample 3 items for each permutation
import random
random.seed(123)
new_df = valid_items[0:0]



for i in range(len(all_permutations)):
    
    construct = all_permutations[i][0]
    inverted = all_permutations[i][1]
    difficulty = all_permutations[i][2]

    # This construct has only two items, so we need to sample only two items
    if "openness" in construct and inverted and difficulty == 3:
        n_sample = 2
    else:
        # Need for Closure got different sampling procedures than the other constructs
        if 'need_for_closure' not in construct:
            if difficulty == 3:
                n_sample = 3
            else:
                n_sample = 1
        elif 'need_for_closure' in construct and inverted:
            continue
        else:
            n_sample = 2


        new_df=pd.concat([new_df,(valid_items[valid_items.construct==all_permutations[i][0]][valid_items.inverted==all_permutations[i][1]][valid_items.difficulty==all_permutations[i][2]].sample(n_sample)).reset_index(drop=True)],axis=0)



# Create a frequency table of valid_items

new_df.groupby(['construct']).size().reset_index(name='counts')



#new_df.to_csv("selected_items_final.csv", index=False)

new_df.columns