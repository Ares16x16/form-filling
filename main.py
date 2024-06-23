import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

form_url = ""

# Define conditions for different sections
run_short_text_input = True
short_text_input_answer = {"test 1": "answer 1", "test 2": "answer 2"}

run_drop_down_list = True
dropdown_answer = "b"

run_radio_button_input = True
radio_button_input_answer = {"test 4": "a", "test 5": "c"}


# ===============================================================
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.delete_all_cookies()
driver.get(form_url)

time.sleep(0.1)

# Fill in the short text input fields
if run_short_text_input and short_text_input_answer:

    # Get the text fields and their names
    text_fields = driver.find_elements(
        By.XPATH, "//input[contains(@class,'whsOnd zHQkBf')]"
    )
    name_of_text_fields = []
    for texts in driver.find_elements(By.XPATH, "//span[contains(@class,'M7eMe')]"):
        name_of_text_fields.append(texts.text)

    # Truncate the list of names to match the number of text fields
    # name_of_text_fields = name_of_text_fields[: len(short_text_input_answer)]
    filtered_list = [
        name for name in name_of_text_fields if name in short_text_input_answer
    ]
    logging.info(f"Short Answer Fields: {filtered_list}")

    # Fill in the text fields with the answer
    for i, name_of_text_field in enumerate(filtered_list):
        if (
            list(short_text_input_answer.keys())[i].lower()
            in name_of_text_field.lower()
        ):
            text_fields[i].clear()
            text_fields[i].send_keys(
                short_text_input_answer[list(short_text_input_answer.keys())[i]]
            )

# Fill in the dropdown fields
if run_drop_down_list and dropdown_answer:
    dropdown = driver.find_element(
        By.XPATH, "//div[contains(@class,'MocG8c HZ3kWc mhLiyf LMgvRb KKjvXb DEh1R')]"
    )
    dropdown.click()
    time.sleep(0.15)

    for selections in driver.find_elements(
        By.XPATH, "//span[contains(@class,'vRMGwf oJeWuf')]"
    ):

        logging.info(f"Dropdown Options: {selections.text}")
        if dropdown_answer in selections.text:
            time.sleep(0.1)
            selections.click()
            break
time.sleep(0.1)

"""# Fill in the radio button inputs
if run_radio_button_input and radio_button_input_answer:
    for title, answer in radio_button_input_answer.items():
        radio_buttons = driver.find_elements(
            By.CLASS_NAME,
            "appsMaterialWizToggleRadiogroupEl",
        )
        time.sleep(0.1)
        for i, radio_button in enumerate(radio_buttons):
            logging.info(f"Radio Button Options: {radio_button[i]}")
            time.sleep(0.1)
            if radio_button[i] == answer:
                time.sleep(0.1)
                radio_button.click()
                break
time.sleep(0.1)"""
# Submit the form
try:
    submit = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span',
            )
        )
    )
    submit.click()
except Exception as e:
    print(str(e))
finally:
    # Close the web driver
    driver.quit()
