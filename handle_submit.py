import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from selenium.webdriver.common.by import By

from submit import submit_assignment
from ultis.handle_string import is_valid_question_url


async def process_link(driver, url):
    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        await submit_assignment(driver, url)
        print(f"Processing URL: {url}, Title: {driver.title}")
        time.sleep(2)
    except Exception as e:
        print(f"Failed to process {url}: {e}")

async def handle(driver):
    total_page = config.TOTAL_PAGE
    urls = []
    try:
        for page in range(1, total_page+1):
            driver.get(f"https://code.ptit.edu.vn/student/question?page={page}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            lines = driver.find_elements(By.XPATH, "//tr[not(contains(@class, 'bg--10th'))]")
            for line in lines:
                link = line.find_element(By.XPATH, ".//a")
                url = link.get_attribute('href')

                if is_valid_question_url(url):
                    urls.append(url)

        for u in urls:
            print(u)
            await process_link(driver, u)


    except Exception as e:
        print(f"Failed to get assignment:)): {e}")
