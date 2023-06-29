import pandas as pd
import re

# Read .csv into a dataframe
df = pd.read_csv('./pkm_info.csv')

# (1) Some attributes are in lists, let's split them into separate columns
for attribute in ['types', 'abilities', 'obtainability']:
    # Remove [] and '
    df[attribute] = df[attribute].str.replace(r"[\[\]']", '', regex=True)
    if attribute != 'obtainability':
        # Find how many new columns will be created by each attribute split
        max_value = df[attribute].apply(lambda x: x.count(',') + 1).max()
        new_column_names = [f'{attribute}{x}' for x in range(1, max_value+1)]
        # Split into new columns
        df[new_column_names] = df[attribute].str.split(',', expand=True)
        # Drop original column
        df = df.drop(attribute, axis=1)

# (2) Lowercase all column headers
df.columns = [x.lower() for x in df.columns]

# (3) Replace . for _ if needed on headers
df.columns = [re.sub('\.', '_', x) for x in df.columns]

# (4) Correct typos on headers
df = df.rename(columns={'types1': 'type1',
                        'types2': 'type2',
                        'abilities1': 'ability1',
                        'abilities2': 'ability2',
                        'abilities3': 'ability3'})

# (5) Normalize null values
df.loc[df['obtainability'] == '', 'obtainability'] = 'None'

# Export!
df.to_csv('pkm_info_clean.csv', index=False)
