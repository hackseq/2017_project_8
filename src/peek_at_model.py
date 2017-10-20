import pickle

if __name__ == '__main__':
    with open("../data/nbt.3437-S3/Code/Rule_Set_2_scoring_v1/saved_models/V3_model_nopos.pickle", "rb") as open_file:
        model, options = pickle.load(open_file)
        print(options)