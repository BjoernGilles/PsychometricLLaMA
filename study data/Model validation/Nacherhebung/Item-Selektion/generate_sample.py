import pandas as pd
import os


os.chdir('C:\\Users\\Admin\\sciebo\\Uni\\Master\\Masterarbeit\\Fragebogen\\Zweite Version\\Items')

# Read in the data
data = pd.read_excel('item_no_train_cleaned_nv1_screened.xlsx')

data = data[data['Exklude']!='x']

# select 2 random items for each permutaiton of inverted TRUE or FALSE and difficulty == 1 or 5

data['construct'] =  [x[:-2] for x in data['construct']]

item_list = []



for construct in data['construct'].unique():
    for difficulty in [1,5]:
        for inverted in [True, False]:
            items = data[(data['construct'] == construct) & (data['difficulty'] == difficulty) & (data['inverted'] == inverted)]
            items = items.sample(n=2)
            item_list.append(items)

# List to DataFrame

sample = pd.concat(item_list)


# Save the sample
sample.to_excel('sample_items.xlsx', index=False)