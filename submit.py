from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from AutoSubmit.file import load_abs_file

async def submit_assignment(driver, url):
    try:
        file_input = driver.find_element(By.ID, 'fileInput')
        abs_path_file = load_abs_file(url)
        if abs_path_file is not None:
            file_input.send_keys(abs_path_file)
            submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit__pad__btn')))
            submit_button.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            alert_div = driver.find_elements(By.CSS_SELECTOR, 'div.alert.alert-info')
            for alert in alert_div:
                if "Hôm nay bạn đã làm quá nhiều bài tập" in alert.text:
                    print("Thông báo: Bạn đã làm quá nhiều bài tập.")
                    driver.quit()
                    exit()
                    return
    
    except Exception as e:
        print(f"Failed to submit assignment because not find element: {e}")
