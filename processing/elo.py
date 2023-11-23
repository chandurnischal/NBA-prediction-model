import json
import mysql.connector as mc
from tqdm import tqdm
import pandas as pd

with open("creds.json") as file:
    creds = json.load(file)


with mc.connect(**creds) as conn:
    cur = conn.cursor()


    query = '''
    select * from games order by year(date);
    '''

    cur.execute(query)

    column_names = [column[0] for column in cur.description]
    rows = cur.fetchall()


    data = pd.DataFrame(rows, columns=column_names)
    data.columns = [column.lower() for column in data.columns]


    elo_ratings = {team: 1500 for team in set(data['home']) | set(data['visitor'])}


    elo_list = []
    homeEloList = []
    visitorEloList = []

    for index, row in tqdm(data.iterrows()):
        home = row['home']
        visitor = row['visitor']
        home_elo = elo_ratings[home]
        away_elo = elo_ratings[visitor]

        expected_home_win = 1 / (1 + 10**((away_elo - home_elo) / 400))
        expected_away_win = 1 / (1 + 10**((home_elo - away_elo) / 400))

        k = 20 * ((abs(row['mov']) + 3) ** 0.8) / (7.5 + 0.006 * (abs(home_elo - away_elo)))
        home_score = 1 if row['hpoints'] > row['vpoints'] else 0
        away_score = 1 - home_score
        new_home_elo = round(home_elo + k * (home_score - expected_home_win), 2)
        new_away_elo = round(away_elo + k * (away_score - expected_away_win), 2)

        elo_ratings[home] = new_home_elo
        elo_ratings[visitor] = new_away_elo
        homeEloList.append(new_home_elo)
        visitorEloList.append(new_away_elo)

    data['home_elo'] = homeEloList
    data['visitor_elo'] = visitorEloList
    data = data[['date', 'season', 'is_regular', 'home_id', 'home_fid', 'visitor_id', 'visitor_fid', 'home', 'hpoints', 'home_elo', 'visitor', 'vpoints', 'visitor_elo', 'mov']]
    from sqlalchemy import create_engine

    engine = create_engine("mysql+mysqlconnector://{}:{}@{}/{}".format(creds['user'], creds['password'], creds['host'], creds['database']))
    data.to_sql(name="elo", con=engine, index=False, if_exists="replace")