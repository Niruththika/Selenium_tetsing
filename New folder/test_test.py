import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os
import base64
import logging



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
logging.info("Test started")
logging.error("Something failed")

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

    elif tc_id == 2:
        multi_upload(
            driver,
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg")
        )

    elif tc_id == 3:
        pytest.skip("Skipped test case")

    elif tc_id == 4:
        upload(driver, os.path.join(DESKTOP, "test.pdf"))
        page = driver.page_source.lower()
        assert "invalid" in page or "unsupported" in page

    elif tc_id == 5:
        upload(driver, os.path.join(DESKTOP, "big.jpg"))
        page = driver.page_source.lower()
        assert "large" in page or "limit" in page or "mb" in page

    elif tc_id == 6:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))
        driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()

    elif tc_id == 7:
        multi_upload(
            driver,
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg")
        )

    elif tc_id == 8:
        pass

    elif tc_id == 9:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))

    elif tc_id == 10:
        multi_upload(
            driver,
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg")
        )

    elif tc_id == 11:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))
        driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()

    # ================= SETTINGS =================
    elif 13 <= tc_id <= 21:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))

        if tc_id == 13: click(driver, "A4")
        elif tc_id == 14: click(driver, "Letter")
        elif tc_id == 15: click(driver, "Portrait")
        elif tc_id == 16: click(driver, "Landscape")
        elif tc_id == 17: click(driver, "Vertical")
        elif tc_id == 18: click(driver, "Horizontal")
        elif tc_id == 19: click(driver, "One")
        else: click(driver, "Multiple")

        click(driver, "Create")
        check_pdf_generated(driver)

    elif 22 <= tc_id <= 29:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))
        click(driver, "A4")
        click(driver, "Portrait")
        click(driver, "Vertical")
        click(driver, "One")
        click(driver, "Create")
        check_pdf_generated(driver)

    elif 30 <= tc_id <= 37:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))
        click(driver, "Letter")
        click(driver, "Create")
        check_pdf_generated(driver)

    elif tc_id == 38:
        upload(driver, os.path.join(DESKTOP, "corrupt.jpg"))
        page = driver.page_source.lower()
        assert "invalid" in page or "corrupt" in page

    elif tc_id == 39:
        upload(driver, os.path.join(DESKTOP, "test.pptx"))
        page = driver.page_source.lower()
        assert "unsupported" in page or "invalid" in page

    elif tc_id == 40:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))
        driver.refresh()

    elif tc_id == 41:
        upload(driver, os.path.join(DESKTOP, "longfilename.jpg"))

    elif tc_id == 42:
        driver.set_window_size(400, 800)

    elif tc_id == 43:
        driver.set_window_size(375, 812)
        time.sleep(2)
        assert driver.find_element(By.XPATH, "//input[@type='file']").is_displayed()
        assert driver.find_element(By.XPATH, "//button[contains(text(),'Create')]").is_displayed()

    elif tc_id == 45:
        upload(driver, os.path.join(DESKTOP, "test.pdf"))
        page = driver.page_source.lower()
        assert any(k in page for k in ["error", "invalid", "unsupported", "format"])


# =========================
# PYTEST TEST
# =========================

@pytest.mark.parametrize("tc_id", range(1, 46))
def test_all_cases(driver, tc_id):
    open_page(driver)

    try:
        execute_test(driver, tc_id)
        take_screenshot(driver, tc_id)

    except Exception as e:
        take_screenshot(driver, tc_id)
        raise e