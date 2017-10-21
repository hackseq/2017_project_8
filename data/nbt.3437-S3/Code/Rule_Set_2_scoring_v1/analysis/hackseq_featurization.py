import pandas as pd
from features.featurization import featurize_data

learn_options = {"V": 2,
                 # "train_genes": load_data.get_V2_genes("../../../../stable16corrected.csv"),
                 # 'test_genes': load_data.get_V3_genes(),
                 "testing_non_binary_target_name": 'ranks',
                 'include_pi_nuc_feat': True,
                 "gc_features": True,
                 "nuc_features": True,
                 "include_gene_position": True,
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
                 # main "ls", alternatives: "lad", "huber", "quantile", see scikit docs for details
                 'adaboost_alpha': 0.5,  # this parameter is only used by the huber and quantile loss functions.
                 'normalize_features': False,
                 }

if __name__ == '__main__':
    feature_df = pd.read_csv("../../../../stable16corrected.csv")
    print(featurize_data(feature_df,
                         learn_options=learn_options,
                         Y=feature_df,
                         gene_position=feature_df))
