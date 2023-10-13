import requests
from os.path import join
import pandas as pd
from bs4 import BeautifulSoup, Comment


class Players:
    def __init__(self, type: str) -> None:
        self.__baseURL = "https://www.basketball-reference.com/"
        if type == "regular":
            self.__baseURL += "leagues/"
        elif type == "playoffs":
            self.__baseURL += "playoffs/"
        else:
            return None

    def __tableExtractor(self, html: requests.Response, mode: str) -> pd.DataFrame:
        soup = BeautifulSoup(html.text, "lxml")
        table = soup.find(id=mode)

        if table == None:
            soup = BeautifulSoup("\n".join(soup.find_all(text=Comment)), "lxml")

        table = soup.find(id=mode)

        columns = table.find("thead").text.strip().split("\n")
        tbody = table.find("tbody")

        remove = tbody.find_all("tr", class_="thead")

        for r in remove:
            r.decompose()

        tableRows = tbody.find_all("tr")

        rows = []

        for tableRow in tableRows:
            row = []

            th = tableRow.find("th").text.strip()
            row.append(th)

            tds = tableRow.find_all("td")

            for td in tds:
                row.append(td.text.strip())
            rows.append(row)

        data = pd.DataFrame(rows, columns=columns)

        return data

    def totalStats(self, year: int) -> pd.DataFrame:
        url = self.__baseURL + "NBA_{}_totals.html".format(year)
        r = requests.get(url)
        data = self.__tableExtractor(r, "totals_stats")

        data["Year"] = year

        return data

    def perGameStats(self, year: int) -> pd.DataFrame:
        url = self.__baseURL + "NBA_{}_per_game.html".format(year)

        r = requests.get(url)
        data = self.__tableExtractor(r, "per_game_stats")

        data["Year"] = year

        return data

    def perMinuteStats(self, year: int) -> pd.DataFrame:
        url = self.__baseURL + "NBA_{}_per_minute.html".format(year)

        r = requests.get(url)

        data = self.__tableExtractor(r, "per_minute_stats")

        data["Year"] = year

        return data

    def perPossessionStats(self, year: int) -> pd.DataFrame:
        url = self.__baseURL + "NBA_{}_per_poss.html".format(year)
        r = requests.get(url)

        data = self.__tableExtractor(r, "per_poss_stats")

        data["Year"] = year

        return data

    def advancedStats(self, year: int) -> pd.DataFrame:
        url = self.__baseURL + "NBA_{}_advanced.html".format(year)
        r = requests.get(url)

        data = self.__tableExtractor(r, "advanced_stats")

        data["Year"] = year

        return data


class Teams:
    def __init__(self, type: str) -> None:
        self.__baseURL = "https://www.basketball-reference.com"
        if type == "regular":
            self.__baseURL += "/leagues/"
        elif type == "playoffs":
            self.__baseURL += "/playoffs/"
        else:
            return None

    def __tableExtractor(self, mode: str, year: int) -> pd.DataFrame:
        url = self.__baseURL + "NBA_{}.html".format(year)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        table = soup.find(id=mode)

        if table == None:
            soup = BeautifulSoup("\n".join(soup.find_all(text=Comment)), "lxml")

        table = soup.find(id=mode)

        thead = table.find("thead").text.strip().split(" ")
        tbody = table.find("tbody")
        tableRows = tbody.find_all("tr")

        rows = []

        for tableRow in tableRows:
            row = []
            th = tableRow.find("th").text.strip()
            row.append(th)

            td = tableRow.find_all("td")

            for t in td:
                row.append(t.text.strip())

            rows.append(row)

        data = pd.DataFrame(rows, columns=thead)

        data["Year"] = year

        return data

    def totalStats(self, year: int) -> pd.DataFrame:
        return self.__tableExtractor(mode="totals-team", year=year)

    def perGameStats(self, year: int) -> pd.DataFrame:
        return self.__tableExtractor(mode="per_game-team", year=year)

    def perPossStats(self, year: int) -> pd.DataFrame:
        return self.__tableExtractor(mode="per_poss-team", year=year)

    def __conferenceTableRemover(self, table) -> pd.DataFrame:
        columns = ["Team"] + table.find("thead").text.strip().split("\n")[1:]

        eTableRows = table.find("tbody").find_all("tr")

        eRows = []

        for tableRow in eTableRows:
            row = []
            th = tableRow.find("th").text.strip()
            row.append(th)
            trs = tableRow.find_all("td")

            for tr in trs:
                row.append(tr.text)

            eRows.append(row)

        conf = pd.DataFrame(eRows, columns=columns)
        return conf

    def conferenceStandings(self, year: int) -> pd.DataFrame:
        url = "https://www.basketball-reference.com/leagues/NBA_{}.html".format(year)

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "lxml")
        remove = soup.find_all("tr", class_="thead")

        for r in remove:
            r.decompose()

        eTable = soup.find("table", id="divs_standings_E")
        wTable = soup.find("table", id="divs_standings_W")
        eConf = self.__conferenceTableRemover(eTable)
        wConf = self.__conferenceTableRemover(wTable)
        eConf["conf"] = "E"
        wConf["conf"] = "W"

        data = pd.concat([eConf, wConf]).reset_index()

        del data["index"]
        data["Year"] = year
        return data

    def removeHyphen(data:pd.DataFrame) -> pd.DataFrame:
        data = data.replace(to_replace="—", value=None)

        columns = data.columns.to_list()

        for column in columns:
            try:
                data[column] = data[column].astype(float)
            except:
                pass
        return data
