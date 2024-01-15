import pandas as pd
import os
import numpy as np
from configurations.config import Config
from functions.general import getallPaths
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


df = pd.read_csv(r'..\raw_data_sorted/#machine_learning/output_raw.csv')

df_new = df.head(18601)

print(df_new)

output_pfad_csv = os.path.join(Config.PATH_data_machine_learning, 'output_raw_einzeln.csv')
df_new.to_csv(output_pfad_csv, index=False)