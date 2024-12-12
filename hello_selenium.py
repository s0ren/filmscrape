from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)

url = r"https://www.example.com/"
driver.get(url)

# vent til siden er loaded i browseren
# Sætter Selenium Webdriver til at vente på at den annonyme function `return document.readyState`, afslutter i browseren
WebDriverWait(driver, 10).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)

html = driver.page_source
driver.quit()
print(html)
