# Author: Enes Kemal Ergin
# Date: 20-21-22 October 2017
# HackSeq 2017

from scipy.stats import truncnorm
import pandas as pd
from utils import *
import random

## Read the cleaned real data and dummy candidate sgRNA data

real = pd.read_csv('../data/new/cleaned_celegans_crispr_data.csv')
dumy = pd.read_csv('../data/new/sgRNA_dummy_candidates.csv')

## Further filter

# Get the melting temps and gc counts of real data
real_melt_temps = list(map(melt_temp, list(real['sgRNA-1'])))
real_gc_counts = list(map(calc_gc, list(real['sgRNA-1'])))

# Add melting temp and gc counts to dumy dataframe
dumy['melting_temp'] = pd.Series(map(melt_temp, list(dumy['sgRNA'])))
dumy['gc_counts'] = pd.Series(map(calc_gc, list(dumy['sgRNA'])))

# filter out the ones are outside of the real data's scope
dumy = dumy[((dumy['melting_temp'] > min(real_gc_counts)) &
             (dumy['melting_temp'] < max(real_gc_counts))) &
             ((dumy['gc_counts'] > min(real_melt_temps)) &
             (dumy['gc_counts'] < max(real_melt_temps))) ].reset_index(drop=True)


## Simulate the sgRNA_cut variable

# Get the ratio of real data's sgRNA cut
real['sgRNA_cut'] = real['sgRNA_cut'].map({'Yes': 1, 'No': 0})
pos_ratio = real[real['sgRNA_cut'] == 1].shape[0] / len(real['sgRNA_cut'])
neg_ratio = real[real['sgRNA_cut'] == 0].shape[0] / len(real['sgRNA_cut'])

# Create artificial data points by keeping the real rations
pos_lst = []
neg_lst = []
pos_lst = [1] * int(np.ceil(pos_ratio*dumy.shape[0]))
neg_lst = [0] * int(np.floor(neg_ratio*dumy.shape[0]))
cut_lst = pos_lst + neg_lst
random.shuffle(cut_lst)


## Simulate the num_worms

# Getting min and max of real data
a, b = min(real['num_worms']), max(real['num_worms'])
# Getting mean and standard deviation of real data
mu, sigma = np.mean(real['num_worms']), np.std(real['num_worms'])
# Create the distribution object
dist = truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)
# Creat data size number of values
values = dist.rvs(dumy.shape[0])
num_worms_lst = [int(i) for i in values]

## Simulate the num_lines

# Getting min and max of real data
a, b = min(real['num_lines']), max(real['num_lines'])
# Getting mean and standard deviation of real data
mu, sigma = np.mean(real['num_lines']), np.std(real['num_lines'])
# Create the distribution object
dist = truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)
# Creat data size number of values
values = dist.rvs(dumy.shape[0])
num_lines_lst = [int(i) for i in values]


## Comparing num_worms and num_lines : Final sanity check

tmp_lines = []
tmp_worms = []

for i in range(dumy.shape[0]):
    worm = num_worms_lst[i]
    line = num_lines_lst[i]
    if worm < line:
        worm, line = line, worm

    tmp_worms.append(worm)
    tmp_lines.append(line)

num_worms_lst = tmp_worms
num_lines_lst = tmp_lines
## Final touches to dataframe

# Adding the simulated lists into dataframe
dumy['sgRNA_cut'] = pd.Series(cut_lst)
dumy['num_worms'] = pd.Series(num_worms_lst)
dumy['num_lines'] = pd.Series(num_lines_lst)

# Reorganize the columns
dumy = dumy[['sgRNA', 'target_name', 'sgRNA_cut', 'num_worms', 'num_lines',
                             'melting_temp', 'gc_counts', 'true_PAM']]

# Drop the unused columns
dumy = dumy.drop(['melting_temp', 'gc_counts', 'true_PAM'], axis=1)

## Write to csv
dumy.to_csv('../data/new/artificial_sgRNA_c_elegans_data.csv', index=None)
