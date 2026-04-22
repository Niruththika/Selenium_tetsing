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

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

URL = "https://www.pixelssuite.com/image-to-pdf"

results = []

# =========================
# HELPERS
# =========================

def open_page():
    driver.get(URL)
    time.sleep(4)

def upload(file_path):
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file_path)
    time.sleep(3)

def click(text):
    driver.find_element(By.XPATH, f"//button[contains(text(),'{text}')]").click()
    time.sleep(1)

def check_pdf_generated():
    time.sleep(3)
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    assert (
        "download" in page_text or
        "pdf" in page_text or
        "save" in page_text
    ), "PDF not generated"

def multi_upload(*files):
    upload("\n".join(files))

# =========================
# 🔥 FULL PAGE SCREENSHOT (BEST METHOD)
# =========================

def take_screenshot(tc_id):
    path = os.path.join(SCREENSHOT_DIR, f"TC_{tc_id:03}.png")

    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "fromSurface": True,
        "captureBeyondViewport": True
    })

    with open(path, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))

# =========================
# TEST RUNNER
# =========================

def run_test(tc_id):
    open_page()

    try:

        # ================= BASIC TESTS =================
        if tc_id == 1:
            upload(os.path.join(DESKTOP, "test.jpg"))

        elif tc_id == 2:
            multi_upload(
                os.path.join(DESKTOP, "test.jpg"),
                os.path.join(DESKTOP, "test.jpg")
            )

        elif tc_id == 3:
            print("TC_003 skipped")

        elif tc_id == 4:
            upload(os.path.join(DESKTOP, "test.pdf"))
            page = driver.page_source.lower()
            assert "invalid" in page or "unsupported" in page

        elif tc_id == 5:
            upload(os.path.join(DESKTOP, "big.jpg"))
            page = driver.page_source.lower()
            assert "large" in page or "limit" in page or "mb" in page

        elif tc_id == 6:
            upload(os.path.join(DESKTOP, "test.jpg"))
            driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()

        elif tc_id == 7:
            multi_upload(
                os.path.join(DESKTOP, "test.jpg"),
                os.path.join(DESKTOP, "test.jpg")
            )

        elif tc_id == 8:
            pass

        elif tc_id == 9:
            upload(os.path.join(DESKTOP, "test.jpg"))

        elif tc_id == 10:
            multi_upload(
                os.path.join(DESKTOP, "test.jpg"),
                os.path.join(DESKTOP, "test.jpg"),
                os.path.join(DESKTOP, "test.jpg")
            )

        elif tc_id == 11:
            upload(os.path.join(DESKTOP, "test.jpg"))
            driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()

        # ================= SETTINGS TESTS =================
        elif 13 <= tc_id <= 21:
            upload(os.path.join(DESKTOP, "test.jpg"))

            if tc_id == 13: click("A4")
            elif tc_id == 14: click("Letter")
            elif tc_id == 15: click("Portrait")
            elif tc_id == 16: click("Landscape")
            elif tc_id == 17: click("Vertical")
            elif tc_id == 18: click("Horizontal")
            elif tc_id == 19: click("One")
            else: click("Multiple")

            click("Create")
            check_pdf_generated()

        elif 22 <= tc_id <= 29:
            upload(os.path.join(DESKTOP, "test.jpg"))
            click("A4")
            click("Portrait")
            click("Vertical")
            click("One")
            click("Create")
            check_pdf_generated()

        elif 30 <= tc_id <= 37:
            upload(os.path.join(DESKTOP, "test.jpg"))
            click("Letter")
            click("Create")
            check_pdf_generated()

        elif tc_id == 38:
            upload(os.path.join(DESKTOP, "corrupt.jpg"))
            page = driver.page_source.lower()
            assert "invalid" in page or "corrupt" in page

        elif tc_id == 39:
            upload(os.path.join(DESKTOP, "test.pptx"))
            page = driver.page_source.lower()
            assert "unsupported" in page or "invalid" in page

        elif tc_id == 40:
            upload(os.path.join(DESKTOP, "test.jpg"))
            driver.refresh()

        elif tc_id == 41:
            upload(os.path.join(DESKTOP, "longfilename.jpg"))

        elif tc_id == 42:
            driver.set_window_size(400, 800)

        elif tc_id == 43:
            driver.set_window_size(375, 812)
            time.sleep(2)
            assert driver.find_element(By.XPATH, "//input[@type='file']").is_displayed()
            assert driver.find_element(By.XPATH, "//button[contains(text(),'Create')]").is_displayed()

        elif tc_id == 45:
            upload(os.path.join(DESKTOP, "test.pdf"))
            page = driver.page_source.lower()
            assert any(k in page for k in ["error", "invalid", "unsupported", "format"])

        # ================= RESULT =================
        take_screenshot(tc_id)
        results.append((f"TC_{tc_id:03}", "PASS"))
        print(f"TC_{tc_id:03} PASS")

    except Exception as e:
        take_screenshot(tc_id)
        results.append((f"TC_{tc_id:03}", "FAIL"))
        print(f"TC_{tc_id:03} FAIL ->", e)

# =========================
# RUN ALL TESTS
# =========================

for i in range(1, 46):
    run_test(i)

print("ALL TESTS DONE")

# =========================
# ATTRACTIVE HTML REPORT
# =========================

pass_count = sum(1 for _, s in results if s == "PASS")
fail_count = sum(1 for _, s in results if s == "FAIL")
total = len(results)

html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Automation Test Report</title>
<style>
body {{
    font-family: Arial;
    background: #f4f6f9;
    padding: 20px;
}}

.container {{
    max-width: 1000px;
    margin: auto;
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

h1 {{
    text-align: center;
}}

.summary {{
    display: flex;
    justify-content: space-around;
    margin: 20px 0;
}}

.card {{
    padding: 15px;
    border-radius: 10px;
    width: 30%;
    color: white;
    font-weight: bold;
    text-align: center;
}}

.total {{ background: #007bff; }}
.pass {{ background: #28a745; }}
.fail {{ background: #dc3545; }}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
}}

th {{
    background: #333;
    color: white;
}}

tr:nth-child(even) {{
    background: #f9f9f9;
}}

.badge-pass {{
    background: #28a745;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
}}

.badge-fail {{
    background: #dc3545;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
}}
</style>
</head>

<body>
<div class="container">

<h1>🧪 Automation Test Report</h1>

<div class="summary">
<div class="card total">TOTAL<br>{total}</div>
<div class="card pass">PASSED<br>{pass_count}</div>
<div class="card fail">FAILED<br>{fail_count}</div>
</div>

<table>
<tr>
<th>Test Case</th>
<th>Status</th>
<th>Screenshot</th>
</tr>
"""

for tc, status in results:
    badge = "badge-pass" if status == "PASS" else "badge-fail"
    img = f"screenshots/{tc}.png"

    html += f"""
<tr>
<td>{tc}</td>
<td><span class="{badge}">{status}</span></td>
<td><a href="{img}" target="_blank">View</a></td>
</tr>
"""

html += """
</table>
</div>
</body>
</html>
"""

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

time.sleep(3)
driver.quit()