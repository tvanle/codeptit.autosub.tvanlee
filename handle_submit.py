import time
import random
import logging
import json
import smtplib
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from file import load_abs_file
from ultis.handle_string import is_valid_question_url
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging to both console and file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="assignment_log.log", filemode='w')

# Log a message when the script starts
logging.info("Script started")

async def process_link(driver, url):
    try:
        driver.get(url)
        logging.info(f"Visiting URL: {url}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        await submit_assignment(driver, url)
        logging.info(f"Processing URL: {url}, Title: {driver.title}")

        # Sleep with a random delay to avoid triggering anti-bot systems
        time.sleep(random.randint(1, 3))
    except Exception as e:
        logging.error(f"Failed to process {url}: {e}")

async def handle(driver):
    total_page = config.TOTAL_PAGE
    urls = []
    try:
        for page in range(1, total_page+1):
            logging.info(f"Fetching page {page}...")
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

        logging.info(f"Found {len(urls)} URLs to process.")
        for u in urls:
            logging.info(f"Processing URL: {u}")
            await process_link(driver, u)
        # Save the processed URLs to a file
        await save_processed_urls(urls)

    except Exception as e:
        logging.error(f"Failed to get assignment links: {e}")

async def submit_assignment(driver, url):
    try:
        logging.info(f"Attempting to submit assignment for {url}...")

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
                    logging.warning("Thông báo: Bạn đã làm quá nhiều bài tập.")
                    driver.quit()
                    exit()
                    return

    except Exception as e:
        logging.error(f"Failed to submit assignment due to missing elements: {e}")
        retry_submission(driver, url)

def retry_submission(driver, url, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            logging.info(f"Retrying submission for {url}, attempt {attempt + 1}...")
            submit_assignment(driver, url)
            break
        except Exception as e:
            logging.error(f"Retry {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(random.randint(2, 5))  # Random delay before retry

async def auto_login(driver, username, password) -> bool:
    try:
        logging.info("Attempting to login...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains("student/question")
        )
        logging.info("Login successful")
        return True
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return False

async def track_progress(driver):
    try:
        # This function tracks the progress of assignments being submitted.
        completed_assignments = 0
        total_assignments = config.TOTAL_PAGE * 10  # Assuming 10 questions per page
        logging.info("Tracking progress of assignments...")
        for i in range(total_assignments):
            # Simulate progress tracking (this part can be expanded)
            completed_assignments += 1
            logging.info(f"Completed: {completed_assignments}/{total_assignments}")
            time.sleep(1)  # Sleep to simulate time between submissions

    except Exception as e:
        logging.error(f"Error while tracking progress: {e}")

async def save_session_data(driver):
    try:
        # Simulating the function to save session data such as cookies for future sessions
        cookies = driver.get_cookies()
        logging.info(f"Saving session cookies: {cookies}")
        with open('session_cookies.json', 'w') as file:
            json.dump(cookies, file)
        logging.info("Session data saved successfully")
    except Exception as e:
        logging.error(f"Error while saving session data: {e}")

async def load_session_data(driver):
    try:
        # Simulating the function to load session data from saved cookies
        logging.info("Loading session data...")
        with open('session_cookies.json', 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        logging.info("Session data loaded successfully")
    except Exception as e:
        logging.error(f"Error while loading session data: {e}")

async def random_wait_time():
    # This function introduces a random wait time between actions to simulate human-like behavior.
    wait_time = random.randint(2, 5)
    logging.info(f"Waiting for {wait_time} seconds...")
    time.sleep(wait_time)

async def send_feedback(driver, feedback="Task completed"):
    try:
        # Simulate sending feedback after completing a task
        feedback_input = driver.find_element(By.ID, 'feedbackInput')
        feedback_input.clear()
        feedback_input.send_keys(feedback)
        submit_button = driver.find_element(By.ID, 'feedbackSubmitButton')
        submit_button.click()
        logging.info(f"Feedback sent: {feedback}")
    except Exception as e:
        logging.error(f"Error while sending feedback: {e}")

async def save_processed_urls(urls):
    try:
        # Save processed URLs to a file
        with open("processed_urls.json", "w") as file:
            json.dump(urls, file)
        logging.info(f"Processed URLs saved to 'processed_urls.json'.")
    except Exception as e:
        logging.error(f"Error saving processed URLs: {e}")

async def send_completion_email():
    try:
        # Function to send an email notification once the task is complete
        sender_email = "your_email@example.com"
        receiver_email = "receiver_email@example.com"
        subject = "Task Completion Notification"
        body = "The script has completed all the assignments successfully."

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, "your_password")
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            logging.info("Completion email sent successfully.")
    except Exception as e:
        logging.error(f"Error while sending completion email: {e}")

