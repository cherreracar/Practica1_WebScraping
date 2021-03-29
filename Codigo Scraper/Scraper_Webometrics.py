import requests
import pandas as pd

from bs4 import BeautifulSoup
from time import sleep
from random import randint

# Lists for data storage
Area_Ranking = []
World_Ranking = []
University_Web = []
University = []
Impact_Scores = []
Openness_Scores = []
Excellence_Scores = []

# Options for url_input.
dict_url = {0: "http://www.webometrics.info/en/North_america",
            1: "http://www.webometrics.info/en/Latin_America",
            2: "http://www.webometrics.info/en/Europe",
            3: "http://www.webometrics.info/en/Asia",
            4: "http://www.webometrics.info/en/Africa",
            5: "http://www.webometrics.info/en/Oceania"
            }

# User input.
url_option = int(input("Please choose the number that corresponds to the area whose ranking of universities you want "
                       "to obtain:\n 0: North America\n 1: " "Latin America\n 2: Europe\n 3: Asia\n 4: Africa\n 5: "
                       "Oceania\n"))

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
label = last_page_text[index1:index2+1]

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

        # Extracting Europe and World ranking position:
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
                University_Web.append(link)

    # Crawl rate (Avoiding saturating the web server)
    sleep(randint(3, 10))

# Generating data set with the scraped data.
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