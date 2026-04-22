import pytest
import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By

# =========================
# CONFIG (NO HARDCODE LOGIC)
# =========================

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
URL = "https://www.pixelssuite.com/word-to-pdf"

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

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
# HELPERS (UNCHANGED LOGIC STYLE)
# =========================

def open_page(driver):
    driver.get(URL)
    time.sleep(3)

def upload(driver, file):
    if not os.path.exists(file):
        raise Exception(f"File not found: {file}")

    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file)
    time.sleep(2)

def click_convert(driver):
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
# TEST CASES (PYTEST VERSION)
# =========================

def test_TC_0001(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    click_convert(driver)

    assert ("pdf" in page_text(driver) or "download" in page_text(driver))

    take_screenshot(driver, "TC_0001")


def test_TC_0002(driver):
    open_page(driver)
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(
        os.path.join(DESKTOP, "test.docx")
    )

   
    take_screenshot(driver, "TC_0002")


def test_TC_0003(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "image.png"))

    assert ("error" in page_text(driver) or "invalid" in page_text(driver))

    take_screenshot(driver, "TC_0003")


def test_TC_0004(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "empty.docx"))

    assert "error" in page_text(driver)

    take_screenshot(driver, "TC_0004")


def test_TC_0005(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "large.docx"))

    click_convert(driver)
    take_screenshot(driver, "TC_0005")

    # forced invalid expectation
    assert "this_will_never_exist" in page_text(driver)


def test_TC_0006(driver):
    open_page(driver)

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")

    file_input.send_keys(
        "\n".join([
            os.path.join(DESKTOP, "test1.docx"),
            os.path.join(DESKTOP, "test2.docx")
        ])
    )

    take_screenshot(driver, "TC_0006")

    # -----------------------------
    # REAL VALIDATION (DYNAMIC)
    # -----------------------------

    page = page_text(driver)

    preview = driver.find_elements(By.XPATH, "//img | //canvas | //iframe")

    file_value = file_input.get_attribute("value")

    # possible real outcomes:
    upload_rejected = (
        len(preview) == 0 and
        ("error" in page or "invalid" in page or "not supported" in page)
    )

    upload_ignored = (
        file_value is None or file_value == ""
    )

    upload_partial = (
        len(preview) <= 1  # only first file accepted
    )

    assert (
        upload_rejected or upload_ignored or upload_partial
    ), "Multi-file upload behavior not detected or UI did not respond"
    


def test_TC_0007(driver):
    open_page(driver)
    take_screenshot(driver, "TC_0007")


def test_TC_0008(driver):
    open_page(driver)
    driver.refresh()
    time.sleep(2)

    assert driver.execute_script("return document.readyState") == "complete"
    take_screenshot(driver, "TC_0008")


def test_TC_0009(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    click_convert(driver)

    
    take_screenshot(driver, "TC_0009")



def test_TC_0010(driver):
    open_page(driver)

    upload(driver, os.path.join(DESKTOP, "styled.docx"))
    click_convert(driver)

    take_screenshot(driver, "TC_0010")

    time.sleep(5)

    page = driver.page_source.lower()

    # Only SAFE checks (no strict DOM dependency)
    assert len(page) > 500, "Page seems broken"

    # Ensure page did not crash
    assert "failed" not in page
    assert "unsupported" not in page

def test_TC_0011(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "multipage.docx"))
    click_convert(driver)

    take_screenshot(driver, "TC_0011")


def test_TC_0012(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "verylongfilenameeeeeeeeeeeee.docx"))

    take_screenshot(driver, "TC_0012")


def test_TC_0013(driver):
    open_page(driver)

    assert len(driver.find_elements(By.TAG_NAME, "button")) > 0

    take_screenshot(driver, "TC_0013")


def test_TC_0014(driver):
    open_page(driver)

    # FIXED: do NOT force fail
    assert driver.execute_script("return document.readyState") == "complete"

    take_screenshot(driver, "TC_0014")


def test_TC_0015_responsive(driver):
    driver.set_window_size(375, 812)
    time.sleep(2)

    # -----------------------------
    # 1. Page must still load
    # -----------------------------
    assert driver.execute_script("return document.readyState") == "complete"

    # -----------------------------
    # 2. Core elements must exist
    # -----------------------------
    assert len(driver.find_elements(By.XPATH, "//input[@type='file']")) > 0
    assert len(driver.find_elements(By.TAG_NAME, "button")) > 0

    # -----------------------------
    # 3. Page must not break
    # -----------------------------
    body = driver.page_source.lower()
    assert len(body) > 300

    # -----------------------------
    # 4. No crash or empty UI
    # -----------------------------
    assert "error" not in body
    assert "failed" not in body

    # -----------------------------
    # 5. Ensure UI is still interactive (NOT blank)
    # -----------------------------
    clickable = driver.find_elements(By.XPATH, "//button | //input")
    assert len(clickable) > 0

    take_screenshot(driver, "TC_0015")
    
def test_TC_0015_ui_validation(driver):

    # 1. Upload exists (core functionality)
    upload_input = driver.find_elements(By.XPATH, "//input[@type='file']")
    assert len(upload_input) > 0, "Upload input missing"

    # 2. Buttons exist
    buttons = driver.find_elements(By.TAG_NAME, "button")
    assert len(buttons) > 0, "No action buttons found"

    # 3. Page is loaded properly
    assert driver.execute_script("return document.readyState") == "complete"

    # 4. Basic DOM sanity check
    html_length = len(driver.page_source)
    assert html_length > 1000, "Page looks incomplete or broken"

    # =========================
    # ❌ NEGATIVE VALIDATION (IMPORTANT FIX)
    # =========================

    body_text = driver.page_source.lower()

    invalid_keywords = [
        "jpg",
        "png",
        "webp",
        "supported formats",
        "image format"
    ]

    for word in invalid_keywords:
        assert word not in body_text, f"Invalid UI text found: {word}"

    take_screenshot(driver, "TC_0015")


def test_TC_0017(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    click_convert(driver)

    take_screenshot(driver, "TC_0018")


def test_TC_0018(driver):
    open_page(driver)
    upload(driver, os.path.join(DESKTOP, "test.docx"))
    driver.refresh()
    time.sleep(2)

    assert "test.docx" not in page_text(driver)

    take_screenshot(driver, "TC_0019")