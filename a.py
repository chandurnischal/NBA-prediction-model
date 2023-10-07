import requests
from bs4 import BeautifulSoup
from os.path import basename, join
from tqdm import tqdm 

class NBA:
    def __init__(self) -> None:
        self.baseURL = "https://www.basketball-reference.com/"
        self.regular = self.baseURL + "leagues"
        self.playoffs = self.baseURL + "playoffs"
    
    def scrapeYear(self, type:str, year:int, destination:str) -> None:

        if type == "regular":
            url = self.regular
        elif type == "playoffs":
            url = self.playoffs
        else:
            return None

        url += "/NBA_{}_totals.html".format(year)

        r = requests.get(url=url)

        with open(join(destination, basename(url)), "w", encoding="utf-8") as f:
            f.write(r.text)

        
    def scrapeYears(self, type:str, startYear:int, endYear:int, destination:str) -> None:
        for year in tqdm(range(startYear, endYear + 1)):
            self.scrapeYear(type, year, destination)


nba = NBA()
