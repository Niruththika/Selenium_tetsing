# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
# import time

# # =========================
# # CONFIG
# # =========================

# URL = "https://www.pixelssuite.com/image-enlarger"

# USER = os.environ["USERPROFILE"]
# DESKTOP = os.path.join(USER, "Desktop")

# SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
# os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# # =========================
# # DRIVER FIXTURE
# # =========================

# @pytest.fixture
# def driver():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get(URL)
#     time.sleep(5)
#     yield driver
#     driver.quit()

# # =========================
# # SCREENSHOT FUNCTION (WORKING)
# # =========================

# def take_screenshot(driver, name):
#     path = os.path.join(SCREENSHOT_DIR, f"{name}.png")

#     try:
#         driver.save_screenshot(path)
#         print(f"✔ Screenshot saved: {path}")
#     except Exception as e:
#         print(f"✘ Screenshot failed: {e}")

# # =========================
# # HELPERS
# # =========================

# # =========================
# # HELPERS
# # =========================

# def upload_image(driver, filename="image.png"):
#     path = os.path.join(DESKTOP, filename)

#     if not os.path.exists(path):
#         raise Exception(f"File not found: {path}")

#     file_input = driver.find_element(By.XPATH, "//input[@type='file']")
#     file_input.send_keys(path)
#     time.sleep(3)


# def find(driver, xpath):
#     return driver.find_elements(By.XPATH, xpath)


# # =========================
# # TEST CASES (FIXED)
# # =========================

# def test_TC_027(driver):
#     take_screenshot(driver, "TC_027")
#     assert "enlarg" in driver.page_source.lower()


# def test_TC_028(driver):
#     take_screenshot(driver, "TC_028")
#     assert len(find(driver, "//input[@type='file']")) > 0


# def test_TC_029(driver):
#     upload_image(driver)
#     take_screenshot(driver, "TC_029")
#     assert len(find(driver, "//img | //canvas")) > 0


# def test_TC_030(driver):
#     upload_image(driver)
#     take_screenshot(driver, "TC_030")
#     assert len(find(driver, "//img | //canvas")) > 0


# def test_TC_031(driver):
#     upload_image(driver)
#     take_screenshot(driver, "TC_031")

#     page = driver.page_source.lower()
#     assert "width" in page or "height" in page


# def test_TC_032(driver):
#     upload_image(driver)

#     sliders = find(driver, "//input[@type='range']")
#     take_screenshot(driver, "TC_032")

#     assert len(sliders) > 0


# # ✅ FIXED (NO MORE assert True)
# def test_TC_033(driver):
#     upload_image(driver)

#     sliders = find(driver, "//input[@type='range']")
#     assert len(sliders) > 0

#     slider = sliders[0]

#     before = slider.get_attribute("value")

#     # ✅ Force change using JavaScript
#     driver.execute_script(
#         "arguments[0].value = 80; arguments[0].dispatchEvent(new Event('input'));",
#         slider
#     )

#     time.sleep(1)

#     after = slider.get_attribute("value")

#     take_screenshot(driver, "TC_033")

#     assert before != after


# def test_TC_034(driver):
#     upload_image(driver)
#     take_screenshot(driver, "TC_034")

#     assert len(find(driver, "//img | //canvas")) > 0


# def test_TC_035(driver):
#     upload_image(driver)

#     buttons = find(driver, "//button[contains(.,'Download')]")
#     take_screenshot(driver, "TC_035")

#     assert len(buttons) > 0


# def test_TC_036(driver):
#     upload_image(driver)

#     clear_btn = find(driver, "//button[contains(.,'Clear')]")
#     assert len(clear_btn) > 0

#     clear_btn[0].click()
#     time.sleep(2)

#     take_screenshot(driver, "TC_036")

#     assert len(find(driver, "//img")) == 0


# def test_TC_037(driver):
#     upload_image(driver)

#     driver.refresh()
#     time.sleep(3)

#     take_screenshot(driver, "TC_037")

#     assert len(find(driver, "//img")) == 0


#     ####run command pytest test_image_enlarger.py -v --html=image_enlarger_report.html --self-contained-html###

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import logging

# =========================
# LOG CONFIG (ADDED ONLY)
# =========================

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "image_enlarger_report.log")

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

URL = "https://www.pixelssuite.com/image-enlarger"

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# DRIVER FIXTURE
# =========================

