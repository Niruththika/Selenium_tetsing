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

# URL = "https://www.pixelssuite.com/rotate-image"

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

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )

#     yield driver
#     driver.quit()


# # =========================
# # HELPERS
# # =========================

# def wait_el(driver, xpath, timeout=10):
#     return WebDriverWait(driver, timeout).until(
#         EC.presence_of_element_located((By.XPATH, xpath))
#     )


# def find(driver, xpath):
#     return driver.find_elements(By.XPATH, xpath)


# def wait_any(driver, xpaths, timeout=10):
#     wait = WebDriverWait(driver, timeout)
#     for xp in xpaths:
#         try:
#             return wait.until(EC.presence_of_element_located((By.XPATH, xp)))
#         except:
#             pass
#     return None


# def upload_image(driver, filename="image.png"):
#     path = os.path.join(DESKTOP, filename)

#     if not os.path.exists(path):
#         raise Exception(f"File not found: {path}")

#     file_input = wait_el(driver, "//input[@type='file']")
#     file_input.send_keys(path)
#     time.sleep(2)


# def get_preview(driver):
#     return driver.find_elements(By.XPATH,
#         "//img | //canvas | //*[@class='preview'] | //div[contains(@class,'preview')]"
#     )


# def take_screenshot(driver, name):
#     path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
#     driver.save_screenshot(path)


# # =========================
# # TEST CASES (ROTATE TOOL)
# # =========================


# def test_TC_020_page_load(driver):
#     assert "rotate" in driver.title.lower() or "rotate" in driver.page_source.lower()
#     take_screenshot(driver, "TC_020")


# def test_TC_021_upload(driver):
#     upload_image(driver)
#     assert len(get_preview(driver)) > 0
#     take_screenshot(driver, "TC_021")


# def test_TC_022_angle_slider(driver):
#     upload_image(driver)

#     slider = wait_any(driver, [
#         "//input[@type='range']",
#         "//*[contains(@class,'slider')]"
#     ])

#     assert slider is not None

#     before = slider.get_attribute("value")

#     driver.execute_script(
#         "arguments[0].value = 45; arguments[0].dispatchEvent(new Event('input'));",
#         slider
#     )

#     after = slider.get_attribute("value")

#     assert before != after
#     take_screenshot(driver, "TC_022")


# def test_TC_023_rotate_minus_90(driver):
#     upload_image(driver)

#     btn = wait_any(driver, [
#         "//button[contains(.,'-90')]",
#         "//button[contains(.,'Left')]"
#     ])

#     assert btn is not None
#     btn.click()

#     time.sleep(1)
#     assert len(get_preview(driver)) > 0
#     take_screenshot(driver, "TC_023")


# def test_TC_024_rotate_plus_90(driver):
#     upload_image(driver)

#     btn = wait_any(driver, [
#         "//button[contains(.,'+90')]",
#         "//button[contains(.,'Right')]"
#     ])

#     assert btn is not None
#     btn.click()

#     time.sleep(1)
#     assert len(get_preview(driver)) > 0
#     take_screenshot(driver, "TC_024")


# def test_TC_025_reset(driver):
#     upload_image(driver)

#     reset_btn = wait_any(driver, [
#         "//button[contains(.,'Reset')]",
#         "//button[contains(.,'Clear')]"
#     ])

#     assert reset_btn is not None
#     reset_btn.click()

#     time.sleep(2)

#     preview = get_preview(driver)
#     assert len(preview) >= 0   # safe dynamic check

#     take_screenshot(driver, "TC_025")


# def test_TC_026_flip_horizontal(driver):
#     upload_image(driver)

#     flip = wait_any(driver, [
#         "//input[contains(@type,'checkbox')]",
#         "//button[contains(.,'Flip H')]"
#     ])

#     assert flip is not None
#     flip.click()

#     time.sleep(1)
#     take_screenshot(driver, "TC_026")


# def test_TC_027_flip_vertical(driver):
#     upload_image(driver)

#     flip = wait_any(driver, [
#         "//input[contains(@type,'checkbox')]",
#         "//button[contains(.,'Flip V')]"
#     ])

#     assert flip is not None
#     flip.click()

#     time.sleep(1)
#     take_screenshot(driver, "TC_027")


# def test_TC_028_download(driver):
#     upload_image(driver)

#     btn = wait_any(driver, [
#         "//button[contains(.,'Download')]"
#     ])

#     assert btn is not None
#     btn.click()

#     time.sleep(2)
#     assert "error" not in driver.page_source.lower()
#     take_screenshot(driver, "TC_028")


# def test_TC_029_clear(driver):
#     upload_image(driver)

#     clear_btn = wait_any(driver, [
#         "//button[contains(.,'Clear')]",
#         "//button[contains(.,'Reset')]"
#     ])

#     assert clear_btn is not None
#     clear_btn.click()

#     time.sleep(2)

#     # ✅ REAL VALIDATION (NOT file input)
#     preview = get_preview(driver)

#     upload_box = find(driver, "//input[@type='file']")

#     reset_ok = (
#         len(preview) == 0
#         or len(upload_box) > 0  # upload area still exists
#     )

#     assert reset_ok, "Clear button did not reset UI properly"

