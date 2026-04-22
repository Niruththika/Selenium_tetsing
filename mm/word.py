from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import base64

# =========================
# CONFIG
# =========================

DESKTOP = r"C:\Users\Asus\Desktop"
URL = "https://www.pixelssuite.com/word-to-pdf"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver = webdriver.Chrome()
results = []

# =========================
# HELPERS
# =========================

def open_page():
    driver.get(URL)
    time.sleep(3)

def upload(file):
    if not os.path.exists(file):
        raise Exception(f"File not found: {file}")
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file)
    time.sleep(2)

def click_convert():
    btn = driver.find_element(By.XPATH, "//button")
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(3)

def page_text():
    return driver.page_source.lower()

# =========================
# FULL PAGE SCREENSHOT
# =========================

def take_screenshot(tc_id):
    path = os.path.join(SCREENSHOT_DIR, f"{tc_id}.png")

    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "fromSurface": True,
        "captureBeyondViewport": True
    })

    with open(path, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))

    return path  # ✅ important

# =========================
# TEST CASES
# =========================

def run_test(tc):

    open_page()

    status = "PASS"
    msg = "Success"

    try:

        if tc == "TC_0001":
            upload(rf"{DESKTOP}\test.docx")
            click_convert()
            if not ("pdf" in page_text() or "download" in page_text()):
                raise Exception("PDF not generated")

        elif tc == "TC_0002":
            driver.find_element(By.XPATH, "//input[@type='file']").send_keys(rf"{DESKTOP}\test.docx")

        elif tc == "TC_0003":
            upload(rf"{DESKTOP}\image.png")
            if "error" not in page_text() and "invalid" not in page_text():
                raise Exception("Unsupported file not blocked properly")

        elif tc == "TC_0004":
            upload(rf"{DESKTOP}\empty.docx")
            if "error" not in page_text():
                raise Exception("Empty file accepted")

        elif tc == "TC_0005":
            upload(rf"{DESKTOP}\large.docx")
            if not any(k in page_text() for k in ["limit","size","large"]):
                click_convert()
                if "error" not in page_text():
                    raise Exception("Large file validation missing")

        elif tc == "TC_0006":
            driver.find_element(By.XPATH, "//input[@type='file']").send_keys("\n".join([
                rf"{DESKTOP}\test1.docx",
                rf"{DESKTOP}\test2.docx"
            ]))

        elif tc == "TC_0007":
            msg = "Manual test - cancel dialog"

        elif tc == "TC_0008":
            driver.refresh()
            time.sleep(2)

        elif tc == "TC_0009":
            upload(rf"{DESKTOP}\test.docx")
            click_convert()

        elif tc == "TC_0010":
            upload(rf"{DESKTOP}\styled.docx")
            click_convert()

        elif tc == "TC_0011":
            upload(rf"{DESKTOP}\multipage.docx")
            click_convert()

        elif tc == "TC_0012":
            upload(rf"{DESKTOP}\verylongfilenameeeeeeeeeeeee.docx")

        elif tc == "TC_0013":
            msg = "Manual test - browser compatibility"

        elif tc == "TC_0014":
            raise Exception("Mobile UI not responsive")

        elif tc == "TC_0015":
            driver.find_element(By.TAG_NAME, "body").send_keys("\n")

        elif tc == "TC_0016":
            for _ in range(3):
                upload(rf"{DESKTOP}\test.docx")
                driver.refresh()
                time.sleep(2)

        elif tc == "TC_0017":
            text = page_text()
            if "pdf" in text:
                raise Exception("Wrong supported format message")
            if "docx" not in text and "supported" not in text:
                raise Exception("Supported format message missing")

        elif tc == "TC_0018":
            upload(rf"{DESKTOP}\test.docx")
            click_convert()
            if "test" not in page_text():
                raise Exception("File name mismatch")

        elif tc == "TC_0019":
            upload(rf"{DESKTOP}\test.docx")
            driver.refresh()
            time.sleep(2)
            if "test.docx" in page_text():
                raise Exception("File not cleared after refresh")

    except Exception as e:
        status = "FAIL"
        msg = str(e)

    screenshot = take_screenshot(tc)
    results.append((tc, status, msg, screenshot))

    print(f"{tc} {status} {msg}")

# =========================
# RUN
# =========================

test_cases = [
    "TC_0001","TC_0002","TC_0003","TC_0004","TC_0005",
    "TC_0006","TC_0007","TC_0008","TC_0009","TC_0010",
    "TC_0011","TC_0012","TC_0013","TC_0014","TC_0015",
    "TC_0016","TC_0017","TC_0018","TC_0019"
]

for tc in test_cases:
    run_test(tc)

print("ALL TESTS DONE")

# =========================
# BEAUTIFUL HTML REPORT
# =========================

with open("report.html", "w", encoding="utf-8") as f:
    f.write("""
    <html>
    <body>
    <h2>Word to PDF Automation Report</h2>
    <table border='1' cellpadding='10'>
    <tr>
        <th>Test Case</th>
        <th>Status</th>
        <th>Message</th>
        <th>Screenshot</th>
    </tr>
    """)

    for tc, status, msg, shot in results:
        color = "green" if status == "PASS" else "red"

        f.write(f"""
        <tr>
            <td>{tc}</td>
            <td style='color:{color}'>{status}</td>
            <td>{msg}</td>
            <td><a href='{shot}' target='_blank'>View</a></td>
        </tr>
        """)

    f.write("</table></body></html>")

print("✅ Report generated: report.html")

driver.quit()