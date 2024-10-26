import json
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()


def save_cookies(cookies_file: str = "cookies") -> list[dict]:
    """
    Get cookies from current website and saves cookies to .json file
    """
    
    # Get cookies from current website
    cookies = driver.get_cookies()

    # Save cookies to .json file
    with open(f"cookies/{cookies_file}.json", 'w') as file:
        json.dump(cookies, file, indent=4)

    return cookies


def load_cookies(cookies_file: str = "cookies") -> list[dict]:
    """
    Get cookies from .json file and load them on current website
    """

    # Get cookies from .json file
    with open(f"cookies/{cookies_file}.json", 'r') as file:
        cookies = json.load(file)
    
    # Load cookies on current website
    for cookie in cookies:
        driver.add_cookie(cookie)

    return cookies


def upload_instagram() -> str:
    """
    Upload video to Instagram and returns the URL of the video
    """
    
    pass


def upload_tiktok() -> str:
    """
    Upload video to Tiktok and returns the URL of the video
    """

    pass


def upload_youtube(input_file: str = "generate_video_output", title: str = "test", article: str = "The quick brown fox jumps over the lazy dog. Lorem Ipsum is simply dummy text of the printing and typesetting industry.", link: str = "https://en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_article/", schedule_date: str | None = None, schedule_time: str | None = None) -> str:
    """
    Upload video to YouTube and returns the URL of the video
    """

    # Link
    driver.get("https://studio.youtube.com")
    if "youtube_cookies.json" in os.listdir():
        load_cookies("youtube_cookies")
    else:
        input("Press any key to continue after logging in: ")
        save_cookies("youtube_cookies")

    
    # Select upload
    driver.find_element(By.ID, "upload-icon").click()
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(f"media/{input_file}.mp4")
    time.sleep(1)

    # Input Details page
    video_url = driver.find_element(By.CLASS_NAME, "style-scope ytcp-video-info").text
    driver.find_elements(By.ID, "textbox")[0].send_keys(title)
    driver.find_elements(By.ID, "textbox")[1].send_keys(f"{article}/n/nLink:{link}")
    driver.find_element(By.ID, "next-button").click()
    time.sleep(1)

    # Input Video Elements page
    driver.find_element(By.ID, "next-button").click()
    time.sleep(1)

    # Input Checks page
    driver.find_element(By.ID, "next-button").click()
    time.sleep(1)

    # Input Visibility page
    driver.find_element(By.ID, "second-container-expand-button").click()
    driver.find_element(By.ID, "input-3").send_keys(schedule_date)
    driver.find_element(By.ID, "input-2").send_keys(schedule_time)
    driver.find_element(By.ID, "done-button").click()
    time.sleep(1)

    # Return URL
    return video_url


if __name__ == "__main__":
    upload_youtube()