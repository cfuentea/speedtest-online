from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def perform_test():
    path = "./chromedriver-linux64/chromedriver"
    service = Service(executable_path=path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("http://beta.speedtest.net")
    #print("ingresando a speedtest.net")
    time.sleep(10)
    start_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.start-button a.js-start-test'))
    )
    start_button.click()
    #print("realizando medicion de down/up  en speedtest")
    time.sleep(60)
    
    element = driver.find_element(By.CSS_SELECTOR,'div.overall-progress.visuallyhidden')
    summarized = element.text
    url=driver.current_url
    test_number= url.split('/')[-1]
    message = "Test finalizado. Puedes encontrar el test en: "
    url = ("https://www.speedtest.net/es/result/"+test_number).replace(" ","")
    print(message,url)
    return summarized

def clean_text(resumen):
    a = re.findall(r"\d+\.\d+", resumen)
    return a

summarized = perform_test()
array = clean_text(summarized)
download = array[0]
upload = array[1]
print("Velocidad de descarga:", download,'Mbps')
print("Velocidad de subida", upload,' Mbps')

