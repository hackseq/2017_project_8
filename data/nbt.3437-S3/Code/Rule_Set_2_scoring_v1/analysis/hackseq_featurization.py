import pandas as pd
from features.featurization import featurize_data
from util import concatenate_feature_sets
import numpy as np


learn_options = {"V": 2,
                 # "train_genes": load_data.get_V2_genes("../../../../stable16corrected.csv"),
                 # 'test_genes': load_data.get_V3_genes(),
                 "testing_non_binary_target_name": 'ranks',
                 'include_pi_nuc_feat': True,
                 "gc_features": True,
                 "nuc_features": True,
                 "include_gene_position": False,
                 "include_NGGX_interaction": True,
                 "include_Tm": True,
                 "include_strand": False,
                 "include_gene_feature": False,
                 "include_gene_guide_feature": 0,
                 "extra pairs": False,
                 "weighted": None,
                 "training_metric": 'spearmanr',
                 "NDGC_k": 10,
                 "order": True,
                 "num_proc": 9,
                 "cv": "gene",
                 "include_gene_effect": False,
                 "include_drug": False,
                 "include_sgRNAscore": False,
                 'adaboost_loss': 'ls',
                 'include_known_pairs': False,
                 'include_microhomology': False, # Hackseq: Someone could attempt to get this working
                 # main "ls", alternatives: "lad", "huber", "quantile", see scikit docs for details
                 'adaboost_alpha': 0.5,  # this parameter is only used by the huber and quantile loss functions.
                 'normalize_features': False,
                 }

if __name__ == '__main__':
    feature_df = pd.read_csv("../../../../../results/cleaned_c_elegans_30mers.csv")

    features = featurize_data(feature_df,
                         learn_options=learn_options,
                         Y=feature_df,
                         gene_position=feature_df)
    inputs, dim, dimsum, feature_names = concatenate_feature_sets(features)
    np.save("../../../../c_elegans_features.npy", inputs)

    with open("../../../../c_elegans_names.txt", "w+") as feature_file:
        feature_file.writelines(["{}\n".format(feature) for feature in feature_names])
