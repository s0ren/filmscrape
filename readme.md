# WebScraping

## Brug Selenium i stedet for requests

Selenium er lavet til at fjernstyre webbrowsere fra et program, f.eks. python.
Selenium kan også bruge både Firefoc, Edge og Chrome (samt Chromium) og muligvis også flere andre. Det sker igennem modulet WebDriver.

## Eksempel

Se også afsnittet om [Installation](#installation) nedenfor. \
Her vil vises hvordan Selenium bruges med en container. Som egentlig er _remote_ mode, og derfor også kunne være en dedikeret maskine.

#### Start Chrome standalone i Docker

    docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.27.0-20241204

Se hvad der foregår på selenium grid'ets portal på <http://localhost:4444/>

#### Mindste mulige eksempel

```python
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)

url = r"https://www.example.com/"
driver.get(url)
html = driver.page_source

driver.quit()

print(html)
```
Se også _<hello_selenium.py>_

Se også disse sider:
* Om at tilslutte til Selenium grid 
    * <https://medium.com/@ethan.han.qa/how-to-connect-selenium-grid-with-python-35bb460803f4>
* om at bruge Selenium til scraping
    * <https://medium.com/@dmautomationqa/a-complete-guide-to-web-scraping-with-selenium-python-in-2024-4c856890be68>
    * https://www.zenrows.com/blog/selenium-python-web-scraping#export-data

## Installation

### Python lib

Der skal bruges et enkel library, som installeres med _pip_:

    pip install selenium    

Det er også en god ide at tilføje `selenium` til _requirements.txt_.

### WebDriver eller container

Det _er_ muligt at installere webdriveren lokalt, men for chrome betyder det at man skal finde en version der svarer til den installerede browser. \
Se <https://www.zenrows.com/blog/selenium-python-web-scraping#getting-started> \
Det lader ikke til at være muligt i mit tilfælde, lige pt. (12. december 2024), da jeg har Chrome version 131.0.6778.109, og der er ikke en version af webdriveren, med samme version, til windows... suk 

Hvis det ikke er muligt at installere en WebDriver (til din forestrukne browser) direkte på sit system, er klare fordele ved at køre denne i en docker container. Det kræver ikke at man sætter hele sit projekt op i en container, bare browseren/webdriveren.  
Man kan konfigurere et helt grid af browsercontainere med flere browsere, via docker-compose.  
Det er måske en ide hvis man skal skrabe massivt mange data, men især nok interessant for dem der skal teste om en web-applikation fungerer korrekt. Også hvis man tester løbende i CI/CL.

Docker desktop skal være installeret på systemet. \
Se <https://www.docker.com/get-started/>

Se mere om Selenium i containere fra den oprindelige kilde, på <https://github.com/SeleniumHQ/docker-selenium/blob/trunk/README.md>

Her i projektet har jeg kopieret fra ovenstående, *.bat filer med kommandoer til at starte containere med _Chrome_, _Edge_ og _Firefox_. 

Se: 
- <./selenium_standalone_chrome.bat>, 
- <./selenium_standalone_edge.bat> og 
- <./selenium_standalone_firefox.bat>.

> **Bemærk** man kan kun køre en _standalone_ container med en browser adgangen, fordi de lytter på port 4444. \
Hvis du vil have flere skal du bruge et grid, som der er en meget simpel version af i 