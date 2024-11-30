from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Constants
LOGIN_URL = "https://code.ptit.edu.vn/login"
TOTAL_PAGE = 3
LIMIT_SUBMIT = 20

#Path chromedriver
CHROME_DRIVER_PATH = "chromedriver.exe"

def initialize_driver(url = None):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    if url:
        driver.get(url)
    return driver