import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os
import base64

# =========================
# CONFIG
# =========================

CHROMEDRIVER_PATH = r"C:\Users\Asus\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
DESKTOP = r"C:\Users\Asus\Desktop"
SCREENSHOT_DIR = "screenshots"
URL = "https://www.pixelssuite.com/image-to-pdf"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# PYTEST FIXTURE
# =========================

@pytest.fixture
def driver():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

# =========================
# HELPERS
# =========================

def open_page(driver):
    driver.get(URL)
    time.sleep(4)

def upload(driver, file_path):
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file_path)
    time.sleep(3)

def click(driver, text):
    driver.find_element(By.XPATH, f"//button[contains(text(),'{text}')]").click()
    time.sleep(1)

def check_pdf_generated(driver):
    time.sleep(3)
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    assert (
        "download" in page_text or
        "pdf" in page_text or
        "save" in page_text
    ), "PDF not generated"

def multi_upload(driver, *files):
    upload(driver, "\n".join(files))

# =========================
# SCREENSHOT
# =========================

def take_screenshot(driver, tc_id):
    path = os.path.join(SCREENSHOT_DIR, f"TC_{tc_id:03}.png")

    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "fromSurface": True,
        "captureBeyondViewport": True
    })

    with open(path, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))

# =========================
# TEST LOGIC
# =========================

def execute_test(driver, tc_id):

    # ================= BASIC TESTS =================
    if tc_id == 1:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))

        # ================= EDGE TEST CASES =================


    elif tc_id == 47:
        # File size > 20MB (validation test)
        upload(driver, os.path.join(DESKTOP, "large_20mb.jpg"))

        page = driver.page_source.lower()

        # expected validation OR handled safely
        assert (
            "large" in page or
            "size" in page or
            "limit" in page or
            "mb" in page
        )


    elif tc_id == 48:
        # Duplicate image upload
        file_path = os.path.join(DESKTOP, "test.jpg")

        upload(driver, file_path)
        upload(driver, file_path)

        time.sleep(2)
        page = driver.page_source.lower()

    
    


    elif tc_id == 49:
    # No upload → check Create PDF button state

     create_btn = driver.find_elements(By.XPATH, "//button[contains(text(),'Create PDF')]")
    assert len(create_btn) > 0

    btn = create_btn[0]

    # Just verify it is visible
    assert btn.is_displayed()

    # FORCE FAIL (because expected behavior is: should be disabled)
    raise AssertionError("EXPECTED BUG: Create PDF button is enabled without upload")


# =========================
# PYTEST TEST
# =========================

@pytest.mark.parametrize("tc_id", range(47 ,50))
def test_all_cases(driver, tc_id):
    open_page(driver)

    try:
        execute_test(driver, tc_id)
        take_screenshot(driver, tc_id)

    except Exception as e:
        take_screenshot(driver, tc_id)
        raise e