import requests
import pandas as pd
import waybackpy

from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from random import randint

# Lists for data storage
Area_Ranking = []
World_Ranking = []
University_Web = []
University = []
Impact_Scores = []
Openness_Scores = []
Excellence_Scores = []
Year = []

# Options for url_input.
dict_url = {0: "http://www.webometrics.info/en/North_america",
            1: "http://www.webometrics.info/en/Latin_America",
            2: "http://www.webometrics.info/en/Europe",
            3: "http://www.webometrics.info/en/Asia",
            4: "http://www.webometrics.info/en/Africa",
            5: "http://www.webometrics.info/en/Oceania"
            }

# User input.
scraping_option = int(input("Please choose one option:\n 0: Obtain current ranking\n 1:  Obtain historical ranking "
                            "data since 2012 about top 100 universities.\n\n"))

url_option = int(input("Please choose the number that corresponds to the area whose ranking of universities you want "
                       "to obtain:\n 0: North America\n 1: " "Latin America\n 2: Europe\n 3: Asia\n 4: Africa\n 5: "
                       "Oceania\n\n"))

# Scraping Current Ranking.
if scraping_option == 0:
    # Obtaining web content to calculate total pages.
    input_url = dict_url[int(url_option)]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}
    page = requests.get(input_url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    # Searching for total pages in the HTML.
    last_page_text = str(soup.find(title="Go to last page")['href'])
    index1 = last_page_text.index('?')
    index2 = last_page_text.index('=')
    total_page = int(last_page_text[index2 + 1:])

    # Obtaining the label for generating all the links.
    label = last_page_text[index1:index2 + 1]

    # Creating the url list to scraping.
    url_list = [input_url + str(label) + str(i) for i in range(1, total_page + 1)]
    url_list.insert(0, input_url)

    print("Generating your csv file, please wait...")

    # Start of scraping
    for url in url_list:

        # Get web content
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        # Scraping the table variables
        for tr in soup.find_all('tr')[1:]:

            tag_td = tr.find_all('td')

            # Extracting Region and World ranking position:
            Area_Ranking.append(int(tag_td[0].text))
            World_Ranking.append(int(tag_td[1].text))

            # Extracting university's name:
            University.append(tag_td[2].text)

            # Extracting Impact, Openness and Excellence scores:
            Impact_Scores.append(int(tag_td[5].text))
            Openness_Scores.append(int(tag_td[6].text))
            Excellence_Scores.append(int(tag_td[7].text))

            # Extracting the university webs.
            tag_a = tr.find_all('a')
            for link in tag_a:
                link = link.get('href')
                if "detalles" not in link:
                    index1 = link.index('//')
                    total_page = int(last_page_text[index2 + 1:])
                    University_Web.append(link)

        # Crawl rate (Avoiding saturating the web server)
        sleep(randint(3, 10))

# Scraping Historical data.
elif scraping_option == 1:
    print("Generating your csv file, please wait...")

    # Obtaining archive URLs from Wayback Machine.
    input_url = dict_url[int(url_option)]
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
    wayback = waybackpy.Url(input_url, user_agent)
    now = datetime.now()
    year_limit = now.year
    wayback_urls = []

    for i in range(2012, year_limit):
        archive = wayback.near(year=i, month=12)
        wayback_urls.append(archive.archive_url)

    # Variable Year.
    for i in range(2012, year_limit):
        for j in range(1, 101):
            Year.append(i)

    # Start of scraping
    for url in wayback_urls:

        # Get web content
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        # Scraping the table variables
        target_table = soup.find("table", attrs={"class": "sticky-enabled"})
        for tr in target_table.find_all('tr')[1:]:

            tag_td = tr.find_all('td')

            # Extracting Region and World ranking position:
            Area_Ranking.append(int(tag_td[0].text))
            World_Ranking.append(int(tag_td[1].text))

            # Extracting university's name:
            University.append(tag_td[2].text)

            # Extracting Impact, Openness and Excellence scores:
            Impact_Scores.append(int(tag_td[6].text))
            Openness_Scores.append(int(tag_td[7].text))
            Excellence_Scores.append(int(tag_td[8].text))

            # Extracting the university webs.
            tag_a = tr.find_all('a')
            for link in tag_a:
                link = link.get('href')
                index = link.rindex("//")
                if "detalles" not in link:
                    final_link = link[index + 2:len(link) - 1]
                    University_Web.append(final_link)

        # Crawl rate (Avoiding saturating the web server)
        sleep(randint(3, 10))

# Generating data set with the scraped data.

# CSV for Current Ranking.
if scraping_option == 0:
    dataset = pd.DataFrame({
        'Name': University,
        'Web': University_Web,
        'Regional_ranking': Area_Ranking,
        'World_ranking': World_Ranking,
        'Impact_score': Impact_Scores,
        'Openness_score': Openness_Scores,
        'Excellence_core': Excellence_Scores,
    })

    # Exporting data set to a CSV file.
    if url_option == 0:
        dataset.to_csv('UniversityRanking_NorthAmerica.csv', index=False, encoding="utf-8-sig")

    elif url_option == 1:
        dataset.to_csv('UniversityRanking_LatinAmerica.csv', index=False, encoding="utf-8-sig")

    elif url_option == 2:
        dataset.to_csv('UniversityRanking_Europe.csv', index=False, encoding="utf-8-sig")

    elif url_option == 3:
        dataset.to_csv('UniversityRanking_Asia.csv', index=False, encoding="utf-8-sig")

    elif url_option == 4:
        dataset.to_csv('UniversityRanking_Africa.csv', index=False, encoding="utf-8-sig")

    elif url_option == 5:
        dataset.to_csv('UniversityRanking_Oceania.csv', index=False, encoding="utf-8-sig")

# CSV for Historical data.
if scraping_option == 1:
    dataset = pd.DataFrame({
        'Name': University,
        'Web': University_Web,
        'Regional_ranking': Area_Ranking,
        'World_ranking': World_Ranking,
        'Impact_score': Impact_Scores,
        'Openness_score': Openness_Scores,
        'Excellence_core': Excellence_Scores,
        'Year': Year,
    })

    # Exporting data set to a CSV file.
    if url_option == 0:
        dataset.to_csv('Historic_NorthAmerica.csv', index=False, encoding="utf-8-sig")

    elif url_option == 1:
        dataset.to_csv('Historic_LatinAmerica.csv', index=False, encoding="utf-8-sig")

    elif url_option == 2:
        dataset.to_csv('Historic_Europe.csv', index=False, encoding="utf-8-sig")

    elif url_option == 3:
        dataset.to_csv('Historic_Asia.csv', index=False, encoding="utf-8-sig")

    elif url_option == 4:
        dataset.to_csv('Historic_Africa.csv', index=False, encoding="utf-8-sig")

    elif url_option == 5:
        dataset.to_csv('Historic_Oceania.csv', index=False, encoding="utf-8-sig")
