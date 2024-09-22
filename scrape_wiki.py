import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


ROOT_URL = "https://en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_article/"
driver = webdriver.Chrome()


def open_wiki(day: int | None = None, month: str | None = None, year: int | None = None) -> None:
    """
    Default date is current date unless argument given

    Date formatting should be ("8", "August", "2024")
    """

    day = datetime.now().strftime("%#d") if day is None else day
    month = datetime.now().strftime("%B") if month is None else month
    year = datetime.now().strftime("%Y") if year is None else year

    driver.get(f"{ROOT_URL}{month}_{day},_{year}")
    time.sleep(1)


# consider using https://en.wikipedia.org/wiki/Special:Random
def get_wiki() -> list[str]:
    article = driver.find_element(By.XPATH, "//*[@id='mw-content-text']/div[1]").text
    
    # Removes extra text
    article = article.split(" (Full article...)")[0]
    article = article.split("\n")[1] if "\n" in article else article

    driver.find_element(By.XPATH, "//*[@id='mw-content-text']/div[1]/p/b/a").click()
    time.sleep(1)

    title = driver.find_element(By.XPATH, "//*[@id='firstHeading']").text    
    link = driver.current_url
    driver.quit()

    print(f"{title}\n{article}\n{link}")

    return title, article, link


if __name__ == "__main__":
    open_wiki()