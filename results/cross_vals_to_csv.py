import pickle
import pandas as pd

with open("cross_vals.pickle", "rb") as f:
  data = pickle.load(f)

new_array = []

z = zip(data[0], data[1])
for index, (string, array) in enumerate(z):
  for value in array:
    new_array.append([string,value])
  

pd.DataFrame({"Model":[x[0] for x in new_array], "MSE":[x[1] for x in new_array]}).to_csv("cross_vals.csv", index=False)