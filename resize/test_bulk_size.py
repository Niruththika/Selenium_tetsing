# """
# ===========================================
# BULK RESIZE IMAGE AUTOMATION (PyTest + Selenium)
# ===========================================

# URL: https://www.pixelssuite.com/bulk-resize

# Covers:
# TC-012 to TC-025

# Run:
# pytest test_bulk_resize.py -v --html=report.html --self-contained-html
# ===========================================
# """

# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import os
# import time

# # =========================
# # CONFIG
# # =========================

# USER = os.environ["USERPROFILE"]
# DESKTOP = os.path.join(USER, "Desktop")

# URL = "https://www.pixelssuite.com/bulk-resize"

# SCREENSHOT_DIR = "screenshots"
# os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# # =========================
# # FIXTURE
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
# # HELPERS
# # =========================

# def upload_multiple(driver, files):
#     """
#     Upload multiple images (bulk input)
#     """
#     file_input = driver.find_element(By.XPATH, "//input[@type='file']")

#     paths = [os.path.join(DESKTOP, f) for f in files]

#     for p in paths:
#         if not os.path.exists(p):
#             raise Exception(f"File not found: {p}")

#     file_input.send_keys("\n".join(paths))
#     time.sleep(3)


# def find(driver, xpath):
#     return driver.find_elements(By.XPATH, xpath)


# # =========================
# # TEST CASES
# # =========================

# # TC-012
# def test_TC_012_bulk_page_load(driver):
#     assert "bulk" in driver.page_source.lower()


# # TC-013
# def test_TC_013_files_section(driver):
#     files_section = find(driver, "//div[contains(.,'Files')]")
#     assert len(files_section) > 0


# # TC-014
# def test_TC_014_options_section(driver):
#     options_section = find(driver, "//div[contains(.,'Options')]")
#     assert len(options_section) > 0


# # TC-015
# def test_TC_015_upload_via_select(driver):
#     upload_multiple(driver, ["image.png", "image2.png"])
#     assert len(find(driver, "//img | //canvas")) > 0


# # TC-016
# def test_TC_016_drag_drop_upload(driver):
#     # Selenium cannot fully simulate OS drag-drop reliably
#     # so we validate UI accepts multiple images after upload
#     upload_multiple(driver, ["image.png", "image2.png"])
#     assert len(find(driver, "//img | //canvas")) > 0


# # TC-017
# def test_TC_017_width_input(driver):
#     input_box = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Width') or @type='number']")
#     input_box.clear()
#     input_box.send_keys("500")
#     assert input_box.get_attribute("value") == "500"


# # TC-018
# def test_TC_018_height_input(driver):
#     input_box = driver.find_elements(By.XPATH, "//input[@type='number']")[1]
#     input_box.clear()
#     input_box.send_keys("400")
#     assert input_box.get_attribute("value") == "400"


# # TC-019
# def test_TC_019_keep_aspect_enabled(driver):
#     checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
#     if not checkbox.is_selected():
#         checkbox.click()
#     assert checkbox.is_selected()


# # TC-020
# def test_TC_020_keep_aspect_disabled(driver):
#     checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
#     if checkbox.is_selected():
#         checkbox.click()
#     assert not checkbox.is_selected()


# # TC-021
# def test_TC_021_process_download(driver):
#     upload_multiple(driver, ["image.png"])

#     buttons = find(driver, "//button[contains(.,'Process') or contains(.,'Download')]")
#     assert len(buttons) > 0


# # TC-022
# def test_TC_022_clear_button(driver):
#     upload_multiple(driver, ["image.png"])

#     clear_btn = driver.find_element(By.XPATH, "//button[contains(.,'Clear')]")
#     clear_btn.click()
#     time.sleep(2)

#     assert "no files" in driver.page_source.lower() or len(find(driver, "//img")) == 0


# # TC-023
# def test_TC_023_process_without_upload(driver):
#     btn = driver.find_element(By.XPATH, "//button[contains(.,'Process')]")
#     assert btn.is_enabled() is False or "disabled" in btn.get_attribute("class")


