import os
from time import sleep
from typing import List

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests


def creating_folders(name: str) -> None:
    """
    The function takes the class name as input and creates a directory if one does not exist at the moment.
    """
    if not os.path.isdir(name):
        os.mkdir(name)


def download_images(links: List[str], name: str) -> None:
    """
    The function accepts the class name and a list of links to images as input.
    A directory with the name of the class is created and, going through the list,
    it downloads images and saves them in the specified directory.
    """
    creating_folders(os.path.join("dataset", name))
    count: int = 0
    page: str = ""
    for link in links:
        while page == "":
            try:
                sleep(5)
                response = requests.get(link, verify=False).content
                with open(
                    os.path.join("dataset", name, f"{str(count).zfill(4)}.jpg"), "wb"
                ) as f:
                    f.write(response)
                count += 1
                break
            except:
                print("Error.Waiting 6s")
                sleep(6)
                print("Now try reconnecting")
                continue


def get_images(name: str, num_img: int) -> List[str]:
    """
    The function takes as input the name of the class and the number of images to be parsed.
    A link opens in the browser and with the help of the element code there are links to images that are saved to the list.
    """
    url: str = f"https://yandex.ru/images/search?text={name}"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "a.serp-item__link").click()
    elem1: str = driver.find_element(By.CLASS_NAME, "MMImage-Origin").get_attribute(
        "src"
    )
    links: List[str] = [elem1]
    for _ in range(num_img):
        try:
            sleep(1)
            driver.find_element(
                By.CLASS_NAME, "MediaViewer_theme_fiji-ButtonNext"
            ).click()
            link: str = driver.find_element(
                By.CLASS_NAME, "MMImage-Origin"
            ).get_attribute("src")
            links.append(link)
        except:
            continue
    driver.close()
    return links


def main(name1: str, name2: str, num_img: int) -> None:
    creating_folders("dataset")
    download_images(get_images(name1, num_img), name1)
    download_images(get_images(name2, num_img), name2)


if __name__ == "__main__":
    main("rose", "tulip", 9)
