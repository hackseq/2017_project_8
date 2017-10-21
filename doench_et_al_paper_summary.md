### change seq of sgRNA to change Cas-9; optimize on-target efficacy and minimize off-target potential

### sgRNA sequence and experimental condition - important for high efficiency

### 1841 sgRNAs used for screening - resulted in Rule Set 1 score and used for the following libraries:
    1. Avana - human
    2. Asiago- mouse

### 6 sgRNAs per gene, are selected based on: (Supp Table 1- 3)
    1. Rule Set 1 score
    2. Specificity within protein-coding regions
    3. Target site location within the gene

### Libraries tested using resistance to vemurafenib (Zelboraf) in A375 melanoma cells which carry BRAF V600E mutation and are sensitive to MAPK pathway (Supp Fig 1 - 2)

### More screening data in Supp Fig 3

### sgRNAs were ranked by their log2 fold-change relative to their abundance in the plasmid DNA pool and averaged ranks from the two replicates - Supp Table 4

### RIGER Algorithm screening for GeCKOv1, GeCKOv2 and Avana - Supp Table 5 + Supp Fig 4

### RIGER only uses data from the top two perturbations so STARS was developed - generates false-discovery rates (FDR) - similar to MAGeCK algorithm

### STARS observation - CUL3, MED12, NF1, NF2, TADA1, TADA2B - FDR < 1% - Supp Table 6

### Annotation of PanCancer genes - loss may restore MAPK pathway or find other path for survival - Supp Table 7

### Selumetinib screen - Supp Tables 8 and 9

### Screening results - Supp Figs 5 and 6

### Negative screens - Supp Fig 7 and Supp Tables 10 and 11

### ROC-AUC of each sgRNA for the three libraries - Supp Fig 8 and Supp Table 12

### Gene Set Enrichment Analysis - Supp Fig 8 and Supp Table 12

### Avana + GeCKO -> STARS - Supp Table 13

### Negative-selection screen performance of Avana in HT29 (colon cancer cell line) - Supp Table 10 and 11 and Supp Fig 10

### More Avana library analysis - Supp Table 12

### Screening of Avana to purine analog 6-thiguanine in A375 (HPRT1 was targeted most), HT29 and 293T cell lines (HPRT1 was enriched but NUDT5 targeting produced similar resistance) - Fig 2a, Supp Table 14 and Supp Fig 11

### Asisago - BV2 cells challenged with interferon gamma and STARS - Table 1 and Supp Table 15

### Rule Set 2 - Fig 3a and Supp Table 16 - 2549 sgRNAs targeting 8 genes make RES data set.

### 4000 sgRNAs targeting 17 genes - efficacy of each sgRNA versus its position in protein coding region - Supp Fig 12 and Fig 3c

### Machine learning models already used:
1. Linear Regression
2. L1-regularized linear regression
3. L2-regularized linear regression
4. hybrid SVM plus logistic regression
5. Random Forest
6. Gradient-boosted regression tree
7. L1 logistic regression (classifier)
8. SVM classification

### One-hot encoding done

### 20% versus 80% classification using SVM with logistic regression gave best results - Fig 4a and Supp Fig 13.

### Linear vs Logistic regression model performance on FC data set - Supp Fig 14 - linear performed better

### Factors considered: (Fig 4b) - L1 regression model
1. Previously single and dinucleotide position-specific nucleotides and GC count of sgRNA were used
2. Position-independent nucleotide counts
3. Location of sgRNA target site within gene
4. Biochemical and structural properties - specifically thermodynamic properties
5. Microhomology features - did not improve performance


### For RES and combined data set - gradient boosted regression trees performed better

### For FC data set, performance was comparable


### Gradient boosted regression tree model proposed best - single-nucleotide and dinucleotide at each position of sgRNA, contributed most (58%) - Supp Fig 15 and Supp Table 17

### Position-independent counts of single and dinucleotides - 16%; location of sgRNA within protein - 13% and melting temperatures of different regions - 11%

### Model trained with combined data set performed best - Supp Fig 16

### Gradient-boosted regression tress model with the augmented feature set trained on combined data set - Rule Set 2

### CFD scoring - Supp Fig 19, Supp Table 19 and 20, Supp Fig 21 and 22

### Optimized sgRNA libraries - Brunello and Brie - Supp Tab 21 and 22

### CCtop algorithm implemented for scoring of Rule Set 2

### Bowtie2 not suitable for large sequences

### GUIDE-seq used for finding off-target sites
