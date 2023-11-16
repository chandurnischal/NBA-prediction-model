import utils as u
import json
import pandas as pd
from tqdm import tqdm 
from sqlalchemy import create_engine

with open("creds.json") as file:
    creds = json.load(file)

def factor(row) -> float:
    lg_ast = row['lg_ast']
    lg_fg = row['lg_fg']
    lg_ft = row['lg_ft']
    term1 = 2/3
    term2 = 0.5 * (lg_ast / lg_fg)
    term3 = 2 * (lg_fg / lg_ft)

    return term1 - term2 / term3

def VOP(row) -> float:
    return row['lg_pts'] / (row['lg_fga'] - row['lg_orb'] + row['lg_tov'] + 0.44 * row['lg_fta'])

def DRBPerc(row) -> float:
    return (row['lg_trb'] - row['lg_orb']) / row['lg_trb']

def uPER(row):
    fac = factor(row)
    vop = VOP(row)
    drbPERC = DRBPerc(row)

    return (1/row['mp']) * (row['3p']
                    + (2/3) * row['ast']
                    + (2 - fac * (row['team_ast'] / row['team_fg'])) * row['fg']
                    + (row['ft'] * 0.5 * (1 + (1 - (row['team_ast'] / row['team_fg'])) + (2/3) * (row['team_ast'] / row['team_fg'])))
                    - vop * row['tov']
                    - vop * drbPERC * (row['fga'] - row['fg'])
                    - vop * 0.44 * (0.44 + (0.56 * drbPERC)) * (row['fta'] - row['ft'])
                    + vop * (1 - drbPERC) * (row['trb'] - row['orb'])
                    + vop * drbPERC * row['orb']
                    + vop * drbPERC * row['blk']
                    - row['pf'] * ((row['lg_ft'] / row['lg_pf']) - 0.44 * (row['lg_fta'] / row['lg_pf']) * vop)
                    )

'''
(PTS + REB + AST + STL + BLK - Missed FG - Missed FT - TO) / GP
'''

def EFF(row) -> float:
    return (row['pts'] + row['trb'] + row['ast'] + row['stl'] + row['blk'] - (row['fga'] - row['fg']) - (row['fta'] - row['ft']) - row['tov']) / row['g']

'''
PER = (FGM x 85.910 + Steals x 53.897 + 3PTM x 51.757 + FTM x 46.845 + Blocks x 39.190 + Offensive_Reb x 39.190 + Assists x 34.677 + Defensive_Reb x 14.707 — Foul x 17.174 — FT_Miss x 20.091 — FG_Miss x 39.190 — TO x 53.897) x (1 / Minutes)
'''

def PER(row) -> float:
    return (row['fg'] * 85.91
            + row['stl'] * 53.897
            + row['3p'] * 51.757
            + row['ft'] * 46.845
            + row['blk'] * 39.19
            + row['orb'] * 39.19
            + row['ast'] * 34.677
            + row['drb'] * 14.707
            - row['pf'] * 17.174
            - (row['fta'] - row['ft']) * 20.091
            - (row['fga'] - row['fg']) * 39.190
            - row['tov'] * 53.897) * (1 / row['mp'])

def efficiencyTablePerPlayer(player_id:int, is_regular:int) -> pd.DataFrame:
    
    if is_regular != 0 | is_regular != 1:
        return None

    query = '''
    select a.player_id, a.team_id, a.player, a.tm, a.g, a.mp, a.pts, a.3p, a.ast, a.fg, a.ft, a.fta, a.tov, a.fga, a.trb, a.orb, a.drb, a.stl, a.blk, a.pf, b.ast team_ast, b.fg team_fg, c.*, a.is_regular from (select * from player_total where player_id = {} and is_regular= {}) a join (select team_id, team, nickname, ast, fg, year from team_total where is_regular={}) b on a.team_id=b.team_id and a.year = b.year join (select avg(ft) lg_ft, avg(pf) lg_pf, avg(fta) lg_fta, avg(ast) lg_ast, avg(fg) lg_fg, avg(pts) lg_pts, avg(fga) lg_fga, avg(orb) lg_orb, avg(tov) lg_tov, avg(trb) lg_trb, year from team_total group by year) as c on c.year=b.year order by a.year;
    '''.format(player_id, is_regular, is_regular)

    data = u.sqlTodf(query, creds)
    data = data.apply(pd.to_numeric, errors = 'ignore')
    columns = data.columns.to_list()
    columns = [c.lower() for c in columns]
    data.columns = columns

    data['uPER'] = uPER(data)
    data['eff'] = EFF(data)
    data['PER'] = PER(data)

    return data

query = '''
select * from player_unique
'''

engine = create_engine("mysql://root:root@localhost/nba")

data = u.sqlTodf(query, creds)
ids = list(data['id'])

with open("ids.txt", "a") as file:
    for id in tqdm(ids):
        try:
            df = efficiencyTablePerPlayer(id, 0)            
            if df.empty == False:
                df.to_sql(name="player_efficiency", con=engine, index=False, if_exists="append")
            else:
                file.write('{}, {}, {}\n'.format(id, 0, "empty DF"))

            df = efficiencyTablePerPlayer(id, 1)            
            if df.empty == False:
                df.to_sql(name="player_efficiency", con=engine, index=False, if_exists="append")
            else:
                file.write('{}, {}, {}\n'.format(id, 1, "empty DF"))


        except Exception as e:
            file.write('{}, {}\n'.format(id, e.__class__))