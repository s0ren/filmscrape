from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
# til at parse url
from urllib.parse import unquote_plus, urlparse, quote, parse_qs, parse_qsl
# til at gemme data
import csv

import urllib

options = webdriver.ChromeOptions()
driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=options)

### TODO: opdel i passende funktioner, for bedre design og genbrug!

# Her er url'en dekonstrueret manuelt
# _Bemærk_ at de underlige '%5B' og '%5D' er '[' og ']', som er _urlencoded_, dvs konverteret til tegnets ascii-værdi i hex.
#   Herunder har jeg manuelt konverteret tilbage til '[]'. Ovenfor er det sket automatisk...
base_url = "https://www.dfi.dk/search"
p = { 
    'additional[subsection]'        : 4158,
    'additional[grouping]'          : 'filmdatabase_movie',
    'additional[api_only]'          : 'true',
    'additional[hide_back_button]'  : 'true',
    'additional[allow_empty_query]' : 'true',
    'query'                         : '',
    'filters[Category]'             : '',
    'filters[SubCategory]'          : '',
    'filters[Keywords]'             : '',
    'filters[ProductionCountry]'    : 'Danmark',
    'filters[PremiereDate][start]'  : '2000',
    'filters[PremiereDate][end]'    : '2025',
    'page'                          : '1'
}

url = base_url + '?' + urllib.parse.urlencode(p)

driver.get(url)
# vent til siden er loaded i browseren
# Sætter Selenium Webdriver til at vente på at den annonyme function `return document.readyState`, afslutter i browseren
WebDriverWait(driver, 10).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)
html = driver.page_source

film_liste = []

hasNext = True

while hasNext:

    soup = BeautifulSoup(html, 'html.parser')

    if soup.css.select_one(".pager__item--next"):
        next_url = base_url + soup.css.select_one(".pager__item--next")['href'] 
        hasNext = True
    else:
        hasNext = False

    # print(f'next_url: {next_url}')

    # alle af class 'list__item'
    films = soup.css.select(".list__item")
    for film in films:
        try:
            #  check hvert element for om det findes, og brug en tom streng alternativt...
            film_data = {
                "titel":            film.css.select_one(".beside__title").string,
                "instruktør":       ', '.join(film.css.select_one(".beside__subtitle").string.split(', ')[:-1]),
                "årstal":           film.css.select_one(".beside__subtitle").string.split(', ')[-1],
                "beskrivelse":      film.css.select_one(".beside__text").string if film.css.select_one(".beside__text") else ''
            }
            # film_data = {}


            film_liste.append(film_data)
        except Exception as e:
            print(f"Exception {e}, med film {film}")

    print(f'Hentede {len(films)} film, {len(film_liste)} ialt')
    
    driver.get(url)
    # vent til siden er loaded i browseren
    # Sætter Selenium Webdriver til at vente på at den annonyme function `return document.readyState`, afslutter i browseren
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    html = driver.page_source

driver.quit()

#  gem i cvs fil

with open('filmliste.csv', 'w', encoding='UTF8', newline='\n') as csv_file: # åbn file-handle til at skrive i. Auto close når vi forlader with block
    dw = csv.DictWriter(
        csv_file,               # det filehandle der skal skrivesa til
        film_liste[0].keys(),   # navne på felter fra `film`-dict der skal med i csv-filen. Vi tager alle.
        quoting=1               # tilføjer " " om alle værdier. F.eks. kan titel og beskrivelse indeholde komma (,)
        )
    dw.writeheader()
    dw.writerows(film_liste)


print(f'{len(film_liste)} film gemt i csv-fil.')