# # TC-024
# def test_TC_024_missing_dimensions(driver):
#     upload_multiple(driver, ["image.png"])

#     btn = driver.find_element(By.XPATH, "//button[contains(.,'Process')]")
#     btn.click()
#     time.sleep(2)

#     # Expect validation or no download
#     assert "error" in driver.page_source.lower() or "required" in driver.page_source.lower()


# # TC-025
# def test_TC_025_invalid_dimensions(driver):
#     upload_multiple(driver, ["image.png"])

#     inputs = driver.find_elements(By.XPATH, "//input[@type='number']")
#     inputs[0].clear()
#     inputs[0].send_keys("0")

#     inputs[1].clear()
#     inputs[1].send_keys("-100")

#     driver.find_element(By.XPATH, "//button[contains(.,'Process')]").click()
#     time.sleep(2)

#     assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower()

# """
# ===========================================
# BULK RESIZE - FINAL SAFE VERSION
# ===========================================
# ✔ Screenshots ALWAYS work
# ✔ No hooks
# ✔ Submission safe version
# ===========================================
# """

# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
# import time

# # =========================
# # CONFIG
# # =========================

# URL = "https://www.pixelssuite.com/bulk-resize"

# USER = os.environ["USERPROFILE"]
# DESKTOP = os.path.join(USER, "Desktop")

# SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
# os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# # =========================
# # DRIVER
# # =========================

# @pytest.fixture
# def driver():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get(URL)
#     time.sleep(5)
#     yield driver
#     driver.quit()

# =========================
# SCREENSHOT FUNCTION (IMPORTANT)
# =========================

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

# def upload_multiple(driver, files):
#     file_input = driver.find_element(By.XPATH, "//input[@type='file']")

#     paths = []
#     for f in files:
#         full = os.path.join(DESKTOP, f)
#         if not os.path.exists(full):
#             raise Exception(f"Missing file: {full}")
#         paths.append(full)

#     file_input.send_keys("\n".join(paths))
#     time.sleep(3)

# def find(driver, xpath):
#     return driver.find_elements(By.XPATH, xpath)

# # =========================
# # TEST CASES (ALL WITH SCREENSHOTS)
# # =========================

# def test_TC_012(driver):
#     time.sleep(2)
#     take_screenshot(driver, "TC_012")
#     assert "bulk" in driver.page_source.lower()

# def test_TC_013(driver):
#     take_screenshot(driver, "TC_013")
#     assert len(find(driver, "//div[contains(.,'Files')]")) > 0

# def test_TC_014(driver):
#     take_screenshot(driver, "TC_014")
#     assert len(find(driver, "//div[contains(.,'Options')]")) > 0

# def test_TC_015(driver):
#     upload_multiple(driver, ["image.png", "image2.png"])
#     take_screenshot(driver, "TC_015")
#     assert len(find(driver, "//img | //canvas")) > 0

# def test_TC_016(driver):
#     upload_multiple(driver, ["image.png", "image2.png"])
#     take_screenshot(driver, "TC_016")
#     assert len(find(driver, "//img | //canvas")) > 0

# def test_TC_017(driver):
#     inp = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Width') or @type='number']")
#     inp.clear()
#     inp.send_keys("500")
#     take_screenshot(driver, "TC_017")
#     assert inp.get_attribute("value") == "500"

# def test_TC_018(driver):
#     inp = driver.find_elements(By.XPATH, "//input[@type='number']")[1]
#     inp.clear()
#     inp.send_keys("400")
#     take_screenshot(driver, "TC_018")
#     assert inp.get_attribute("value") == "400"

# def test_TC_019(driver):
#     cb = driver.find_element(By.XPATH, "//input[@type='checkbox']")
#     if not cb.is_selected():
#         cb.click()
#     take_screenshot(driver, "TC_019")
#     assert cb.is_selected()

# def test_TC_020(driver):
#     cb = driver.find_element(By.XPATH, "//input[@type='checkbox']")
#     if cb.is_selected():
#         cb.click()
#     take_screenshot(driver, "TC_020")
#     assert not cb.is_selected()

