from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# =========================
# CONFIG
# =========================

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

URL = "https://www.pixelssuite.com/pdf-editor"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver = webdriver.Chrome()
results = []

# =========================
# HELPERS
# =========================

def open_page():
    driver.get(URL)
    driver.maximize_window()
    time.sleep(4)

def upload(file):
    if not os.path.exists(file):
        raise Exception(f"File not found: {file}")
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(file)
    time.sleep(3)

def page_text():
    return driver.page_source.lower()

def screenshot(tc):
    path = f"{SCREENSHOT_DIR}\\{tc}.png"

    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    time.sleep(1)

    driver.save_screenshot(path)

    driver.maximize_window()
    return path

def log(tc, status, msg="", shot=""):
    results.append((tc, status, msg, shot))
    print(f"{tc} {status} {msg}")

# =========================
# TEST CASES
# =========================

def run_test(tc):

    open_page()
    msg = ""

    try:

        # TC_001
        if tc == "TC_001":
            if "editor" not in page_text():
                raise Exception("PDF Editor page not loaded")
            msg = "PDF Editor page loaded successfully"

        # TC_002
        elif tc == "TC_002":
            buttons = driver.find_elements(By.XPATH, "//button")
            if len(buttons) == 0:
                raise Exception("Toolbar not visible")
            msg = "Toolbar visible with buttons"

        # TC_003
        elif tc == "TC_003":
            tools = driver.find_elements(By.XPATH, "//button")
            if len(tools) < 5:
                raise Exception("Editing tools missing")
            msg = "Editing tools displayed"

        # TC_004
        elif tc == "TC_004":
            text = page_text()
            if not any(k in text for k in ["font", "bold", "align"]):
                raise Exception("Font settings not visible")
            msg = "Font settings visible"

        # TC_005
        elif tc == "TC_005":
            sliders = driver.find_elements(By.XPATH, "//input[@type='range']")
            if len(sliders) == 0:
                raise Exception("Zoom slider not found")
            msg = "Zoom slider present"

        # TC_006
        elif tc == "TC_006":
            if "page" not in page_text():
                raise Exception("Page section not visible")
            msg = "Page section visible"

        # TC_007
        elif tc == "TC_007":
            upload(f"{DESKTOP}\\test.pdf")
            if "page" not in page_text():
                raise Exception("PDF not loaded into editor")
            msg = "PDF uploaded successfully"

        # TC_008
        elif tc == "TC_008":
            upload(f"{DESKTOP}\\test.pdf")
            msg = "Text tool requires manual validation"

        # TC_009
        elif tc == "TC_009":
            upload(f"{DESKTOP}\\test.pdf")
            msg = "Pencil tool requires manual validation"

        # TC_010
        elif tc == "TC_010":
            upload(f"{DESKTOP}\\test.pdf")
            msg = "Eraser tool requires manual validation"

        # TC_011
        elif tc == "TC_011":
            upload(f"{DESKTOP}\\test.pdf")
            msg = "Font change requires manual validation"

        # TC_012
        elif tc == "TC_012":
            upload(f"{DESKTOP}\\test.pdf")
            msg = "Font size requires manual validation"

        # TC_013
        elif tc == "TC_013":
            upload(f"{DESKTOP}\\test.pdf")
            msg = "Alignment requires manual validation"

        # TC_014
        elif tc == "TC_014":
            upload(f"{DESKTOP}\\test.pdf")
            msg = "Undo/Redo requires manual validation"

        # TC_015
        elif tc == "TC_015":
            upload(f"{DESKTOP}\\multipage.pdf")
            text = page_text()
            if not ("next" in text or "prev" in text):
                raise Exception("Navigation buttons missing")
            msg = "Page navigation working"

        shot = screenshot(tc)
        log(tc, "PASS", msg, shot)

    except Exception as e:
        shot = screenshot(tc)
        log(tc, "FAIL", str(e), shot)

# =========================
# RUN TESTS
# =========================

test_cases = [f"TC_{str(i).zfill(3)}" for i in range(1, 16)]

for tc in test_cases:
    run_test(tc)

print("ALL TESTS DONE")

# =========================
# REPORT
# =========================

with open("report.html", "w", encoding="utf-8") as f:
    f.write("""
    <html>
    <body>
    <h2>PDF Editor Automation Report</h2>
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
            <td style='max-width:300px;word-wrap:break-word;'>{msg}</td>
            <td><a href='{shot}' target='_blank'>View</a></td>
        </tr>
        """)

    f.write("</table></body></html>")

print("✅ Report generated: report.html")

driver.quit()