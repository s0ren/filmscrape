import requests
from bs4 import BeautifulSoup

# https://www.dfi.dk/search?additional%5Bsubsection%5D=4158&additional%5Bgrouping%5D=filmdatabase_movie&additional%5Bapi_only%5D=true&additional%5Bhide_back_button%5D=true&additional%5Ballow_empty_query%5D=true&query=&filters%5BCategory%5D=&filters%5BSubCategory%5D=&filters%5BKeywords%5D=&filters%5BProductionCountry%5D=Danmark&filters%5BPremiereDate%5D%5Bstart%5D=2000&filters%5BPremiereDate%5D%5Bend%5D=2024&page=1

raw_url = r"https://www.dfi.dk/search?additional%5Bsubsection%5D=4158&additional%5Bgrouping%5D=filmdatabase_movie&additional%5Bapi_only%5D=true&additional%5Bhide_back_button%5D=true&additional%5Ballow_empty_query%5D=true&query=&filters%5BCategory%5D=&filters%5BSubCategory%5D=&filters%5BKeywords%5D=&filters%5BProductionCountry%5D=Danmark&filters%5BPremiereDate%5D%5Bstart%5D=2000&filters%5BPremiereDate%5D%5Bend%5D=2024&page=1"
respons = requests.get(raw_url)

# base_url = "https://www.dfi.dk/search"

# p = { 'additional%5Bsubsection%5D' : 4158,
#       'additional%5Bgrouping%5D'=filmdatabase_movie
#       additional%5Bapi_only%5D=true
#       additional%5Bhide_back_button%5D=true
#       additional%5Ballow_empty_query%5D=true
#       query=&filters%5BCategory%5D=&filters%5BSubCategory%5D=&filters%5BKeywords%5D=&filters%5BProductionCountry%5D=Danmark&filters%5BPremiereDate%5D%5Bstart%5D=2000&filters%5BPremiereDate%5D%5Bend%5D=2024&page=1}


print(respons.status_code)
# print(respons.text)

soup = BeautifulSoup(respons.text, 'html.parser')

# alle af class 'list__item'

films = soup.css.select(".list__item")
print(films[0])
film_liste = []
for film in films:
    film_data = {
        "titel":            film.css.select_one(".beside__title").string,
        "instruktør": ',    '.join(film.css.select_one(".beside__subtitle").string.split(', ')[:-1]),
        "årstal":           film.css.select_one(".beside__subtitle").string.split(', ')[-1],
        "beskrivelse":      film.css.select_one(".beside__text").string
    }
    film_liste.append(film_data)

print(film_liste)