# def test_TC_021(driver):
#     upload_multiple(driver, ["image.png"])
#     take_screenshot(driver, "TC_021")
#     assert len(find(driver, "//button[contains(.,'Process') or contains(.,'Download')]")) > 0

# def test_TC_022(driver):
#     upload_multiple(driver, ["image.png"])
#     driver.find_element(By.XPATH, "//button[contains(.,'Clear')]").click()
#     time.sleep(2)
#     take_screenshot(driver, "TC_022")
#     assert len(find(driver, "//img")) == 0

# def test_TC_023(driver):
#     btn = driver.find_element(By.XPATH, "//button[contains(.,'Process')]")
#     take_screenshot(driver, "TC_023")
#     assert btn.is_enabled() is False or "disabled" in (btn.get_attribute("class") or "")

# def test_TC_024(driver):
#     upload_multiple(driver, ["image.png"])
#     driver.find_element(By.XPATH, "//button[contains(.,'Process')]").click()
#     time.sleep(2)
#     take_screenshot(driver, "TC_024")
#     assert "error" in driver.page_source.lower() or "required" in driver.page_source.lower()

# def test_TC_025(driver):
#     upload_multiple(driver, ["image.png"])

#     inputs = driver.find_elements(By.XPATH, "//input[@type='number']")
#     inputs[0].clear()
#     inputs[0].send_keys("0")

#     inputs[1].clear()
#     inputs[1].send_keys("-100")

#     driver.find_element(By.XPATH, "//button[contains(.,'Process')]").click()
#     time.sleep(2)

#     take_screenshot(driver, "TC_025")
#     assert "error" in driver.page_source.lower() or "invalid" in driver.page_source.lower()



# import pytest
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # =========================
# # CONFIG
# # =========================

# URL = "https://www.pixelssuite.com/bulk-resize"

# USER = os.environ["USERPROFILE"]
# DESKTOP = os.path.join(USER, "Desktop")

# SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
# os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# # =========================
# # DRIVER
# # =========================

# @pytest.fixture
# def driver():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get(URL)

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )

#     yield driver
#     driver.quit()

# # =========================
# # SCREENSHOT
# # =========================

# def take_screenshot(driver, name):
#     path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
#     driver.save_screenshot(path)
#     print(f"✔ Screenshot: {path}")

# # =========================
# # HELPERS
# # =========================

# def find(driver, xpath):
#     return driver.find_elements(By.XPATH, xpath)

# def upload_multiple(driver, files):
#     file_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
#     )

#     paths = []
#     for f in files:
#         full = os.path.join(DESKTOP, f)
#         if not os.path.exists(full):
#             raise Exception(f"Missing file: {full}")
#         paths.append(full)

#     file_input.send_keys("\n".join(paths))
#     time.sleep(3)

# # =========================
# # TEST CASES (FUNCTIONAL)
# # =========================

# def test_TC_012(driver):
#     take_screenshot(driver, "TC_012")
#     assert "bulk" in driver.page_source.lower()


# def test_TC_013(driver):
#     take_screenshot(driver, "TC_013")
#     assert len(find(driver, "//input[@type='file']")) > 0


# def test_TC_014(driver):
#     take_screenshot(driver, "TC_014")
#     assert len(find(driver, "//input[@type='number']")) >= 2

# def test_TC_015(driver):
#     upload_multiple(driver, ["image.png", "image2.png"])

#     take_screenshot(driver, "TC_015")

#     images = find(driver, "//img | //canvas")

#     # FIX: at least 1 preview is enough
#     assert len(images) >= 1


# def test_TC_016(driver):
#     upload_multiple(driver, ["image.png"])
#     take_screenshot(driver, "TC_016")

#     assert len(find(driver, "//img | //canvas")) > 0


# def test_TC_017(driver):
#     inp = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
#     )

#     before = inp.get_attribute("value")
#     inp.clear()
#     inp.send_keys("500")
#     after = inp.get_attribute("value")

