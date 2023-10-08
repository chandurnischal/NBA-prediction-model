import requests
from os.path import basename, join
import pandas as pd
from tqdm import tqdm 
from time import sleep
from bs4 import BeautifulSoup


class Players:

    def __init__(self) -> None:
        self.baseURL = "https://www.basketball-reference.com/"
        self.regular = self.baseURL + "leagues"
        self.playoffs = self.baseURL + "playoffs"
    
    def scrapeYear(self, type:str, year:int) -> pd.DataFrame:
        # regular or playoffs data
        if type == "regular":
            url = self.regular
        elif type == "playoffs":
            url = self.playoffs
        else:
            return None


        # create url for the page
        url += "/NBA_{}_totals.html".format(year)

        # request html
        r = requests.get(url)


        soup = BeautifulSoup(r.text, "html.parser")

        # locate table in html
        table = soup.find("table", id = "totals_stats")
        
        # extract columns of the table from html
        columns = table.find("thead").text.strip().split('\n')

        # remove unwanted rows from table (redundant column names present in table)
        remove = table.find_all('tr', class_ = "thead")
        for r in remove:
            r.decompose()

        # extract table rows
        body = table.find("tbody")
        tableRows = body.find_all("tr")


        rows = []
        for r in tableRows:
            row = []
        
            # extracting rank
            th = r.find("th").text
            row.append(th)

            # extract rest of data
            td = r.find_all("td")
            for t in td:
                row.append(t.text)
            rows.append(row)


        data = pd.DataFrame(rows, columns=columns)
        data["Year"] = year

        return data
        
    def scrapeYears(self, type:str, startYear:int, endYear:int) -> pd.DataFrame:

        tableRows = []
        for year in tqdm(range(startYear, endYear + 1)):
            df = self.scrapeYear(type, year)
            tableRows.append(df)
            sleep(5)
        data = pd.concat(tableRows)

        return data
    
class Teams:
    def __init__(self) -> None:
        pass



