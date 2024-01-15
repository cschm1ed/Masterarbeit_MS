from machine_learning.preparedata import prepareData
from machine_learning.random_forest.functions_rf import runRandomForest

# keine Normierung:
runRandomForest(data_raw=r'../raw_data_sorted/#machine_learning/output_raw.parquet', n_estimators=100, scaler_type='Ohne')

# MinMax:
#runRandomForest(data_raw=r'../raw_data_sorted/#machine_learning/output_MinMaxScaler.parquet', n_estimators=4, scaler_type='MinMax')

# Standard:
#runRandomForest(data_raw=r'../raw_data_sorted/#machine_learning/output_StandardScaler.parquet', n_estimators=4, scaler_type='Standard')