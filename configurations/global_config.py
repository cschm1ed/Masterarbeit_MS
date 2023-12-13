from configurations.local_config import LocalConfig
import os
class GlobalConfig:
    STR_raw_data = r'raw_data_sorted'
    STR_alt = r'#alt'
    STR_neu = r'#fertig'

    PATH_raw_date = os.path.join(LocalConfig.BASE_PATH, STR_raw_data)
    PATH_alt = os.path.join(PATH_raw_date, STR_alt)




