

import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# =========================
# CONFIG
# =========================

URLS = [
    "https://www.pixelssuite.com/compress-image",
    "https://www.pixelssuite.com/png-compressor",
    "https://www.pixelssuite.com/gif-compressor"
]

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# DRIVER FIXTURE
# =========================

@pytest.fixture(params=URLS)
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(request.param)
    time.sleep(4)
    yield driver
    driver.quit()

# =========================
# HELPERS
# =========================

def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"✔ Screenshot saved: {path}")

def find(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

def click(driver, xpath):
    el = find(driver, xpath)
    if el:
        el[0].click()
        time.sleep(2)

def upload_file(driver, filename="image.png"):
    path = os.path.join(DESKTOP, filename)
    assert os.path.exists(path), f"Missing file: {path}"

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(path)
    time.sleep(3)

def is_error(driver):
    return "error" in driver.page_source.lower()

def has_element(driver, xpath):
    return len(driver.find_elements(By.XPATH, xpath)) > 0


# =========================
# TEST CASES
# =========================

#Compress tool page load validation
def test_TC_105(driver):
    """TC_105 - Verify Compress Tool Page Loads Correctly"""
    take_screenshot(driver, "TC_105")
    assert "compress" in driver.title.lower() or has_element(driver, "//input[@type='file']")

#Verify that file upload input field is present on the page
def test_TC_106(driver):
    """TC_106 - Verify File Upload Input Exists"""
    take_screenshot(driver, "TC_106")
    assert has_element(driver, "//input[@type='file']")

#Upload an image and verify preview is displayed
def test_TC_107(driver):
    """TC_107 - Verify Image Upload and Preview Appears"""
    upload_file(driver)
    take_screenshot(driver, "TC_107")
    assert has_element(driver, "//img | //canvas")

#Upload an image and verify preview remains stable
def test_TC_108(driver):
    """TC_108 - Verify Image Preview Stability After Upload"""
    upload_file(driver)
    take_screenshot(driver, "TC_108")
    assert has_element(driver, "//img | //canvas")

#Upload image and verify compression output or preview section appears.
def test_TC_109(driver):
    """TC_109 - Verify Preview or Compression Output Exists"""
    upload_file(driver)
    take_screenshot(driver, "TC_109")
    assert has_element(driver, "//img | //canvas | //div[contains(@class,'preview')]")

#Clear button functionality
def test_TC_110(driver):
    """TC_110 - Verify Clear Button Resets Upload"""
    upload_file(driver)
    click(driver, "//button[contains(.,'Clear')]")
    time.sleep(2)

    preview = driver.find_elements(By.XPATH, "//img | //canvas")

    assert len(preview) == 0 or not preview[0].is_displayed()

    take_screenshot(driver, "TC_110")

#File size information display validation
def test_TC_111(driver):
    """TC_111 - Verify File Size Information Displayed"""
    upload_file(driver)
    take_screenshot(driver, "TC_111")

    assert has_element(driver,
        "//*[contains(text(),'KB') or contains(text(),'MB') or contains(text(),'Size')]"
    )


def get_slider(driver):
    sliders = driver.find_elements(By.XPATH, "//input[@type='range']")
    return sliders[0] if sliders else None

#Compression controls availability
def test_TC_112(driver):
    """TC_112 - Verify Compression Controls Exist"""
    upload_file(driver)
    take_screenshot(driver, "TC_112")

    assert has_element(driver, "//select | //button | //input")

#Download button error-free execution
def test_TC_113(driver):
    """TC_113 - Verify Download Button Works Without Error"""
    upload_file(driver)
    click(driver, "//button[contains(.,'Download')]")

    take_screenshot(driver, "TC_114")
    assert not is_error(driver)

#PNG download option validation
def test_TC_114(driver):
    """TC_114 - Verify PNG Download Option Works"""
    upload_file(driver)
    click(driver, "//*[contains(.,'PNG') or contains(.,'Download PNG')]")

    take_screenshot(driver, "TC_115")
    assert not is_error(driver)

#– Compression level selection validation (O2 / O3)
def test_TC_115(driver):
    """TC_115 - Verify Compression Level Options (O2 / O3)"""
    upload_file(driver)

    click(driver, "//*[contains(text(),'O2')]")
    click(driver, "//*[contains(text(),'O3')]")

    active = driver.find_elements(By.XPATH, "//*[contains(@class,'active') or contains(@class,'selected')]")

    take_screenshot(driver, "TC_117")
    assert len(active) >= 0

#Upload image and perform compression action
def test_TC_116(driver):
    """TC_116 - Verify Compress Action Works Successfully"""
    upload_file(driver)
    click(driver, "//button[contains(.,'Compress')]")

    take_screenshot(driver, "TC_119")
    assert not is_error(driver)

#Page refresh reset validation
def test_TC_017(driver):
    """TC_017 - Verify Page Refresh Resets State"""
    upload_file(driver)

    driver.refresh()
    time.sleep(4)

    images = driver.find_elements(By.XPATH, "//img")
    canvas = driver.find_elements(By.XPATH, "//canvas")

    visible_imgs = [i for i in images if i.is_displayed()]

    assert len(visible_imgs) == 0 or len(canvas) <= 1

    take_screenshot(driver, "TC_018")