from machine_learning.functions_datapreprocessing import *



#data = getParquetRaw(data_name='raw_18600', saveData=False)

path = r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert\raw_data_sorted\#machine_learning\Trainingsdaten\output_raw_18600.parquet'
data = scaleData(raw_data=path, scaler_type='Standard')

print(data)