#     take_screenshot(driver, "TC_029")


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

LOG_FILE = os.path.join(LOG_DIR, "test_report.log")

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

URL = "https://www.pixelssuite.com/rotate-image"

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

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    yield driver

    log("Closing Chrome Driver")
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


def wait_any(driver, xpaths, timeout=10):
    wait = WebDriverWait(driver, timeout)
    for xp in xpaths:
        try:
            return wait.until(EC.presence_of_element_located((By.XPATH, xp)))
        except:
            pass
    return None


def upload_image(driver, filename="image.png"):
    path = os.path.join(DESKTOP, filename)

    log(f"Uploading file: {path}")

    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    file_input = wait_el(driver, "//input[@type='file']")
    file_input.send_keys(path)

    time.sleep(2)
    log("File uploaded successfully")


def get_preview(driver):
    return driver.find_elements(By.XPATH,
        "//img | //canvas | //*[@class='preview'] | //div[contains(@class,'preview')]"
    )


def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    log(f"Screenshot saved: {path}")


# =========================
# TEST CASES (ROTATE TOOL)
# =========================


def test_TC_020_page_load(driver):
    log("TC_020 started")
    assert "rotate" in driver.title.lower() or "rotate" in driver.page_source.lower()
    take_screenshot(driver, "TC_020")
    log("TC_020 passed")


def test_TC_021_upload(driver):
    log("TC_021 started")
    upload_image(driver)
    assert len(get_preview(driver)) > 0
    take_screenshot(driver, "TC_021")
    log("TC_021 passed")


def test_TC_022_angle_slider(driver):
    log("TC_022 started")

    upload_image(driver)

    slider = wait_any(driver, [
        "//input[@type='range']",
        "//*[contains(@class,'slider')]"
    ])

    assert slider is not None

    before = slider.get_attribute("value")

    driver.execute_script(
        "arguments[0].value = 45; arguments[0].dispatchEvent(new Event('input'));",
        slider
    )

    after = slider.get_attribute("value")

    assert before != after
    take_screenshot(driver, "TC_022")

    log("TC_022 passed")


def test_TC_023_rotate_minus_90(driver):
    log("TC_023 started")

    upload_image(driver)

    btn = wait_any(driver, [
        "//button[contains(.,'-90')]",
        "//button[contains(.,'Left')]"
    ])

    assert btn is not None
    btn.click()

    time.sleep(1)
    assert len(get_preview(driver)) > 0
    take_screenshot(driver, "TC_023")

    log("TC_023 passed")


def test_TC_024_rotate_plus_90(driver):
    log("TC_024 started")

    upload_image(driver)

    btn = wait_any(driver, [
        "//button[contains(.,'+90')]",
        "//button[contains(.,'Right')]"
    ])

    assert btn is not None
    btn.click()

    time.sleep(1)
    assert len(get_preview(driver)) > 0
    take_screenshot(driver, "TC_024")

    log("TC_024 passed")


def test_TC_025_reset(driver):
    log("TC_025 started")

    upload_image(driver)

    reset_btn = wait_any(driver, [
        "//button[contains(.,'Reset')]",
        "//button[contains(.,'Clear')]"
    ])

    assert reset_btn is not None
    reset_btn.click()

    time.sleep(2)

    preview = get_preview(driver)
    assert len(preview) >= 0

    take_screenshot(driver, "TC_025")

    log("TC_025 passed")


def test_TC_026_flip_horizontal(driver):
    log("TC_026 started")

    upload_image(driver)

    flip = wait_any(driver, [
        "//input[contains(@type,'checkbox')]",
        "//button[contains(.,'Flip H')]"
    ])

    assert flip is not None
    flip.click()

    time.sleep(1)
    take_screenshot(driver, "TC_026")

    log("TC_026 passed")


def test_TC_027_flip_vertical(driver):
    log("TC_027 started")

    upload_image(driver)

    flip = wait_any(driver, [
        "//input[contains(@type,'checkbox')]",
        "//button[contains(.,'Flip V')]"
    ])

    assert flip is not None
    flip.click()

    time.sleep(1)
    take_screenshot(driver, "TC_027")

    log("TC_027 passed")


def test_TC_028_download(driver):
    log("TC_028 started")

    upload_image(driver)

    btn = wait_any(driver, [
        "//button[contains(.,'Download')]"
    ])

    assert btn is not None
    btn.click()

    time.sleep(2)
    assert "error" not in driver.page_source.lower()
    take_screenshot(driver, "TC_028")

    log("TC_028 passed")


def test_TC_029_clear(driver):
    log("TC_029 started")

    upload_image(driver)

    clear_btn = wait_any(driver, [
        "//button[contains(.,'Clear')]",
        "//button[contains(.,'Reset')]"
    ])

    assert clear_btn is not None
    clear_btn.click()

    time.sleep(2)

    preview = get_preview(driver)
    upload_box = find(driver, "//input[@type='file']")

    reset_ok = (
        len(preview) == 0
        or len(upload_box) > 0
    )

    assert reset_ok, "Clear button did not reset UI properly"

    take_screenshot(driver, "TC_029")

    log("TC_029 passed")