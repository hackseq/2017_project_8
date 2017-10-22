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

def get_5mer(s):
    assert len(s) == 30, "seems to assume 30mer"
    return s[19:24]


def get_proximal_5mer_feature(data_df):
    proximal_5mer = data_df['30mer'].apply(get_5mer)
    proximal_5mer.name = "proximal_5mers"
    proximal_5mer = pd.DataFrame(proximal_5mer)

    proximal_5mer_counts = proximal_5mer.groupby(["proximal_5mers"]).size().reset_index()
    proximal_5mer = proximal_5mer.merge(proximal_5mer_counts, on="proximal_5mers")
    proximal_5mer = proximal_5mer.rename(columns={0: 'proximal_5mer_counts'})
    return proximal_5mer


if __name__ == '__main__':
    feature_df = pd.read_csv("../../../../../results/cleaned_c_elegans_30mers.csv")

    features = featurize_data(feature_df,
                         learn_options=learn_options,
                         Y=feature_df,
                         gene_position=feature_df)

    features['proximal_5mer'] = get_proximal_5mer_feature(feature_df)
    inputs, dim, dimsum, feature_names = concatenate_feature_sets(features)

    doensch_df = pd.DataFrame(inputs, columns=feature_names)
    feature_df = feature_df.join(doensch_df)
    feature_df = feature_df.drop(axis=1, labels=['sgRNA', 'Gene target', '30mer', 'WormsInjected', 'SuccessfulInjections'])
    feature_df = pd.get_dummies(feature_df).dropna(axis=0)
    if any(feature_df.columns.duplicated()):
        feature_df = feature_df.loc[:,~feature_df.columns.duplicated()]

    feature_df = feature_df.rename(columns={"SuccessRate": "target"})


    print(feature_df.shape)

    cols = feature_df.columns.tolist()
    cols.append(cols.pop(cols.index('target')))
    feature_df = feature_df.reindex(columns=cols)

    print(feature_df.columns.tolist()[-1])

    feature_df.to_csv("../../../../../results/dummied_c_elegans_30mers.csv")
