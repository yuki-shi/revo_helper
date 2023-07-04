from database_manipulation import insert_to_db
import pandas as pd

with open('./pkm_info_clean.csv', 'r') as f:
    df = pd.read_csv(f)

insert_to_db('pkm_list', df)
