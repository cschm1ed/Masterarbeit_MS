import os.path
from machine_learning.random_forest.functions_rf import runRandomForest
from configurations.config import Config

############################################################################################################################

######
data_raw = os.path.join(Config.PATH_data_machine_learning, 'output_raw_18600.parquet')

#sample_lengths = [18600, 9300, 3100, 1860, 100, 10]
sample_lengths = [25, 50, 100, 200, 300, 1860, 9300, 18600]


feature_type = 'MA_Karle'

n_estimator = [4, 10, 100]
######


runRandomForest(data_raw=data_raw, sample_lengths= sample_lengths, n_estimators=n_estimator, feature_type=feature_type)



