"""
===========================================
RESIZE IMAGE AUTOMATION FRAMEWORK (PyTest)
===========================================
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================
# LOG CONFIG (ADDED ONLY)
# =========================

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "resize_test_report.log")

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

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")
URL = "https://www.pixelssuite.com/resize-image"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# =========================
# FIXTURE
# =========================

@pytest.fixture
def driver():
    log("Launching Chrome Driver")
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    log("Closing Chrome Driver")
    driver.quit()


# =========================
# HELPERS (NO LOGIC CHANGE)
# =========================

def open_page(driver):
    log(f"Opening URL: {URL}")
    driver.get(URL)
    time.sleep(3)

def wait(driver, xpath, t=10):
    return WebDriverWait(driver, t).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def upload(driver, filename):
    path = os.path.join(DESKTOP, filename)

    log(f"Uploading file: {path}")

    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(path)
    time.sleep(3)

    log("Upload completed")

def get_inputs(driver):
    return driver.find_elements(By.XPATH, "//input[@type='number']")

def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")

    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    time.sleep(1)

    driver.save_screenshot(path)
    driver.maximize_window()

    log(f"Screenshot saved: {path}")
    return path


# =========================
# HOOK (Screenshot on Failure)
# =========================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs["driver"]
        take_screenshot(driver, item.name)
        log(f"Test FAILED: {item.name}")


# =========================
# TEST CASES (NO LOGIC CHANGE)
# =========================

def test_TC_001_page_load(driver):
    log("TC_001 started")

    open_page(driver)

    body = driver.find_elements(By.TAG_NAME, "body")
    assert len(body) > 0

    log("TC_001 passed")


def test_TC_002_upload_area(driver):
    log("TC_002 started")

    open_page(driver)

    upload_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
    assert len(upload_inputs) > 0

    log("TC_002 passed")


def test_TC_003_resize_section(driver):
    log("TC_003 started")

    open_page(driver)
    upload(driver, "image.png")

    inputs = get_inputs(driver)
    assert len(inputs) >= 2

    log("TC_003 passed")


def test_TC_004_preview_section(driver):
    log("TC_004 started")

    open_page(driver)
    upload(driver, "image.png")

    preview = driver.find_elements(
        By.XPATH, "//canvas | //img | //div[contains(@class,'preview')]"
    )

    assert len(preview) > 0

    log("TC_004 passed")


def test_TC_005_upload_image(driver):
    log("TC_005 started")

    open_page(driver)
    upload(driver, "image.png")

    before = len(get_inputs(driver))
    assert before >= 2

    log("TC_005 passed")


def test_TC_006_dimension_change(driver):
    log("TC_006 started")

    open_page(driver)
    upload(driver, "image.png")

    inputs = get_inputs(driver)
    assert len(inputs) >= 2

    before = inputs[0].get_attribute("value")

    inputs[0].clear()
    inputs[0].send_keys("350")

    time.sleep(2)

    after = inputs[0].get_attribute("value")

    assert before != after

    log("TC_006 passed")


def test_TC_007_keep_aspect_enabled(driver):
    log("TC_007 started")

    open_page(driver)
    upload(driver, "image.png")

    checkbox = wait(driver, "//input[@type='checkbox']")

    before = checkbox.is_selected()
    checkbox.click()
    after = checkbox.is_selected()

    assert before != after

    log("TC_007 passed")


def test_TC_008_keep_aspect_disabled(driver):
    log("TC_008 started")

    open_page(driver)
    upload(driver, "image.png")

    checkbox = wait(driver, "//input[@type='checkbox']")

    if checkbox.is_selected():
        checkbox.click()
        time.sleep(1)

    assert checkbox.is_selected() is False

    log("TC_008 passed")


def test_TC_009_download_button(driver):
    log("TC_009 started")

    open_page(driver)
    upload(driver, "image.png")

    buttons = driver.find_elements(By.XPATH, "//button[contains(.,'Download')]")

    assert len(buttons) > 0

    log("TC_009 passed")


def test_TC_011_refresh(driver):
    log("TC_011 started")

    open_page(driver)
    upload(driver, "image.png")

    driver.refresh()
    time.sleep(3)

    file_input = driver.find_elements(By.XPATH, "//input[@type='file']")
    preview = driver.find_elements(By.XPATH, "//img | //canvas")

    assert len(file_input) > 0
    assert len(preview) <= 1

    log("TC_011 passed")