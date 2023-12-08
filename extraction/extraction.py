import requests
import pandas as pd
from bs4 import BeautifulSoup, Comment
from tqdm import tqdm
from time import sleep
from random import randint


class Players:
    def __init__(self, type: str) -> None:
        self.__baseURL = "https://www.basketball-reference.com/"
        self.type = type
        if self.type == "regular":
            self.__baseURL += "leagues/"
        elif self.type == "playoffs":
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
        columns = [column.strip() for column in columns]
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
        try:
            unwantedColumns = [""]
            for unwanted in unwantedColumns:
                index = data.columns.get_loc(unwanted)
                data = data.drop(data.columns[index], axis=1)
        except:
            pass
        data["is_regular"] = self.type == "regular"
        return data

    def totalStats(self, year: int) -> pd.DataFrame:
        try:
            url = self.__baseURL + "NBA_{}_totals.html".format(year)
            r = requests.get(url)
            data = self.__tableExtractor(r, "totals_stats")

            data["Year"] = year

            return data
        except:
            return None

    def perGameStats(self, year: int) -> pd.DataFrame:
        try:
            url = self.__baseURL + "NBA_{}_per_game.html".format(year)

            r = requests.get(url)
            data = self.__tableExtractor(r, "per_game_stats")

            data["Year"] = year

            return data
        except:
            return None

    def perMinuteStats(self, year: int) -> pd.DataFrame:
        try:
            url = self.__baseURL + "NBA_{}_per_minute.html".format(year)

            r = requests.get(url)

            data = self.__tableExtractor(r, "per_minute_stats")

            data["Year"] = year

            return data
        except:
            return None

    def perPossessionStats(self, year: int) -> pd.DataFrame:
        try:
            url = self.__baseURL + "NBA_{}_per_poss.html".format(year)
            r = requests.get(url)

            data = self.__tableExtractor(r, "per_poss_stats")

            data["Year"] = year
            return data
        except:
            return None

    def advancedStats(self, year: int) -> pd.DataFrame:
        try:
            url = self.__baseURL + "NBA_{}_advanced.html".format(year)
            r = requests.get(url)

            data = self.__tableExtractor(r, "advanced_stats")

            data["Year"] = year

            return data
        except:
            return None


class Teams:
    def __init__(self, type: str) -> None:
        self.__baseURL = "https://www.basketball-reference.com"
        self.type = type
        if self.type == "regular":
            self.__baseURL += "/leagues/"
        elif self.type == "playoffs":
            self.__baseURL += "/playoffs/"
        else:
            return None

    def __tableExtractor(self, mode: str, year: int) -> pd.DataFrame:
        url = self.__baseURL + "NBA_{}.html".format(year)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        table = soup.find(id=mode)

        if table == None:
            soup = BeautifulSoup("\n".join(soup.find_all(string=Comment)), "lxml")

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
        data["is_regular"] = self.type == "regular"
        data["Year"] = year

        return data

    def totalStats(self, year: int) -> pd.DataFrame:
        try:
            return self.__tableExtractor(mode="totals-team", year=year)

        except:
            return None

    def perGameStats(self, year: int) -> pd.DataFrame:
        try:
            return self.__tableExtractor(mode="per_game-team", year=year)
        except:
            return None

    def perPossStats(self, year: int) -> pd.DataFrame:
        try:
            return self.__tableExtractor(mode="per_poss-team", year=year)
        except:
            return None

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
        url = (
            "https://www.basketball-reference.com/leagues/NBA_{}_standings.html".format(
                year
            )
        )

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


class Games:
    def __init__(self) -> None:
        self.baseURL = "https://www.basketball-reference.com/"

    def monthlySchedule(self, url: str) -> pd.DataFrame:
        url = self.baseURL + url
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find("table", id="schedule")
        thead = table.find("thead").text.strip().split("\n")

        n = len(thead)

        c = 1
        for i in range(n):
            if thead[i] == "PTS" and c == 1:
                thead[i] = "VPTS"
                c += 1

        tbody = table.find("tbody")

        trs = tbody.find_all("tr")

        rows = []

        for tr in trs:
            th = tr.find("th").text.strip()
            row = []

            row.append(th)
            tds = tr.find_all("td")

            for td in tds:
                row.append(td.text.strip())
            rows.append(row)

        data = pd.DataFrame(rows, columns=thead)
        unwanted = ["Start (ET)", "\xa0", "\xa0"]

        for u in unwanted:
            try:
                data = data.drop(columns=u, axis=1)
            except:
                pass

        oldColumns = data.columns.to_list()
        requiredColumns = [
            "Date",
            "Visitor",
            "VPoints",
            "Home",
            "HPoints",
            "Attend",
            "Arena",
            "Notes",
        ]
        renameCols = dict.fromkeys(oldColumns, None)

        for i in range(len(oldColumns)):
            renameCols[oldColumns[i]] = requiredColumns[i]

        data = data.rename(columns=renameCols)

        return data

    def seasonSchedule(self, year: int) -> pd.DataFrame:
        url = self.baseURL + "leagues/NBA_{}_games.html".format(year)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        div_element = soup.find("div", class_="filter")

        urls = div_element.find_all("a", href=True)

        dataList = []

        for month in tqdm(urls):
            dataList.append(self.monthlySchedule(month["href"]))
            sleep(randint(5, 10))

        data = pd.concat(dataList)

        data = data.drop("Notes", axis=1)
        return data

    def playoffsDates(self, dateRange) -> pd.DataFrame:
        url = """
        https://www.basketball-reference.com/playoffs/series.html#playoffs_series
        """

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find(id="playoffs_series")
        tbody = table.find("tbody")

        trs = tbody.find_all("tr")
        rows = []

        for tr in trs:
            row = []
            th = tr.find("th").text.strip()
            row.append(th)

            tds = tr.find_all("td")

            for td in tds:
                row.append(td.text)

            rows.append(row)

        data = pd.DataFrame(rows)
        data = data[data[1] == "NBA"]

        data[3] = data[3].replace("\s+\-.+", "", regex=True)
        data[3] = data[3] + ", " + data[0].astype(str)
        data[3] = pd.to_datetime(data[3], format="%b %d, %Y")
        rows = []
        for year in range(*dateRange):
            smallData = data[data[3].dt.year == year]
            row = [year, smallData[3].min()]

            rows.append(row)

        return pd.DataFrame(rows, columns=["year", "start_date"])
