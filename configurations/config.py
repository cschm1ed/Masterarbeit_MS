import os

class Config:
    ##########
    BASE_PATH = r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert'
    #BASE_PATH = r'/content/drive/MyDrive/Colab/Masterarbeit_Schubert'
    ##########

    STR_raw_data = r'raw_data_sorted'
    STR_data_alt = r'#alt'
    STR_data_fertig = r'#fertig'
    STR_data_machine_learning = r'#machine_learning'


    STR_servo_raeder = r"#_servo_zahnräder"
    STR_servo_riemen = r"#_servo_zahnriemen"
    STR_schritt_raeder = r"#_schritt_zahnräder"
    STR_schritt_riemen = r"#_schritt_zahnriemen"

    STR_KNN = r'KNN'
    STR_MinMaxScaler = r'MinMaxScaler'



    PATH_estlcam_exe = r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Estlcam11\Estlcam.exe'
    PATH_logic2_exe = r'C:\Program Files\Logic\Logic.exe'

    PATH_raw_data = os.path.join(BASE_PATH, STR_raw_data)
    PATH_data_alt = os.path.join(PATH_raw_data, STR_data_alt)
    PATH_data_fertig = os.path.join(PATH_raw_data, STR_data_fertig)
    PATH_data_machine_learning = os.path.join(PATH_raw_data, STR_data_machine_learning)


    PATH_servo_raeder = os.path.join(PATH_data_fertig, STR_servo_raeder)
    PATH_servo_riemen = os.path.join(PATH_data_fertig, STR_servo_riemen)
    PATH_schritt_raeder = os.path.join(PATH_data_fertig, STR_schritt_raeder)
    PATH_schritt_riemen = os.path.join(PATH_data_fertig, STR_schritt_riemen)

    PATH_KNN = os.path.join(PATH_data_machine_learning, STR_KNN)











