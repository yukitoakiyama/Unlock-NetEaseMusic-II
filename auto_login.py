# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005C2742678FAB928D49A483B29E90039011036BADB076BCFDCE3A67D386BFD59CBB66FCF8DC353D5431ED4384CD6893789399B8A5F8E49F11A1257B8EF83276A3A9ADC78A230F8728EDE7A45CAC768C724D6B18A65D5393EDE33C4C4B57B14781E153172B95A8B6EEABD392BBAAC9083A4091CC2635CC98C77F97455A4015BCFECBB7399FDD2850410F2835E3FDFE2AC79CFAF4B142807C37CA3232DB870EE80A7182539C720976F19B013B1908B73CA5A2AD9D8D2A96231FCAB2D2D93F78A3C0FD5602B7F5C9D3DD5F5FEB8A44D44F83CC7C031FD3882466E3056739BF1396AD540E63B3F8C1B0F25A514510B678A3B5A3BC52DF3E250B84038FF53BA524DB03563CA49C8988798FE12A22278B2065D30AA47128DA478CD853B706B0C7FCA242DE177C14A9A2D44BFE809F48ECC2C5D10593B6DEFAF2B39D55618613464DDA4F6780292E3B845FFFF64DC79AAA5491EEB56AAA0A62BA56AAD442556418BEB27B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
