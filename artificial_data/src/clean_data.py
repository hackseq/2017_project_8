# Author: Enes Kemal Ergin
# Date: 20-21-22 October 2017
# HackSeq 2017

import pandas as pd


## Read the data given by <> lab @SFU

# NOTE: Data was already cleaned manually a bit, since it has only 73 data points
# Ignore some columns while reading the data into pandas dataframe
data = pd.read_csv('../data/raw/C_elegans_CRISPR_sgRNA_Database.csv', usecols=[0,1,3,5,6,8,9,10,11,12])

## Making things more consistent

# case consistency, make all uppercase
data['sgRNA'] = data['sgRNA'].str.upper()
# use one sign for consistency
data['sgRNA'] = data['sgRNA'].str.replace(',', ';')
# remove unwanted characters from target name
data['target_name'] = data['target_name'].str.replace('`','')

## Split the sgRNA column if it has more than 1 sequence assigned.

# NOTE: This is pretty clumsy way of doing it. Needs to be optimized for scalibility.
first_seq = []
second_seq = []
for i in data['sgRNA']:
    try:
        index_value = i.index(';')
    except ValueError:
        index_value = 0

    if index_value == 0:
        first_seq.append(i)
        second_seq.append('')
    elif index_value != 0:
        first_seq.append(i[:index_value])
        second_seq.append(i[index_value+2:])

# Add sequence columns naming sgRNA-1 and sgRNA-2
data['sgRNA-1'] = pd.Series(first_seq)
data['sgRNA-2'] = pd.Series(second_seq)

# drop the sgRNA column
data = data.drop('sgRNA', axis=1)

# Repositioning the columns
data = data[['sgRNA-1', 'sgRNA-2',"target_name", "sgRNA_cut",
             "num_worms", "num_lines", "sgRNA_type", "promoter_used",
             "cas9_type", "screening_method","repair_mechanism"]]


## Finalizing the cleaning

# Getting rid of paranthesis and contents inside in promoter_used
data['promoter_used'] = data['promoter_used'].str.replace(r'\([^)]*\)', '').str.strip()

# Fill NaNs with 0 and make sure everything stays integer.
data = data.fillna(0, downcast=int)

## Write the dataset
data.to_csv('../data/new/cleaned_celegans_crispr_data.csv', index=None)
