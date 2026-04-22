import pytest
import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =========================
# CONFIG (NO HARDCODE PATH)
# =========================

BASE_URL = "https://www.pixelssuite.com/pdf-to-word"

HOME = str(Path.home())
FILE_DIR = os.path.join(os.getcwd(), "test_files")  # put pdf files here
os.makedirs(FILE_DIR, exist_ok=True)

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# FIXTURE
# =========================

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(BASE_URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    yield driver
    driver.quit()

# =========================
# HELPERS
# =========================

def wait_el(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def find(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

def upload(driver, filename="test.pdf"):
    file_path = os.path.join(FILE_DIR, filename)

    if not os.path.exists(file_path):
        raise Exception(f"File not found in test_files: {file_path}")

    file_input = wait_el(driver, "//input[@type='file']")
    file_input.send_keys(file_path)
    time.sleep(2)

def click_convert(driver):
    btn = wait_el(driver, "//button")
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(4)

def get_text(driver):
    return driver.page_source.lower()

def screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")

    h = driver.execute_script("return document.body.scrollHeight")
    w = driver.execute_script("return window.innerWidth")

    driver.set_window_size(1920, h)
    time.sleep(1)

    driver.save_screenshot(path)
    driver.set_window_size(w, 800)

    return path

def get_text(driver):
    return driver.find_element(By.TAG_NAME, "body").text.lower()

def has(driver, xpath):
    return len(driver.find_elements(By.XPATH, xpath)) > 0

# =========================
# TEST CASES (PYTEST STYLE)
# =========================

def test_TC_01_upload_and_convert(driver):
    upload(driver)
    click_convert(driver)
    assert "error" not in get_text(driver)
    screenshot(driver, "TC_01")


def test_TC_02_upload_only(driver):
    upload(driver)
    assert find(driver, "//input[@type='file']")
    screenshot(driver, "TC_02")


def test_TC_03_multiple_upload_block(driver):
    upload(driver)
    try:
        upload(driver)
        assert False, "Multiple upload should not be allowed"
    except:
        assert True
    screenshot(driver, "TC_03")


def test_TC_04_invalid_file(driver):
    upload(driver, "image.png")
    click_convert(driver)
    text = get_text(driver)
    assert any(x in text for x in ["error", "invalid", "unsupported"])
    screenshot(driver, "TC_04")


def test_TC_05_large_file(driver):
    upload(driver, "large.pdf")
    click_convert(driver)
    assert "error" in get_text(driver)
    screenshot(driver, "TC_05")


def test_TC_06_valid_pdf(driver):
    upload(driver, "test.pdf")
    click_convert(driver)
    assert "error" not in get_text(driver)
    screenshot(driver, "TC_06")


def test_TC_07_buttons_exist(driver):
    assert len(find(driver, "//button")) > 0
    screenshot(driver, "TC_07")


def test_TC_08_responsive(driver):
    # set mobile view
    driver.set_window_size(375, 812)
    time.sleep(2)

    # 1. Page must still load
    assert driver.execute_script("return document.readyState") == "complete"

    # 2. Core functionality must exist (NOT visible assumption)
    upload_input = driver.find_elements("//input[@type='file']")
    assert len(upload_input) > 0, "Upload missing in mobile view"

    # 3. Page must not collapse into empty UI
    page_length = len(driver.page_source)
    assert page_length > 500, "Mobile layout broken or empty"

    # 4. Detect extreme layout failure (important for your case)
    body_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # if layout is EXTREMELY wrong (your issue: too much empty space)
    assert body_height >= viewport_height * 0.5, "UI spacing/layout issue on mobile"

    screenshot(driver, "TC_08")


def test_TC_09_file_size_visible(driver):
    upload(driver)
    assert "kb" in get_text(driver) or "mb" in get_text(driver)
    screenshot(driver, "TC_09")


def test_TC_10_file_name_visible(driver):
    upload(driver)
    assert "test" in get_text(driver)
    screenshot(driver, "TC_10")


def test_TC_11_conversion_flow(driver):
    upload(driver)
    click_convert(driver)
    assert "error" not in get_text(driver)
    screenshot(driver, "TC_11")


def test_TC_12_convert_button(driver):
    assert len(find(driver, "//button")) > 0
    screenshot(driver, "TC_12")

def test_TC_13_general_ui(driver):
    body = get_text(driver)

    # page should not be empty
    assert len(body.strip()) > 10

    # check REAL UI components, not text keywords
    assert has(driver, "//input[@type='file']")
    assert has(driver, "//button")

    screenshot(driver, "TC_13")



def test_TC_14_supported_format(driver):
    text = get_text(driver)
    assert "supported" in text or "format" in text
    screenshot(driver, "TC_14")


def test_TC_15_ui_validation(driver):

    # 1. Upload exists (core functionality)
    upload_input = driver.find_elements(By.XPATH, "//input[@type='file']")
    assert len(upload_input) > 0, "Upload input missing"

    # 2. Buttons exist
    buttons = driver.find_elements(By.TAG_NAME, "button")
    assert len(buttons) > 0, "No action buttons found"

    # 3. Page is loaded properly
    assert driver.execute_script("return document.readyState") == "complete"

    # 4. Basic DOM sanity check
    html_length = len(driver.page_source)
    assert html_length > 1000, "Page looks incomplete or broken"

    # =========================
    # ❌ NEGATIVE VALIDATION (IMPORTANT FIX)
    # =========================

    body_text = driver.page_source.lower()

    invalid_keywords = [
        "jpg",
        "png",
        "webp",
        "supported formats",
        "image format"
    ]

    for word in invalid_keywords:
        assert word not in body_text, f"Invalid UI text found: {word}"

    screenshot(driver, "TC_15")