####
# für Funktionen prepareData()

from machine_learning.preparedata import prepareData

data = prepareData(scaler_type='Standard', saveData=True)

print(data)