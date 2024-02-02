import os.path

import pandas as pd
from machine_learning.functions_augmentation import *
from machine_learning.functions_datapreprocessing import *

# Int.funktion erstellen
#p = createIntFunktion()

# Synthetische Daten erzeugen und abspeichern
#createAugData_Jitt_Scale(number_runs=6)

# Kombinieren von zwei Parquet Dateien
data1 = pd.read_parquet(r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert\raw_data_sorted\#machine_learning\Trainingsdaten\output_aug_new2_18600.parquet')
data2 = pd.read_parquet(r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert\raw_data_sorted\#machine_learning\Trainingsdaten\output_raw+aug+aug_new_18600.parquet')
combined_df = combineParquets(data1, data2)

combined_df.to_parquet(os.path.join(Config.PATH_Trainingsdaten, r'output_raw+aug+aug_new2_18600.parquet'))

