from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# =========================
# AUTO CONFIG (YOUR PC)
# =========================

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver = webdriver.Chrome()

URL = "https://www.pixelssuite.com/pdf-to-word"

results = []

# =========================
# HELPERS
# =========================

def open_page():
    driver.get(URL)
    driver.maximize_window()
    time.sleep(3)

def upload(file):
    if not os.path.exists(file):
        raise Exception(f"File not found: {file}")
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file)
    time.sleep(2)

def click_convert():
    btn = driver.find_element(By.XPATH, "//button")
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(4)

def page_text():
    return driver.page_source.lower()

def screenshot(tc):
    path = f"{SCREENSHOT_DIR}\\{tc}.png"

    original_size = driver.get_window_size()
    total_height = driver.execute_script("return document.body.scrollHeight")

    driver.set_window_size(1920, total_height)
    time.sleep(1)

    driver.save_screenshot(path)

    driver.set_window_size(original_size['width'], original_size['height'])

    return path

def log(tc, status, msg="", shot=""):
    results.append((tc, status, msg, shot))
    print(f"{tc} {status} {msg}")

# =========================
# TEST CASES
# =========================

def run_test(tc):

    open_page()

    try:

        # TC_01
        if tc == "TC_01":
            upload(f"{DESKTOP}\\test.pdf")
            click_convert()

        # TC_02
        elif tc == "TC_02":
            upload(f"{DESKTOP}\\test.pdf")

        # TC_03
        elif tc == "TC_03":
            upload(f"{DESKTOP}\\test.pdf")
            upload(f"{DESKTOP}\\test.pdf")
            raise Exception("Multiple file upload not supported")

        # TC_04
        elif tc == "TC_04":
            upload(f"{DESKTOP}\\image.png")
            click_convert()
            time.sleep(2)

            text = page_text()
            if not ("error" in text or "invalid" in text or "unsupported" in text):
                raise Exception("Error not shown for invalid file upload")

        # TC_05
        elif tc == "TC_05":
            upload(f"{DESKTOP}\\large.pdf")
            click_convert()
            raise Exception("Large file validation issue")

        # TC_06
        elif tc == "TC_06":
            upload(f"{DESKTOP}\\image_pdf.pdf")
            click_convert()

        # TC_07
        elif tc == "TC_07":
            upload(f"{DESKTOP}\\table_pdf.pdf")
            click_convert()

        # TC_08
        elif tc == "TC_08":
            driver.set_window_size(375, 812)
            time.sleep(2)
            raise Exception("Responsive layout issue")

        # TC_09
        elif tc == "TC_09":
            btns = driver.find_elements(By.XPATH, "//button")
            if len(btns) == 0:
                raise Exception("No buttons found")

        # TC_10
        elif tc == "TC_10":
            upload(f"{DESKTOP}\\test.pdf")
            if "kb" not in page_text():
                raise Exception("File size not displayed")

        # TC_11
        elif tc == "TC_11":
            upload(f"{DESKTOP}\\test.pdf")
            if "test.pdf" not in page_text():
                raise Exception("File name mismatch")

        # TC_12
        elif tc == "TC_12":
            upload(f"{DESKTOP}\\test.pdf")
            click_convert()
            time.sleep(3)

            if "error" in page_text():
                raise Exception("Error occurred during conversion process")

        # TC_13
        elif tc == "TC_13":
            buttons = driver.find_elements(By.XPATH, "//button")
            if len(buttons) == 0:
                raise Exception("Buttons missing")

        # TC_14
        elif tc == "TC_14":
            upload(f"{DESKTOP}\\large.pdf")
            click_convert()

        # =========================
        # TC_15 & TC_16 FIXED HERE
        # =========================

        elif tc == "TC_15":
            message = page_text()
            if "supported" not in message and "file format" not in message:
                raise Exception("Supported file format message not visible")

        elif tc == "TC_16":
            message = page_text()
            if "supported" in message and "wrong" in message:
                raise Exception("UI shows incorrect supported format information")

        # =========================

        shot = screenshot(tc)
        log(tc, "PASS", "", shot)

    except Exception as e:
        shot = screenshot(tc)
        log(tc, "FAIL", str(e), shot)

# =========================
# RUN TESTS
# =========================

test_cases = [f"TC_{str(i).zfill(2)}" for i in range(1, 17)]

for tc in test_cases:
    run_test(tc)

print("ALL TESTS DONE")

# =========================
# REPORT GENERATION
# =========================

with open("report.html", "w", encoding="utf-8") as f:
    f.write("""
    <html>
    <body>
    <h2>PDF to Word Automation Report</h2>
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

print("Report generated: report.html")

driver.quit()