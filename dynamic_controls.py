import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Настройка пути к логам
log_directory = r"C:\ProgramData\Jenkins\.jenkins\workspace\SEQA"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Настройка логирования
logging.basicConfig(
    filename=os.path.join(log_directory, 'test_results.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

chrome_driver_path = r"C:\chromedriver\chromedriver.exe"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://the-internet.herokuapp.com/dynamic_controls")

    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#checkbox"))
    )

    remove_button = driver.find_element(By.CSS_SELECTOR, "#checkbox-example button")
    remove_button.click()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element(checkbox)
    )
    logging.info("Checkbox successfully removed")

    add_button = driver.find_element(By.CSS_SELECTOR, "#checkbox-example button")
    add_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#checkbox"))
    )
    logging.info("Checkbox successfully added")

except TimeoutException:
    logging.error("An error occurred: element was not found or did not load in time")

finally:
    driver.quit()
    logging.info("Browser closed")
