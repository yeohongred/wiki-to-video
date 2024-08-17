import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


ROOT_URL = f"https://en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_article/"
driver = webdriver.Chrome()


# Default date is current date unless argument given
# Date formatting should be ("8", "August", "2024")
def open_wiki(day=None, month=None, year=None):
    day = datetime.now().strftime("%#d") if day == None else day
    month = datetime.now().strftime("%B") if month == None else month
    year = datetime.now().strftime("%Y") if year == None else year

    driver.get(f"{ROOT_URL}{month}_{day},_{year}")
    time.sleep(1)


def get_wiki(driver=driver):
    article = driver.find_element(By.XPATH, "//*[@id='mw-content-text']/div[1]").text
    # Removes extra text
    article = article.split(" (Full article...)")[0]
    article = article.split("\n")[1] if "\n" in article else article

    driver.find_element(By.XPATH, "//*[@id='mw-content-text']/div[1]/p/b/a").click()
    time.sleep(1)

    title = driver.find_element(By.XPATH, "//*[@id='firstHeading']").text    
    link = driver.current_url

    print(f"{title}\n{article}\n{link}")

    return title, article, link


def close_wiki():
    driver.quit()