# Author: Enes Kemal Ergin
# Date: 20-21-22 October 2017
# HackSeq 2017

from Bio import SeqIO
import pandas as pd
from utils import *


## Create a gene-sequence dataframe from the fasta file of c.elegans genes:

# Initialize lists
nm = []
sq = []
# Parse the fast
for i in SeqIO.parse('../data/raw/genome.fa', 'fasta'):
    # Add the gene name to nm list
    nm.append(i.name)
    # Convert sequence tuple into string
    tmp_seq = "".join((i.seq))
    # Add the sequence into sq list
    sq.append(tmp_seq)

# Create data frame
celegans_genes = pd.DataFrame()
# Add the populated lists to data frame as Series
celegans_genes['gene_name'] = pd.Series(nm)
celegans_genes['sequence'] = pd.Series(sq)


## Create a DataFrame from geneId text files for c.elegans:
# Read csv file and save it in gene_df
gene_df = pd.read_csv('../data/raw/gene_IDs.txt', header=None, usecols=[2,3])
# Add column names
gene_df.columns = ['gene_id', 'gene_name']


## Merge the two dataframes on gene_name
complete_gene_df = celegans_genes.join(gene_df.set_index('gene_name'), on='gene_name')

## Clearing genes that does not have gene_id

# Fill 0 for NA
complete_gene_df['gene_id'].fillna('0')
# Filter out the 0 ones
complete_gene_df = complete_gene_df[complete_gene_df['gene_id']!='0']
# Reset index
complete_gene_df = complete_gene_df.reset_index()

## Initial Selector for sgRNA by going through all 30mers

# Run through all the sequences and select sgRNA candidate selector
size = complete_gene_df.shape[0]
all_sgRNA = {}
for idx in range(size):
    if idx % 100 == 0:
        print("Looping through:", idx,"/", size)
    seq = complete_gene_df['sequence'][idx]
    gene = complete_gene_df['gene_name'][idx]
    candidates = sgRNA_candidate_selector(unique_kmers(seq, 30))
    if len(candidates) != 0:
        all_sgRNA[gene] = candidates

# Create dataframe and populate with sgRNA the candidates
dummy_sgRNA = pd.DataFrame()

# initalize the lsts
genes_lst = []
sgRNA_lst = []
for key in all_sgRNA.keys():
    for i in all_sgRNA[key]:
        genes_lst.append(key)
        sgRNA_lst.append(i.upper())

# Add the resulting lists to dataframe
dummy_sgRNA['sgRNA'] = pd.Series(sgRNA_lst)
dummy_sgRNA['target_name'] = pd.Series(genes_lst)


## Filtering the candidates by conditions

# drop duplicates, need to be unique
dummy_sgRNA = dummy_sgRNA.drop_duplicates(['sgRNA']).reset_index(drop=True)

# Checking the PAM condition
binary_truth = []
for i in range(dummy_sgRNA.shape[0]):
    seq = dummy_sgRNA['sgRNA'][i]
    # Checking the last 5 bp of 20 mid sequence for PAM
    sub_seq = seq[-10:-5]
    if 'GG' in sub_seq:
        if seq[4] == 'G':
            binary_truth.append(1)
        else:
            binary_truth.append(0)
    else:
        binary_truth.append(0)
dummy_sgRNA['true_PAM'] = pd.Series(binary_truth)

# Drop non PAM ones
dummy_sgRNA = dummy_sgRNA[dummy_sgRNA['true_PAM'] == 1].reset_index(drop=True)

# Write the data
dummy_sgRNA.to_csv('../data/new/sgRNA_dummy_candidates.csv', index=None)
