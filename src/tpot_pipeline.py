from tpot import TPOTRegressor
import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    df = pd.read_csv("../results/featurized_c_elegans_30mers.csv")
    dummy_df = pd.get_dummies(df).dropna(axis=0)
    cols = dummy_df.columns.tolist()
    cols.append(cols.pop(cols.index('SuccessRate')))
    dummy_df = dummy_df.reindex(columns=cols)

    X, y = dummy_df.iloc[:, :-1].values, dummy_df.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        train_size=0.75, test_size=0.25)

    tpot = TPOTRegressor(generations=100,
                         population_size=100,
                         scoring="mean_squared_error",
                         n_jobs=-1,
                         random_state=1,
                         periodic_checkpoint_folder="../results/c_elegans_pipeline",
                         verbosity=4)
    tpot.fit(X_train, y_train)
    print(tpot.score(X_test, y_test))
    tpot.export('c_elegans_pipeline.py')