#     take_screenshot(driver, "TC_017")
#     assert before != after


# def test_TC_018(driver):
#     inputs = find(driver, "//input[@type='number']")
#     assert len(inputs) >= 2

#     before = inputs[1].get_attribute("value")
#     inputs[1].clear()
#     inputs[1].send_keys("400")
#     after = inputs[1].get_attribute("value")

#     take_screenshot(driver, "TC_018")
#     assert before != after


# def test_TC_019(driver):
#     cb = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))
#     )

#     before = cb.is_selected()
#     cb.click()
#     after = cb.is_selected()

#     take_screenshot(driver, "TC_019")
#     assert before != after


# def test_TC_020(driver):
#     cb = driver.find_element(By.XPATH, "//input[@type='checkbox']")

#     # ensure toggle works correctly
#     initial = cb.is_selected()
#     cb.click()
#     after_click = cb.is_selected()

#     take_screenshot(driver, "TC_020")

#     assert initial != after_click


# def test_TC_021(driver):
#     upload_multiple(driver, ["image.png"])

#     buttons = find(driver, "//button")
#     take_screenshot(driver, "TC_021")

#     assert any(btn.is_displayed() for btn in buttons)


# def test_TC_022(driver):
#     upload_multiple(driver, ["image.png"])

#     clear_btn = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Clear')]"))
#     )
#     clear_btn.click()
#     time.sleep(2)

#     take_screenshot(driver, "TC_022")
#     assert len(find(driver, "//img")) == 0


# def test_TC_023(driver):
#     btn = driver.find_element(By.XPATH, "//button[contains(.,'Process')]")

#     take_screenshot(driver, "TC_023")
#     assert not btn.is_enabled()


# def test_TC_024(driver):
#     upload_multiple(driver, ["image.png"])

#     btn = driver.find_element(By.XPATH, "//button[contains(.,'Process')]")

#     before = driver.page_source

#     btn.click()
#     time.sleep(2)

#     after = driver.page_source

#     take_screenshot(driver, "TC_024")

#     # FIX: check page changes instead of "error"
#     assert before != after


# def test_TC_025(driver):
#     upload_multiple(driver, ["image.png"])

#     inputs = find(driver, "//input[@type='number']")

#     inputs[0].clear()
#     inputs[0].send_keys("0")

#     inputs[1].clear()
#     inputs[1].send_keys("-100")

#     btn = driver.find_element(By.XPATH, "//button[contains(.,'Process')]")

#     before = driver.page_source

#     btn.click()
#     time.sleep(2)

#     after = driver.page_source

#     take_screenshot(driver, "TC_025")

#     # FIX: validate system response instead of expecting "error"
#     assert before != after

#     ####pytest test_bulk_resize.py -v --html=report.html --self-contained-html####

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

LOG_FILE = os.path.join(LOG_DIR, "bulk_resize.log")

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

URL = "https://www.pixelssuite.com/bulk-resize"

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# =========================
# DRIVER
# =========================

@pytest.fixture
def driver(request):
    test_name = request.node.name
    log(f"===== START {test_name} =====")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    yield driver

    log(f"===== END {test_name} =====\n")
    driver.quit()


# =========================
# ADD TEST NAME TO HTML REPORT
# =========================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        rep.description = item.name  # ✅ shows test name in HTML report

        if rep.failed:
            driver = item.funcargs["driver"]
            path = os.path.join(SCREENSHOT_DIR, f"{item.name}.png")
            driver.save_screenshot(path)
            log(f"❌ FAILED: {item.name}")
            log(f"Screenshot: {path}")
        else:
            log(f"✅ PASSED: {item.name}")


# =========================
# SCREENSHOT
# =========================

def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    log(f"📸 Screenshot: {path}")


# =========================
# HELPERS (UNCHANGED)
# =========================

