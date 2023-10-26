import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
import logging
import os.path
import requests

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--enable-javascript")

logfile_path = ".\\features\\Test Results\\"
if not os.path.exists(logfile_path):
    os.makedirs(logfile_path)

logfile = os.path.join(logfile_path + "log.txt")
fh1 = logging.FileHandler(filename=logfile, mode='w')
logging.getLogger().addHandler(fh1)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s: %(funcName)s() %(lineno)d - %(message)s')
fh1.setFormatter(formatter)
logging.info(f'Logfile path: {logfile}')


def launch_web_browser(context, browser_type='chrome'):
    try:
        if browser_type.lower() == 'chrome':
            service = Service()
            driver = webdriver.Chrome(service=service, options=options)
        # Can add a elif for 'Firefox' browser
        else:
            assert False, f"Invalid browser type"
        context.driver = driver
        return driver
    except Exception as err:
        assert False, f'{err}'


def open_url_and_verify_xpath_present(context, url, xpath, timeout=10):
    try:
        logging.info(f'Navigating to URL: {url}')
        context.driver.get(url)
        WebDriverWait(context.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return True
    except NoSuchElementException:
        logging.error(f'Element not found with {xpath}')
        return False
    except TimeoutException:
        logging.error(f'TIMEOUT: Unable to locate {xpath}')
        return False
    except Exception as err:
        assert False, f'{err}'


def wait_for_xpath(context, xpath, timeout=10):
    try:
        time.sleep(2)
        WebDriverWait(context.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        logging.info(f'Xpath {xpath} exists')
        return True
    except NoSuchElementException:
        logging.error(f'Element not found with {xpath}')
        return False
    except TimeoutException:
        logging.error(f'TIMEOUT: Unable to locate {xpath}')
        return False
    except Exception as err:
        assert False, f'{err}'


def refresh_page_and_wait_for_xpath(context, xpath):
    try:
        context.driver.refresh()
        wait_for_xpath(context, xpath)
    except Exception as err:
        assert False, f'{err}'


def click_on_element_by_xpath(context, xpath, timeout=10):
    try:
        wait_for_xpath(context, xpath, timeout)
        logging.info(f'Found XPath - {xpath}')
        element = context.driver.find_element(By.XPATH, value=xpath)
        element.click()
        logging.info(f'Clicked on Xpath - {xpath}')
        return True
    except TimeoutException:
        logging.error(f'TIMEOUT: Unable to locate {xpath}')
        return False
    except ElementNotVisibleException:
        logging.error(f'Element to be clicked is not visible with xpath {xpath}')
        return False
    except Exception as err:
        assert False, f'{err}'


def get_products_list_over_api(url='https://react-shopping-cart-67954.firebaseio.com/products.json', retry=3):
    try:
        flag = True
        logging.info("Retrieving product list using API")
        for i in range(retry):
            header = {'Accept': 'application/json, text/plain, */*'}
            time.sleep(2)
            response = requests.get(url, headers=header)
            if '200' in str(response.status_code):
                logging.info(f'Success return code: {response.status_code}')
                return response.json()
            else:
                flag = False

        if not flag:
            logging.error(f"Count not connect to {url}")

    except Exception as err:
        assert False, f'{err}'


def get_multiple_elements_text_by_xpath(context, xpath):
    try:
        wait_for_xpath(context, xpath)
        elements = context.driver.find_elements(By.XPATH, value=xpath)
        output_list = []
        for element in elements:
            output_list.append(element.text)
        logging.info(f'Found following list of values {output_list} from {xpath}')
        return output_list
    except Exception as err:
        assert False, f'{err}'

