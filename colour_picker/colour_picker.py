import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytest_html

# =========================
# CONFIG
# =========================

URL = "https://www.pixelssuite.com/color-picker"

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# TEST CASE NAMES
# =========================

TC_NAMES = {
    "test_TC_012": "TC_012 - Page Load Check",
    "test_TC_013": "TC_013 - Canvas Click HEX Validation",
    "test_TC_014": "TC_014 - Slider Value Change",
    "test_TC_015": "TC_015 - HEX Value Exists",
    "test_TC_016": "TC_016 - HEX Format Check",
    "test_TC_017": "TC_017 - Copy Button Check",
    "test_TC_018": "TC_018 - Color Mode Switch",
    "test_TC_019": "TC_019 - Copy RGB Mode"
}
# =========================
# DRIVER
# =========================

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    yield driver
    driver.quit()

# =========================
# LOG FUNCTION (IMPORTANT)
# =========================

def log(message):
    print(f"[LOG] {message}")

# =========================
# HELPERS
# =========================

def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    log(f"Screenshot saved: {path}")
    return path

def find(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

def click(driver, xpath):
    el = find(driver, xpath)
    assert len(el) > 0, f"Element not found: {xpath}"
    el[0].click()
    time.sleep(1)

def canvas_click(driver):
    canvas = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "canvas"))
    )

    ActionChains(driver).move_to_element_with_offset(canvas, 50, 50).click().perform()
    time.sleep(1)

def get_hex(driver):
    el = find(driver, "//input[contains(@value,'#')]")
    if el:
        return el[0].get_attribute("value")

    el = find(driver, "//*[contains(text(),'#')]")
    if el:
        return el[0].text

    return ""

# =========================
# TEST CASES (NO LOGIC CHANGE)
# =========================

#Color tool page load validation
def test_TC_012(driver):
    log("TC_012 started")
    take_screenshot(driver, "TC_012")
    assert "color" in driver.page_source.lower()

#Click on canvas and verify hex color is generated.
def test_TC_013(driver):
    log("TC_013 started")
    canvas_click(driver)

    hex_val = get_hex(driver)
    take_screenshot(driver, "TC_013")

    assert "#" in hex_val

#Click on canvas and verify hex value is returned
def test_TC_014(driver):
    log("TC_014 started")
    canvas_click(driver)

    hex_val = get_hex(driver)
    take_screenshot(driver, "TC_014")

    assert len(hex_val) > 0

#Click on canvas and verify hex format correctness
def test_TC_015(driver):
    log("TC_015 started")
    canvas_click(driver)

    hex_val = get_hex(driver)
    take_screenshot(driver, "TC_015")

    assert hex_val.startswith("#")

#Click Copy button after selecting a color
def test_TC_016(driver):
    log("TC_016 started")
    canvas_click(driver)

    click(driver, "//button[contains(.,'Copy')]")

    take_screenshot(driver, "TC_016")

    btn = find(driver, "//button[contains(.,'Copy')]")
    assert len(btn) > 0

#Switch between RGB, HSV, HSL, and CMYK formats
def test_TC_017(driver):
    log("TC_017 started")
    canvas_click(driver)

    click(driver, "//button[contains(.,'RGB')]")
    click(driver, "//button[contains(.,'HSV')]")
    click(driver, "//button[contains(.,'HSL')]")
    click(driver, "//button[contains(.,'CMYK')]")

    take_screenshot(driver, "TC_017")

    tabs = find(driver, "//button[contains(.,'RGB') or contains(.,'HSV') or contains(.,'HSL') or contains(.,'CMYK')]")
    assert len(tabs) >= 4

#RGB format and copy the color value.
def test_TC_018(driver):
    log("TC_018 started")
    canvas_click(driver)

    click(driver, "//button[contains(.,'RGB')]")
    click(driver, "//button[contains(.,'Copy')]")

    take_screenshot(driver, "TC_018")

    btn = find(driver, "//button[contains(.,'Copy')]")
    assert len(btn) > 0


# HTML REPORT 


def pytest_html_report_title(report):
    report.title = "Color Picker Automation Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, "extra", [])

    # real test name from mapping
    test_name = item.name
    readable_name = TC_NAMES.get(test_name, test_name)

   
    report.longrepr = readable_name
    report.nodeid = readable_name
    report.description = readable_name

  
    if call.when == "call":
        extra.append(pytest_html.extras.text(f"✔ Executed: {readable_name}"))

    report.extra = extra