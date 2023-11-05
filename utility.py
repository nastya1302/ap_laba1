import os
import time
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random import randint

def creating_folders(names: list):
    if not os.path.isdir(names[0]) and not os.path.isdir(names[1]):
        os.makedirs(names[0])
        os.makedirs(names[1])

def download_images(links: list, name: str):
    os.chdir(name)
    for link in links:
        response = requests.get(link).content
        with open(f'image{randint(0,100)}.jpg', "wb") as f:
           f.write(response)

def get_images(name: str) -> list:
    url = f"https://yandex.ru/images/search?text={name}"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'div.serp-item__preview a.serp-item__link').click()
    elem1 = driver.find_element(By.CLASS_NAME, "MMImage-Origin").get_attribute('src')
    list = [elem1]
    for i in range(10):
            try:
                time.sleep(2)
                button = driver.find_element(By.CLASS_NAME, "MediaViewer_theme_fiji-ButtonNext").click()                
                link = driver.find_element(By.CLASS_NAME, "MMImage-Origin").get_attribute('src')
                list.append(link)
            except:
                continue
    driver.close()

def main() -> None:
    name1, name2 = "rose", "tulip"
    if not os.path.isdir("dataset"):
        os.mkdir("dataset")
    os.chdir("dataset")
    creating_folders((name1, name2))
    download_images(get_images(name1), name1)

    #print(list)
    #print("Текущая директория изменилась на folder:", os.getcwd())

if __name__ == "__main__":
    main()