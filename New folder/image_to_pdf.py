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
# TEST CASE NAMES (UPDATED)
# =========================
TC_NAMES = {
    1: "TC_001 - Upload valid image",
    2: "TC_002 - Upload multiple images",
    3: "TC_003 - Skip test case",
    4: "TC_004 - Upload invalid file (PDF)",
    5: "TC_005 - Upload large image",
    6: "TC_006 - Remove uploaded image",
    7: "TC_007 - Multiple upload validation",
    8: "TC_008 - No action",
    9: "TC_009 - Upload single image again",
    10: "TC_010 - Upload 3 images",
    11: "TC_011 - Upload then remove image",

    13: "TC_013 - Select A4 size",
    14: "TC_014 - Select Letter size",
    15: "TC_015 - Select Portrait mode",
    16: "TC_016 - Select Landscape mode",
    17: "TC_017 - Select Vertical layout",
    18: "TC_018 - Select Horizontal layout",
    19: "TC_019 - Select single page",
    20: "TC_020 - Select multiple pages",
    21: "TC_021 - Settings combination test",

   22: "TC_022 - A4 + Portrait + Vertical + Single",
    23: "TC_023 - A4 + Portrait + Horizontal + Single",
    24: "TC_024 - A4 + Landscape + Vertical + Single",
    25: "TC_025 - A4 + Landscape + Horizontal + Single",
    26: "TC_026 - A4 + Portrait + Vertical + Multiple",
    27: "TC_027 - A4 + Landscape + Horizontal + Multiple",
    28: "TC_028 - A4 + Portrait + Horizontal + Multiple",
    29: "TC_029 - A4 + Landscape + Vertical + Multiple",

    30: "TC_030 - Letter + Portrait + Vertical + Single",
    31: "TC_031 - Letter + Portrait + Horizontal + Single",
    32: "TC_032 - Letter + Landscape + Vertical + Single",
    33: "TC_033 - Letter + Landscape + Horizontal + Single",
    34: "TC_034 - Letter + Portrait + Vertical + Multiple",
    35: "TC_035 - Letter + Landscape + Horizontal + Multiple",
    36: "TC_036 - Letter + Portrait + Horizontal + Multiple",
    37: "TC_037 - Letter + Landscape + Vertical + Multiple",

    38: "TC_038 - Upload corrupt image",
    39: "TC_039 - Upload unsupported file (PPTX)",
    40: "TC_040 - Refresh after upload",
    41: "TC_041 - Upload long filename image",
    42: "TC_042 - Resize window small",
    43: "TC_043 - Mobile view UI check",

    45: "TC_045 - Upload PDF error validation",

    47: "TC_047 - File size > 20MB validation",
    48: "TC_048 - Duplicate image upload",
    49: "TC_049 - Create button without upload (Expected FAIL)"
}

# =========================
# FIXTURE
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

    if tc_id == 1:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))

    elif tc_id == 2:
        multi_upload(driver,
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg"))

    elif tc_id == 3:
        pytest.skip("Skipped test case")

    elif tc_id == 4:
        upload(driver, os.path.join(DESKTOP, "test.pdf"))
        page = driver.page_source.lower()
        assert "invalid" in page or "unsupported" in page

    elif tc_id == 5:
     upload(driver, os.path.join(DESKTOP, "big.jpg"))

    page = driver.page_source.lower()

    # If system does NOT show any restriction message → it's a failure
    if "large" not in page and "limit" not in page and "mb" not in page:
        assert False, "FAIL: System allowed large file upload (should be restricted)"

    elif tc_id == 6:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))
        driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()

    elif tc_id == 7:
        multi_upload(driver,
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg"))

    elif tc_id == 8:
        pass

    elif tc_id == 9:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))

    elif tc_id == 10:
        multi_upload(driver,
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg"),
            os.path.join(DESKTOP, "test.jpg"))

    elif tc_id == 11:
        upload(driver, os.path.join(DESKTOP, "test.jpg"))
        driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()

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

    elif 22 <= tc_id <= 37:

        upload(driver, os.path.join(DESKTOP, "test.jpg"))

        # A4 vs Letter
        if tc_id <= 29:
            click(driver, "A4")
        else:
            click(driver, "Letter")

        # Portrait vs Landscape
        if tc_id in [22,23,26,28,30,31,34,36]:
            click(driver, "Portrait")
        else:
            click(driver, "Landscape")

        # Vertical vs Horizontal
        if tc_id in [22,24,26,29,30,32,34,37]:
            click(driver, "Vertical")
        else:
            click(driver, "Horizontal")

        # One vs Multiple
        if tc_id in [22,23,24,25,30,31,32,33]:
            click(driver, "One")
        else:
            click(driver, "Multiple")

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

    elif tc_id == 47:
        upload(driver, os.path.join(DESKTOP, "large_20mb.jpg"))
        page = driver.page_source.lower()
        assert "large" in page or "size" in page or "limit" in page or "mb" in page

    elif tc_id == 48:
        # Duplicate image upload
        file_path = os.path.join(DESKTOP, "test.jpg")

        upload(driver, file_path)
        upload(driver, file_path)

        time.sleep(2)
        page = driver.page_source.lower()


    elif tc_id == 49:
        create_btn = driver.find_elements(By.XPATH, "//button[contains(text(),'Create PDF')]")
        assert len(create_btn) > 0
        assert create_btn[0].is_displayed()
        assert False, "Expected FAIL: Button should be disabled"

# =========================
# TEST RUNNER
# =========================
@pytest.mark.parametrize(
    "tc_id",
    range(1, 50),
    ids=lambda x: TC_NAMES.get(x, f"TC_{x:03}")
)
def test_all_cases(driver, tc_id):

    print(f"\nRunning: {TC_NAMES.get(tc_id)}")

    open_page(driver)

    try:
        execute_test(driver, tc_id)
        take_screenshot(driver, tc_id)
    except Exception as e:
        take_screenshot(driver, tc_id)
        raise e

# =========================
# HTML REPORT
# =========================
def pytest_html_report_title(report):
    report.title = "Image to PDF Automation Report"

import pytest_html

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, "extra", [])

    if report.when in ("call", "setup"):
        tc_id = item.callspec.params.get("tc_id") if hasattr(item, "callspec") else None

        if tc_id:
            file_name = f"screenshots/TC_{tc_id:03}.png"

            if os.path.exists(file_name):
                extra.append(pytest_html.extras.image(file_name))

    report.extra = extra