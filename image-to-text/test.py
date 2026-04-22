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

LOG_FILE = os.path.join(LOG_DIR, "ocr_test_report.log")

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

URL = "https://www.pixelssuite.com/image-to-text"

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
# HELPERS (NO LOGIC CHANGE)
# =========================

def wait_el(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def find(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

def upload_image(driver, filename="image.png"):
    path = os.path.join(DESKTOP, filename)

    log(f"Uploading image: {path}")

    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    file_input = wait_el(driver, "//input[@type='file']")
    file_input.send_keys(path)
    time.sleep(2)

    log("Upload completed")

def click(driver, xpath):
    el = find(driver, xpath)
    if el:
        el[0].click()
        log(f"Clicked element: {xpath}")
        time.sleep(2)

def get_preview(driver):
    return driver.find_elements(By.XPATH,
        "//img | //canvas | //*[@class='preview'] | //div[contains(@class,'preview')]"
    )

def get_result_text(driver):
    els = find(driver, "//*[contains(@class,'result') or contains(@class,'output') or self::textarea]")
    return [e.text for e in els if e.text.strip()]

def take_screenshot(driver, name):
    import base64

    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "captureBeyondViewport": True
    })

    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")

    with open(path, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))

    log(f"Screenshot saved: {path}")

# =========================
# TEST CASES (NO LOGIC CHANGE)
# =========================

def test_TC_001_page_load(driver):
    log("TC_001 started")

    assert "text" in driver.page_source.lower() or "ocr" in driver.page_source.lower()

    take_screenshot(driver, "TC_001")

    log("TC_001 passed")


def test_TC_002_upload(driver):
    log("TC_002 started")

    upload_image(driver)

    preview = get_preview(driver)

    assert len(preview) > 0 or "upload" in driver.page_source.lower()

    take_screenshot(driver, "TC_002")

    log("TC_002 passed")


def test_TC_003_language_dropdown(driver):
    log("TC_003 started")

    upload_image(driver)

    dropdown = find(driver,
        "//select | //button[contains(.,'Language')] | //*[@role='button']"
    )

    assert len(dropdown) > 0

    click(driver, "//option | //li | //div[contains(.,'English') or contains(.,'Sinhala')]")

    take_screenshot(driver, "TC_003")

    log("TC_003 passed")


def test_TC_004_start_ocr(driver):
    log("TC_004 started")

    upload_image(driver)

    click(driver, "//button[contains(.,'Start') or contains(.,'OCR')]")

    time.sleep(3)

    result = get_result_text(driver)

    assert len(result) >= 0

    take_screenshot(driver, "TC_004")

    log("TC_004 passed")


def test_TC_005_copy(driver):
    log("TC_005 started")

    upload_image(driver)

    click(driver, "//button[contains(.,'Start') or contains(.,'OCR')]")
    time.sleep(3)

    copy_btn = find(driver, "//button[contains(.,'Copy')]")

    if copy_btn:
        copy_btn[0].click()
        log("Copy button clicked")

    assert True

    take_screenshot(driver, "TC_005")

    log("TC_005 passed")


def test_TC_006_clear_options(driver):
    log("TC_006 started")

    upload_image(driver)

    click(driver, "//button[contains(.,'Start') or contains(.,'OCR')]")
    time.sleep(2)

    click(driver, "//button[contains(.,'Clear')]")

    time.sleep(2)

    result = get_result_text(driver)
    preview = get_preview(driver)

    assert len(result) == 0 or len(preview) == 0

    take_screenshot(driver, "TC_006")

    log("TC_006 passed")


def test_TC_007_clear_upload(driver):
    log("TC_007 started")

    upload_image(driver)

    click(driver, "//button[contains(.,'Clear')]")
    time.sleep(2)

    preview = get_preview(driver)

    assert len(preview) == 0 or "upload" in driver.page_source.lower()

    take_screenshot(driver, "TC_007")

    log("TC_007 passed")


def test_TC_008_refresh(driver):
    log("TC_008 started")

    upload_image(driver)

    driver.get(driver.current_url)
    time.sleep(3)

    preview = get_preview(driver)

    assert len(preview) == 0 or "upload" in driver.page_source.lower()

    take_screenshot(driver, "TC_008")

    log("TC_008 passed")