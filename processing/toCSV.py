import json
import utils as u
import os
from tqdm import tqdm

with open('creds.json') as file:
    creds = json.load(file)

tableQuery = '''
show tables;
'''

destination = 'data/csv'

if os.path.exists(destination) == False:
    os.mkdir(destination)

tables = u.sqlTodf(tableQuery, creds)

for _, table in tqdm(tables.iterrows()):
    dataQuery = '''select * from {}'''.format(table.iloc[0])
    data = u.sqlTodf(dataQuery, creds)
    data.to_csv('{}/{}.csv'.format(destination, table.iloc[0]), index=False)