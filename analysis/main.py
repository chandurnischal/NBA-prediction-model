import json
import utils as u

with open('creds.json') as file:
    creds = json.load(file)

eloQ = '''
select * from elo
'''

elo = u.sqlTodf(eloQ, creds)

print(elo)