import requests
from os.path import basename, join
import pandas as pd
from tqdm import tqdm 
from time import sleep



class Players:

    def __init__(self) -> None:
        self.baseURL = "https://www.basketball-reference.com/"
        self.regular = self.baseURL + "leagues"
        self.playoffs = self.baseURL + "playoffs"
    
    def scrapeYear(self, type:str, year:int) -> pd.DataFrame:

        if type == "regular":
            url = self.regular
        elif type == "playoffs":
            url = self.playoffs
        else:
            return None

        url += "/NBA_{}_totals.html".format(year)

        # r = requests.get(url=url)

        # with open(join(destination, basename(url)), "w", encoding="utf-8") as f:
        #     f.write(r.text)

        # sleep(2.5)

        data = pd.read_html(url)[0]

        return data
        
    def scrapeYears(self, type:str, startYear:int, endYear:int) -> pd.DataFrame:

        rows = []
        for year in tqdm(range(startYear, endYear + 1)):
            df = self.scrapeYear(type, year)
            rows.append(df)

        data = pd.concat(rows)

        return data