import pandas as pd
import numpy as np

def normalized_data(lst, size=50000):
    # Returns a normalized data using given list
    # as an effect of function it also plots the data

    s = np.std(lst)
    m = np.mean(lst)
    norm_lst = np.random.normal(m, s, size)

    # Plot the histogram.
    plt.hist(norm_lst, bins=25, normed=True, alpha=0.6, color='g')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, m, s)
    plt.plot(x, p, 'k', linewidth=2)
    plt.title("Normal Distribution of : mean = %.2f,  std = %.2f" % (m, s))
    plt.show()
    return norm_lst

def calc_gc(sequence):
    # Calculates the GC content of given sequence
    return (sequence.count('G') + sequence.count('C')) / float(len(sequence)) * 100

def melt_temp(sequence):
    yG = sequence.count('G')
    zC = sequence.count('C')
    wA = sequence.count('A')
    xT = sequence.count('T')
    return (64.9 + (41 * ((yG+zC-16.4)/(wA+xT+yG+zC))))

# Helper functions to decide the sgRNAs
def kmer_counts(sequence, k=4):
    """Kmer counting function
    Inputs:
        - DNA Sequence (string) (Mandatory)
        - kmer size (int) (default=4)
    Output:
        - Dictionary that holds unique kmer (key) and occurences
    """
    kmers = {}
    for i in range(len(sequence) - k + 1):
       kmer = sequence[i:i+k]
       if kmer in kmers:
          kmers[kmer] += 1
       else:
          kmers[kmer] = 1
    return kmers
    # Uncomment when to print kmer and counts
#     for kmer, count in kmers.items():
#        print (kmer + "\t" + str(count))

def unique_kmers(sequence, k=4):
    """Returns uinque kmers as a list using kmer_counts function"""
    kmer_dict = kmer_counts(sequence, k)
    return list(kmer_dict.keys())

def sgRNA_candidate_selector(all_kmers):
    """Returns candidate list that ensures following conditions"""
    candidate_lst = []
    for i in all_kmers:
        if i[0] != 'g' and (i[17] != 't' or i[17] != 'a'):
            continue

        else:
            candidate_lst.append(i)
    return candidate_lst
