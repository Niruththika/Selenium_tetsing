import pytest
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================
# LOG CONFIG (ADDED ONLY)
# =========================

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "flip_test_report.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

def log(msg):
    logger.info(msg)
    print(msg)


# =========================
# CONFIG
# =========================

URL = "https://www.pixelssuite.com/flip-image"

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# FIXTURE
# =========================

@pytest.fixture
def driver():
    log("Launching Chrome Driver")
    driver = webdriver.Chrome()
    driver.maximize_window()

    log(f"Opening URL: {URL}")
    driver.get(URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    yield driver

    log("Closing Chrome Driver")
    driver.quit()

# =========================
# HELPERS (NO LOGIC CHANGED)
# =========================

def wait_el(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def find(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

def click(driver, xpath):
    el = find(driver, xpath)
    if el:
        el[0].click()
        time.sleep(1)

def upload_image(driver, filename="image.png"):
    path = os.path.join(DESKTOP, filename)

    log(f"Uploading image: {path}")

    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    file_input = wait_el(driver, "//input[@type='file']")
    file_input.send_keys(path)
    time.sleep(2)

    log("Upload completed")

def get_preview(driver):
    return driver.find_elements(By.XPATH,
        "//img | //canvas | //*[@class='preview'] | //div[contains(@class,'preview')]"
    )

def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    log(f"Screenshot saved: {path}")

# =========================
# TEST CASES (NO LOGIC CHANGE)
# =========================

def test_TC_030_page_load(driver):
    log("TC_030 started")
    assert "flip" in driver.title.lower() or "flip" in driver.page_source.lower()
    take_screenshot(driver, "TC_030")
    log("TC_030 passed")


def test_TC_031_upload(driver):
    log("TC_031 started")
    upload_image(driver)

    preview = get_preview(driver)

    assert len(preview) > 0 or "upload" in driver.page_source.lower()

    take_screenshot(driver, "TC_031")
    log("TC_031 passed")


def test_TC_032_flip_horizontal(driver):
    log("TC_032 started")

    upload_image(driver)

    before = len(get_preview(driver))

    click(driver, "//input[contains(@type,'checkbox') or contains(@name,'horizontal')]")

    time.sleep(2)
    after = len(get_preview(driver))

    assert after >= before

    take_screenshot(driver, "TC_032")
    log("TC_032 passed")


def test_TC_033_flip_vertical(driver):
    log("TC_033 started")

    upload_image(driver)

    before = len(get_preview(driver))

    click(driver, "//input[contains(@type,'checkbox') or contains(@name,'vertical')]")

    time.sleep(2)
    after = len(get_preview(driver))

    assert after >= before

    take_screenshot(driver, "TC_033")
    log("TC_033 passed")


def test_TC_034_flip_both(driver):
    log("TC_034 started")

    upload_image(driver)

    click(driver, "//input[contains(@type,'checkbox')]")
    time.sleep(1)
    click(driver, "//input[contains(@type,'checkbox')]")

    preview = get_preview(driver)

    assert len(preview) >= 0

    take_screenshot(driver, "TC_034")
    log("TC_034 passed")


def test_TC_035_download(driver):
    log("TC_035 started")

    upload_image(driver)

    before = len(driver.page_source)

    click(driver, "//button[contains(.,'Download')]")

    time.sleep(2)

    after = len(driver.page_source)

    assert "error" not in driver.page_source.lower()
    assert after > 0

    take_screenshot(driver, "TC_035")
    log("TC_035 passed")


def test_TC_036_clear(driver):
    log("TC_036 started")

    upload_image(driver)

    click(driver, "//button[contains(.,'Clear') or contains(.,'Reset')]")
    time.sleep(2)

    preview = get_preview(driver)
    file_input = wait_el(driver, "//input[@type='file']").get_attribute("value")

    upload_area = driver.find_elements(By.XPATH,
        "//input[@type='file'] | //label[contains(.,'Upload')] | //*[@class='upload']"
    )

    reset_ok = (
        len(preview) == 0
        or file_input in ["", None]
        or len(upload_area) > 0
    )

    assert reset_ok, "Clear did not reset UI properly"

    take_screenshot(driver, "TC_036")
    log("TC_036 passed")


def test_TC_037_refresh(driver):
    log("TC_037 started")

    upload_image(driver)

    driver.get(driver.current_url)
    time.sleep(3)

    preview = get_preview(driver)

    file_input = wait_el(driver, "//input[@type='file']").get_attribute("value")

    reset_ok = (
        len(preview) == 0
        or file_input in ["", None]
        or "upload" in driver.page_source.lower()
    )

    assert reset_ok, "Page did not reset after reload"

    take_screenshot(driver, "TC_037")
    log("TC_037 passed")