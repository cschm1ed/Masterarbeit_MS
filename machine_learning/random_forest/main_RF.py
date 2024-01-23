import os.path
from machine_learning.random_forest.functions_rf import runRandomForest
from configurations.config import Config

############################################################################################################################

######
data_raw = os.path.join(Config.PATH_data_machine_learning, 'output_StandardScaler.parquet')

#window_sizes = [18600, 9300, 3100, 1860, 100, 10]
window_sizes = [25, 50, 100, 200, 300, 1860, 9300, 18600]

feature_type = 'MA_Karle'

n_estimator = [4, 10, 100]
######


runRandomForest(data_raw=data_raw, window_sizes= window_sizes, n_estimators=n_estimator, feature_type=feature_type)



