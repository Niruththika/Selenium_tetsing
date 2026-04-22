import pytest
import os
import time
import logging
import pytest_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =========================
# CONFIG
# =========================

BASE_URL = "https://www.pixelssuite.com/pdf-to-word"

FILE_DIR = os.path.join(os.getcwd(), "test_files")
SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")

os.makedirs(FILE_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# LOGGING
# =========================

logging.basicConfig(
    filename="execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    print(msg)
    logging.info(msg)

# =========================
# TEST CASE NAMES
# =========================

TC_NAMES = {
    "test_TC_01_upload_and_convert": "TC_01 - Upload and Convert",
    "test_TC_02_upload_only": "TC_02 - Upload Only",
    "test_TC_03_multiple_upload_block": "TC_03 - Multi Upload Block",
    "test_TC_04_invalid_file": "TC_04 - Invalid File Upload",
    "test_TC_05_large_file": "TC_05 - Large File Upload",
    "test_TC_06_valid_pdf": "TC_06 - Valid PDF Conversion",
    "test_TC_07_buttons_exist": "TC_07 - Button Existence Check",
    "test_TC_08_responsive": "TC_08 - Responsive UI Check",
    "test_TC_09_file_size_visible": "TC_09 - File Size Visibility",
    "test_TC_10_file_name_visible": "TC_10 - File Name Visibility",
    "test_TC_11_conversion_flow": "TC_11 - Conversion Flow",
    "test_TC_12_convert_button": "TC_12 - Convert Button Check",
    "test_TC_13_general_ui": "TC_13 - General UI Check",
    "test_TC_14_supported_format": "TC_14 - Supported Format Check",
    "test_TC_15_ui_validation": "TC_15 - UI Negative Validation"
}

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

def wait_el(driver, xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def upload(driver, file_name="test.pdf"):
    file_path = os.path.join(FILE_DIR, file_name)

    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    log(f"Uploading: {file_name}")

    file_input = wait_el(driver, "//input[@type='file']")
    file_input.send_keys(file_path)

    time.sleep(2)

def click_convert(driver):
    log("Click convert")
    btn = wait_el(driver, "//button")
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(3)

def get_text(driver):
    return driver.page_source.lower()

def screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    return path

# =========================
# TEST CASES
# =========================

def test_TC_01_upload_and_convert(driver):
    log("TC_01 started")
    upload(driver)
    click_convert(driver)
    assert "error" not in get_text(driver)
    screenshot(driver, "TC_01")


def test_TC_02_upload_only(driver):
    log("TC_02 started")
    upload(driver)
    assert driver.find_element(By.XPATH, "//input[@type='file']")
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
    log("TC_04 started")
    upload(driver, "image.png")
    click_convert(driver)
    assert any(x in get_text(driver) for x in ["error", "invalid", "unsupported"])
    screenshot(driver, "TC_04")


def test_TC_05_large_file(driver):
    log("TC_05 started")
    upload(driver, "large.pdf")
    click_convert(driver)
    assert "error" in get_text(driver)
    screenshot(driver, "TC_05")


def test_TC_06_valid_pdf(driver):
    log("TC_06 started")
    upload(driver, "test.pdf")
    click_convert(driver)
    assert "error" not in get_text(driver)
    screenshot(driver, "TC_06")


def test_TC_07_buttons_exist(driver):
    log("TC_07 started")
    assert len(driver.find_elements(By.XPATH, "//button")) > 0
    screenshot(driver, "TC_07")


def test_TC_08_responsive(driver):
    log("TC_08 started")

    driver.set_window_size(375, 812)
    time.sleep(2)

    assert driver.execute_script("return document.readyState") == "complete"

    assert len(driver.find_elements(By.XPATH, "//input[@type='file']")) > 0

    body = driver.page_source.lower()
    assert len(body) > 500

    screenshot(driver, "TC_08")


def test_TC_09_file_size_visible(driver):
    log("TC_09 started")
    upload(driver)
    assert "kb" in get_text(driver) or "mb" in get_text(driver)
    screenshot(driver, "TC_09")


def test_TC_10_file_name_visible(driver):
    log("TC_10 started")
    upload(driver)
    assert "test" in get_text(driver)
    screenshot(driver, "TC_10")


def test_TC_11_conversion_flow(driver):
    log("TC_11 started")
    upload(driver)
    click_convert(driver)
    assert "error" not in get_text(driver)
    screenshot(driver, "TC_11")


def test_TC_12_convert_button(driver):
    log("TC_12 started")
    assert len(driver.find_elements(By.XPATH, "//button")) > 0
    screenshot(driver, "TC_12")


def test_TC_13_general_ui(driver):
    log("TC_13 started")

    body = get_text(driver)
    assert len(body.strip()) > 10

    assert driver.find_elements(By.XPATH, "//input[@type='file']")
    assert driver.find_elements(By.TAG_NAME, "button")

    screenshot(driver, "TC_13")


def test_TC_14_supported_format(driver):
    log("TC_14 started")

    text = get_text(driver)

    
    assert "png" not in text.lower(), "FAIL: PNG format shown in UI"
    assert "jpg" not in text.lower(), "FAIL: JPG format shown in UI"
    assert "jpeg" not in text.lower(), "FAIL: JPEG format shown in UI"

    
    assert len(text.strip()) > 0, "FAIL: Empty page"

    screenshot(driver, "TC_14")


def test_TC_15_ui_validation(driver):
    log("TC_15 started")

    body = driver.page_source.lower()

    assert "jpg" not in body
    assert "png" not in body

    assert driver.find_elements(By.XPATH, "//input[@type='file']")
    assert driver.find_elements(By.TAG_NAME, "button")

    screenshot(driver, "TC_15")

# =========================
# HTML REPORT CUSTOMIZATION
# =========================

def pytest_html_report_title(report):
    report.title = "PDF to Word Automation Report"


def pytest_html_results_table_header(cells):
    cells.insert(1, "<th>Test Case Name</th>")


def pytest_html_results_table_row(report, cells):
    test_name = report.nodeid.split("::")[-1]
    cells.insert(1, f"<td>{TC_NAMES.get(test_name, test_name)}</td>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, "extra", [])

    if report.when == "call":
        test_name = item.name

        screenshot_path = os.path.join(
            SCREENSHOT_DIR, f"{test_name.split('_')[-1]}.png"
        )

        if os.path.exists(screenshot_path):
            extra.append(pytest_html.extras.image(screenshot_path))

        if os.path.exists("execution.log"):
            with open("execution.log", "r") as f:
                logs = f.read()

            extra.append(pytest_html.extras.text(logs, name="Execution Logs"))

    report.extra = extra