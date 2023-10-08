import requests
from os.path import join
import pandas as pd
from bs4 import BeautifulSoup, Comment


class Players:
    def __init__(self) -> None:
        self.baseURL = "https://www.basketball-reference.com/"
        self.regular = self.baseURL + "leagues"
        self.playoffs = self.baseURL + "playoffs"

    def __tableExtractor(self, table) -> pd.DataFrame:
        # extract columns of the table from html
        columns = table.find("thead").text.strip().split("\n")

        # remove unwanted rows from table (redundant column names present in table)
        remove = table.find_all("tr", class_="thead")
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

        return data

    def perGameStats(self, type: str, year: int) -> pd.DataFrame:
        # regular or playoffs data
        if type == "regular":
            url = self.regular
        elif type == "playoffs":
            url = self.playoffs
        else:
            return None

        # create url for the page
        url += "/NBA_{}_per_game.html".format(year)

        # request html
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")

        # locate table in html
        table = soup.find("table", id="per_game_stats")

        data = self.__tableExtractor(table)

        data["Year"] = year
        return data

    def totalStats(self, type: str, year: int) -> pd.DataFrame:
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
        table = soup.find("table", id="totals_stats")

        data = self.__tableExtractor(table)

        data["Year"] = year
        return data

    def per36minsStats(self, type: str, year: int) -> pd.DataFrame:
        # regular or playoffs data
        if type == "regular":
            url = self.regular
        elif type == "playoffs":
            url = self.playoffs
        else:
            return None

        # create url for the page
        url += "/NBA_{}_per_minute.html".format(year)

        # request html
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")

        # locate table in html
        table = soup.find("table", id="per_minute_stats")

        data = self.__tableExtractor(table)

        data["Year"] = year
        return data

    def per100Possessions(self, type: str, year: int) -> pd.DataFrame:
        # regular or playoffs data
        if type == "regular":
            url = self.regular
        elif type == "playoffs":
            url = self.playoffs
        else:
            return None

        # create url for the page
        url += "/NBA_{}_per_poss.html".format(year)

        # request html
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")

        # locate table in html
        table = soup.find("table", id="per_poss_stats")

        data = self.__tableExtractor(table)

        data["Year"] = year
        return data

    def advancedStats(self, type: str, year: int) -> pd.DataFrame:
        # regular or playoffs data
        if type == "regular":
            url = self.regular
        elif type == "playoffs":
            url = self.playoffs
        else:
            return None

        # create url for the page
        url += "/NBA_{}_advanced.html".format(year)

        # request html
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")

        # locate table in html
        table = soup.find("table", id="advanced_stats")

        data = self.__tableExtractor(table)

        data["Year"] = year
        return data


class Teams:
    def __init__(self, type: str) -> None:
        self.baseURL = "https://www.basketball-reference.com/"

        if type == "regular":
            self.baseURL += "leagues/"
        elif type == "playoffs":
            self.baseURL += "playoffs/"
        else:
            return None

    def __tableExtractor(self, table) -> pd.DataFrame:
        columns = table.find("thead").text.strip().split(" ")

        tbody = table.find("tbody")

        remove = tbody.find_all("tr", class_="thead")

        for r in remove:
            r.decompose()

        tableRows = tbody.find_all("tr")
        rows = []
        for tableRow in tableRows:
            row = []
            th = tableRow.find("th")
            row.append(th.text)
            td = tableRow.find_all("td")

            for t in td:
                row.append(t.text)
            rows.append(row)

        data = pd.DataFrame(rows, columns=columns)

        return data

    def totalStats(self, year: int) -> pd.DataFrame:
        url = self.baseURL + "NBA_{}.html".format(year)

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        table = soup.find(id="totals-team")

        data = self.__tableExtractor(table)
        data["Year"] = year
        return data

    def perGameStats(self, year: int) -> pd.DataFrame:
        url = self.baseURL + "NBA_{}.html".format(year)

        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find(id="per_game-team")
        data = self.__tableExtractor(table)
        data["Year"] = year
        return data

    # doesn't work. potential problem with website
    def perPossStats(self, year: int) -> pd.DataFrame:
        url = self.baseURL + "NBA_{}.html".format(year)

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "lxml")
        soup = BeautifulSoup("\n".join(soup.find_all(string=Comment)), "lxml")
        data = pd.read_html(url)

        for d in data:
            print(
                d,
                "\n------------------------------------------------------------------------------\n",
            )

        # print(soup)
        # return self.__tableExtractor(table)

    def extendedStandings(self, year: int) -> pd.DataFrame:
        url = self.baseURL + "NBA_{}_standings.html".format(year)

        r = requests.get(url)

        soup = BeautifulSoup(r.text, "lxml")
        soup = BeautifulSoup("\n".join(soup.find_all(string=Comment)), "lxml")
        table = soup.find(id="expanded_standings")
        thead = table.find("thead")
        trs = thead.find_all("tr")
        smallCols = trs[1].text.strip().split("\n")
        tbody = table.find("tbody")

        tableRows = tbody.find_all("tr")

        rows = []

        for tableRow in tableRows:
            row = []

            row.append(tableRow.find("th").text.strip())

            tds = tableRow.find_all("td")

            for td in tds:
                row.append(td.text.strip())

            rows.append(row)

        data = pd.DataFrame(rows, columns=smallCols)
        data["Year"] = year

        return data