import pandas as pd
import glob
import os
from configurations.config import Config

# ----
# MAIN: DATENVORBEREITUNG RANDOM FOREST
# ----


# Pfad zum Verzeichnis, das durchsucht werden soll
ordner_pfad = os.path.join(Config.PATH_RF, 'Results_Test')

# Pattern, um alle .xlsx Dateien im Ordner zu finden
pattern = f'{ordner_pfad}/**/*.xlsx'

# Liste aller .xlsx Dateien im Ordner
file_paths = glob.glob(pattern, recursive=True)

# Initialize an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Loop through each file path, read the data, and concatenate it to the combined_df
for path in file_paths:
    # Read the current file
    data = pd.read_excel(path)
    # Änderen der Spalte
    if 'Modelname' in data.columns:
        data.rename(columns={'Modelname': 'Modellname'}, inplace=True)

    # Extract the file name and then scaler type and test type
    file_name = os.path.basename(path)
    parts = file_name.split('_')
    scaler_type = parts[-1].replace('.xlsx', '')
    training_type = '_'.join(parts[4:7]).replace('_18600.parquet', '')
    test_type = parts[3]
    # Add columns for scaler type and test type to identify the data source
    data['Scaler'] = scaler_type
    data['TrainingsType'] = training_type
    data['TestType'] = test_type

    i = 0
    # Änderungen in jeder Zeile data['Modellname']
    for i in range(i, len(data)):
        model_name = data['Modellname'].iloc[i]
        parts = model_name.split('_')
        sample_length = int(parts[-2].replace('.xlsx', ''))
        n_estimators = int(parts[1])
        data.at[i, 'sample_length'] = sample_length
        data.at[i, 'n_estimators'] = n_estimators

    # Concatenate the current data to the combined DataFrame
    combined_df = pd.concat([combined_df, data], ignore_index=True)

# Display the shape of the combined DataFrame to see the total number of rows and columns
print(combined_df)
speicherpfad = os.path.join(Config.PATH_RF, r'Results_Test/Results.xlsx')
combined_df.to_excel(speicherpfad)
