# Get url from DVC
import pandas as pd
import dvc.api

path='data/wine_original.csv'
repo='.'

data_url = dvc.api.get_url(
  path=path,
  repo=repo
  )

data = pd.read_csv(data_url, sep=";")
print(data)
