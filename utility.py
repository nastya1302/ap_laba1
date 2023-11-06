import os
import time
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def creating_folders(name: str):
    if not os.path.isdir(name):
        os.mkdir(name)

def download_images(links: list, name: str):
    creating_folders(f"dataset/{name}")
    count = 0
    page = ''
    for link in links:
        while page == '':
            try:
                time.sleep(5)
                response = requests.get(link, verify=False).content
                with open(f'dataset/{name}/{str(count).zfill(4)}.jpg', "wb") as f:
                    f.write(response)
                count = count+1
                break
            except: 
                print("Error.Waiting 6s")
                time.sleep(6)
                print("Now try reconnecting")
                continue

def get_images(name: str) -> list:
    url = f"https://yandex.ru/images/search?text={name}"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'div.serp-item__preview a.serp-item__link').click()
    elem1 = driver.find_element(By.CLASS_NAME, "MMImage-Origin").get_attribute('src')
    list = [elem1]
    for i in range(1000):
            try:
                time.sleep(1)
                button = driver.find_element(By.CLASS_NAME, "MediaViewer_theme_fiji-ButtonNext").click()                
                link = driver.find_element(By.CLASS_NAME, "MMImage-Origin").get_attribute('src')
                list.append(link)
            except:
                continue
    driver.close()
    return list

def main() -> None:
    name1, name2 = "rose", "tulip"
    creating_folders("dataset")
    download_images(get_images(name1), name1)
    time.sleep(5)
    download_images(get_images(name2), name2)
    
if __name__ == "__main__":
    main()