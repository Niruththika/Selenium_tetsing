import pytest
import os
import time
import base64
import logging
import pytest_html
from selenium import webdriver
from selenium.webdriver.common.by import By

# =========================
# CONFIG
# =========================

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
URL = "https://www.pixelssuite.com/word-to-pdf"

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# LOGGING SETUP
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
    "test_TC_0001_upload_convert": "TC_0001 - Upload valid DOCX and convert",
    "test_TC_0002_file_upload_validation": "TC_0002 - File upload validation",
    "test_TC_0003_image_file": "TC_0003 - Upload image file (negative test)",
    "test_TC_0004_empty_file": "TC_0004 - Upload empty DOCX",
    "test_TC_0005_large_file": "TC_0005 - Large file conversion",
    "test_TC_0006_multiple_files": "TC_0006 - Multiple file upload",
    "test_TC_0007_page_load": "TC_0007 - Page load validation",
    "test_TC_0008_refresh_behavior": "TC_0008 - Refresh behavior test",
    "test_TC_0009_single_conversion": "TC_0009 - Single DOCX conversion",
    "test_TC_0010_styled_conversion": "TC_0010 - Styled DOCX conversion",
    "test_TC_0011_multi_page": "TC_0011 - Multi-page DOCX conversion",
    "test_TC_0012_long_filename": "TC_0012 - Long filename handling",
    "test_TC_0013_ui_button_check": "TC_0013 - UI button check",
    "test_TC_0014_page_ready": "TC_0014 - Page ready state",
    "test_TC_0015_responsive": "TC_0015 - Responsive UI check",
    "test_TC_0016_ui_validation": "TC_0016 - UI validation negative",
    "test_TC_0017_convert_flow": "TC_0017 - Convert flow test",
    "test_TC_0018_refresh_clears_file": "TC_0018 - Refresh clears file"
}

# =========================
# FIXTURE
# =========================

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()

# =========================
# HELPERS
# =========================

def open_page(driver):
    log("Opening page")
    driver.get(URL)
    time.sleep(3)

def upload(driver, file):
    log(f"Uploading file: {file}")

    if not os.path.exists(file):
        raise Exception(f"File not found: {file}")

    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file)
    time.sleep(2)

def click_convert(driver):
    log("Click convert")
    btn = driver.find_element(By.XPATH, "//button")
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(3)

def page_text(driver):
    return driver.page_source.lower()

def take_screenshot(driver, tc_id):
    path = os.path.join(SCREENSHOT_DIR, f"{tc_id}.png")

    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "fromSurface": True,
        "captureBeyondViewport": True
    })

    with open(path, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))

    return path

# =========================
# TEST CASES
# =========================

def test_TC_0001_upload_convert(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    click_convert(driver)

    assert "pdf" in page_text(driver) or "download" in page_text(driver)

    take_screenshot(driver, "TC_0001")


def test_TC_0002_file_upload_validation(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    take_screenshot(driver, "TC_0002")


def test_TC_0003_image_file(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "image.png"))

    ERROR_MESSAGES = ["error", "invalid", "unsupported"]

    assert any(msg in page_text(driver) for msg in ERROR_MESSAGES)

    take_screenshot(driver, "TC_0003")


def test_TC_0004_empty_file(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "empty.docx"))

    expected = ["error", "invalid", "failed"]
    assert any(msg in page_text(driver) for msg in expected)

    take_screenshot(driver, "TC_0004")


def test_TC_0005_large_file(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "large.docx"))
    click_convert(driver)

    take_screenshot(driver, "TC_0005")

   
    assert False, "Large file should not be accepted"


def test_TC_0006_multiple_files(driver):
    open_page(driver)

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")

    file1 = os.path.join(DESKTOP, "test1.docx")
    file2 = os.path.join(DESKTOP, "test2.docx")

    # try multi upload
    file_input.send_keys(file1)
    file_input.send_keys(file2)

    time.sleep(3)

    # check what is actually stored in input
    value = file_input.get_attribute("value") or ""

    
    assert "," not in value, "System allowed multiple file selection"

    take_screenshot(driver, "TC_0006")


def test_TC_0007_page_load(driver):
    open_page(driver)
    take_screenshot(driver, "TC_0007")


def test_TC_0008_refresh_behavior(driver):
    open_page(driver)
    driver.refresh()
    time.sleep(2)

    assert driver.execute_script("return document.readyState") == "complete"

    take_screenshot(driver, "TC_0008")


def test_TC_0009_single_conversion(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    click_convert(driver)

    take_screenshot(driver, "TC_0009")


def test_TC_0010_styled_conversion(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "styled.docx"))
    click_convert(driver)

    time.sleep(5)

    page = page_text(driver)

    assert len(page) > 500
    assert "failed" not in page
    assert "unsupported" not in page

    take_screenshot(driver, "TC_0010")


def test_TC_0011_multi_page(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "multipage.docx"))
    click_convert(driver)

    take_screenshot(driver, "TC_0011")


def test_TC_0012_long_filename(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "verylongfilename.docx"))

    take_screenshot(driver, "TC_0012")


def test_TC_0013_ui_button_check(driver):
    open_page(driver)

    assert len(driver.find_elements(By.TAG_NAME, "button")) > 0

    take_screenshot(driver, "TC_0013")


def test_TC_0014_page_ready(driver):
    open_page(driver)

    assert driver.execute_script("return document.readyState") == "complete"

    take_screenshot(driver, "TC_0014")


def test_TC_0015_responsive(driver):
    driver.set_window_size(375, 812)
    time.sleep(3)

  
    if driver.execute_script("return document.readyState") != "complete":
        assert False, "Page not loaded properly in mobile view"

    
    file_input = driver.find_elements(By.XPATH, "//input[@type='file']")
    buttons = driver.find_elements(By.TAG_NAME, "button")

    if len(file_input) == 0:
        assert False, "Upload input missing in mobile view"

    if len(buttons) == 0:
        assert False, "Buttons missing in mobile view"

    
    body = driver.page_source.lower()

    broken_signals = [
        "error",
        "failed",
        "unsupported",
        "not available",
        "cannot",
        "broken"
    ]

    for word in broken_signals:
        if word in body:
            assert False, f"UI broken detected: {word}"

    if len(body) < 300:
        assert False, "Page content too small → UI not rendered properly"

    
    take_screenshot(driver, "TC_0015")


def test_TC_0016_ui_validation(driver):
    open_page(driver)

    body = driver.page_source.lower()

    assert "jpg" not in body
    assert "png" not in body

    take_screenshot(driver, "TC_0016")


def test_TC_0017_convert_flow(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    click_convert(driver)

    take_screenshot(driver, "TC_0017")


def test_TC_0018_refresh_clears_file(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))

    driver.refresh()
    time.sleep(2)

    assert "test.docx" not in page_text(driver)

    take_screenshot(driver, "TC_0018")

# =========================
# REPORT TITLE
# =========================

def pytest_html_report_title(report):
    report.title = "Word to PDF Automation Test Report"

# =========================
# ADD TEST NAME + SCREENSHOT + LOGS
# =========================

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
        tc_id = test_name.replace("test_", "")

        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{tc_id}.png")

        if os.path.exists(screenshot_path):
            extra.append(pytest_html.extras.image(screenshot_path))

        # attach logs
        if os.path.exists("execution.log"):
            with open("execution.log", "r") as f:
                logs = f.read()

            extra.append(pytest_html.extras.text(logs, name="Execution Logs"))

    report.extra = extra