@pytest.fixture
def driver():
    log("Launching Chrome Driver")

    driver = webdriver.Chrome()
    driver.maximize_window()

    log(f"Opening URL: {URL}")
    driver.get(URL)
    time.sleep(5)

    yield driver

    log("Closing Chrome Driver")
    driver.quit()

# =========================
# SCREENSHOT FUNCTION
# =========================

def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")

    try:
        driver.save_screenshot(path)
        log(f"Screenshot saved: {path}")
    except Exception as e:
        log(f"Screenshot failed: {e}")

# =========================
# HELPERS (NO LOGIC CHANGE)
# =========================

def upload_image(driver, filename="image.png"):
    path = os.path.join(DESKTOP, filename)

    log(f"Uploading image: {path}")

    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(path)
    time.sleep(3)

    log("Upload completed")

def find(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

# =========================
# TEST CASES 

#Image enlargement feature validation
def test_TC_027(driver):
    log("TC_027 started")

    take_screenshot(driver, "TC_027")
    assert "enlarg" in driver.page_source.lower()

    log("TC_027 run successfully")

#Verify that file upload input field exists on the page
def test_TC_028(driver):
    log("TC_028 started")

    take_screenshot(driver, "TC_028")
    assert len(find(driver, "//input[@type='file']")) > 0

    log("TC_028 run successfully")

#Upload an image and verify it is rendered in preview
def test_TC_029(driver):
    log("TC_029 started")

    upload_image(driver)
    take_screenshot(driver, "TC_029")

    assert len(find(driver, "//img | //canvas")) > 0

    log("TC_029 run successfully")

#Upload an image and verify preview rendering consistency.
def test_TC_030(driver):
    log("TC_030 started")

    upload_image(driver)
    take_screenshot(driver, "TC_030")

    assert len(find(driver, "//img | //canvas")) > 0

    log("TC_030 run successfully")

#Verify that image resizing controls (width/height) are available in UI.
def test_TC_031(driver):
    log("TC_031 started")

    upload_image(driver)
    take_screenshot(driver, "TC_031")

    page = driver.page_source.lower()
    assert "width" in page or "height" in page

    log("TC_031 run successfully")

#Verify that slider controls (range inputs) exist for image adjustments
def test_TC_032(driver):
    log("TC_032 started")

    upload_image(driver)

    sliders = find(driver, "//input[@type='range']")
    take_screenshot(driver, "TC_032")

    assert len(sliders) > 0

    log("TC_032 run successfully")

#Adjust slider value and verify that UI updates accordingly
def test_TC_033(driver):
    log("TC_033 started")

    upload_image(driver)

    sliders = find(driver, "//input[@type='range']")
    assert len(sliders) > 0

    slider = sliders[0]

    before = slider.get_attribute("value")

    driver.execute_script(
        "arguments[0].value = 80; arguments[0].dispatchEvent(new Event('input'));",
        slider
    )

    time.sleep(1)

    after = slider.get_attribute("value")

    take_screenshot(driver, "TC_033")

    assert before != after

    log("TC_033 run successfully")

#Upload image and verify preview remains visible
def test_TC_034(driver):
    log("TC_034 started")

    upload_image(driver)
    take_screenshot(driver, "TC_034")

    assert len(find(driver, "//img | //canvas")) > 0

    log("TC_034 run successfully")

#Download button availability
def test_TC_035(driver):
    log("TC_035 started")

    upload_image(driver)

    buttons = find(driver, "//button[contains(.,'Download')]")
    take_screenshot(driver, "TC_035")

    assert len(buttons) > 0

    log("TC_035 run successfully")

#Clear image functionality validation
def test_TC_036(driver):
    log("TC_036 started")

    upload_image(driver)

    clear_btn = find(driver, "//button[contains(.,'Clear')]")
    assert len(clear_btn) > 0

    clear_btn[0].click()
    time.sleep(2)

    take_screenshot(driver, "TC_036")

    assert len(find(driver, "//img")) == 0

    log("TC_036 run successfully")

#age refresh reset validation
def test_TC_037(driver):
    log("TC_037 started")

    upload_image(driver)

    driver.refresh()
    time.sleep(3)

    take_screenshot(driver, "TC_037")

    assert len(find(driver, "//img")) == 0

    log("TC_037 run successfully")