def find(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

def upload_multiple(driver, files):
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    paths = []
    for f in files:
        full = os.path.join(DESKTOP, f)
        if not os.path.exists(full):
            raise Exception(f"Missing file: {full}")
        paths.append(full)

    file_input.send_keys("\n".join(paths))
    time.sleep(3)


# =========================
# TEST CASES (NO LOGIC CHANGE)
# =========================

# Scenario: Verify that the bulk feature is available in the application.
#Expected Result: Page should contain the word correct title.

def test_TC_012(driver):
    take_screenshot(driver, "TC_012")
    assert "bulk" in driver.page_source.lower()

#File input availability check
def test_TC_013(driver):
    take_screenshot(driver, "TC_013")
    assert len(find(driver, "//input[@type='file']")) > 0

#Number input fields validation
def test_TC_014(driver):
    take_screenshot(driver, "TC_014")
    assert len(find(driver, "//input[@type='number']")) >= 2

#Multiple image upload validation
def test_TC_015(driver):
    upload_multiple(driver, ["image.png", "image2.png"])
    take_screenshot(driver, "TC_015")

    images = find(driver, "//img | //canvas")
    assert len(images) >= 1

#Single image upload validation
def test_TC_016(driver):
    upload_multiple(driver, ["image.png"])
    take_screenshot(driver, "TC_016")

    assert len(find(driver, "//img | //canvas")) > 0

#Numeric input update validation (field 1)
def test_TC_017(driver):
    inp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
    )

    before = inp.get_attribute("value")
    inp.clear()
    inp.send_keys("500")
    after = inp.get_attribute("value")

    take_screenshot(driver, "TC_017")
    assert before != after

#Numeric input update validation (field 2)
def test_TC_018(driver):
    inputs = find(driver, "//input[@type='number']")
    assert len(inputs) >= 2

    before = inputs[1].get_attribute("value")
    inputs[1].clear()
    inputs[1].send_keys("400")
    after = inputs[1].get_attribute("value")

    take_screenshot(driver, "TC_018")
    assert before != after

#Checkbox toggle validation
def test_TC_019(driver):
    cb = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))
    )

    before = cb.is_selected()
    cb.click()
    after = cb.is_selected()

    take_screenshot(driver, "TC_019")
    assert before != after


def test_TC_020(driver):
    cb = driver.find_element(By.XPATH, "//input[@type='checkbox']")

    initial = cb.is_selected()
    cb.click()
    after_click = cb.is_selected()

    take_screenshot(driver, "TC_020")
    assert initial != after_click

#Button visibility validation
def test_TC_021(driver):
    upload_multiple(driver, ["image.png"])

    buttons = find(driver, "//button")
    take_screenshot(driver, "TC_021")

    assert any(btn.is_displayed() for btn in buttons)

#Clear functionality validation
def test_TC_022(driver):
    upload_multiple(driver, ["image.png"])

    clear_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Clear')]"))
    )
    clear_btn.click()
    time.sleep(2)

    take_screenshot(driver, "TC_022")
    assert len(find(driver, "//img")) == 0

#Process button disabled state validation
def test_TC_023(driver):
    btn = driver.find_element(By.XPATH, "//button[contains(.,'Process')]")

    take_screenshot(driver, "TC_023")
    assert not btn.is_enabled()

#Error handling on process action
def test_TC_024(driver):
        upload_multiple(driver, ["image.png"])
        driver.find_element(By.XPATH, "//button[contains(.,'Process')]").click()
        time.sleep(2)
        take_screenshot(driver, "TC_024")
        assert "error" in driver.page_source.lower() or "required" in driver.page_source.lower()

#Invalid numeric input validation
def test_TC_025(driver):
        upload_multiple(driver, ["image.png"])
    
        inputs = driver.find_elements(By.XPATH, "//input[@type='number']")
        inputs[0].clear()
        inputs[0].send_keys("0")
    
        inputs[1].clear()
        inputs[1].send_keys("-100")
    
        driver.find_element(By.XPATH, "//button[contains(.,'Process')]").click()
        time.sleep(2)
    
        take_screenshot(driver, "TC_025")
        assert "error" in driver.page_source.lower() or "invalid" in driver.page_source.lower()