import time

from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()


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
    time.sleep(1)

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
    pass