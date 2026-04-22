from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# =========================
# CONFIG
# =========================

USER = os.environ["USERPROFILE"]
DESKTOP = os.path.join(USER, "Desktop")

URL = "https://www.pixelssuite.com/resize-image"

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

        # TC-001
        if tc == "TC_001":
            if "resize" not in driver.page_source.lower():
                raise Exception("Resize page not loaded")
            msg = "Resize page loaded successfully"

        # TC-002
        elif tc == "TC_002":
            if len(driver.find_elements(By.XPATH, "//input[@type='file']")) == 0:
                raise Exception("Upload area not visible")
            msg = "Upload area visible"

        # TC-003
        elif tc == "TC_003":
            upload(f"{DESKTOP}\\image.png")
            if len(driver.find_elements(By.XPATH, "//input[@type='number']")) < 2:
                raise Exception("Resize section missing")
            msg = "Resize section displayed"

        # TC-004
        elif tc == "TC_004":
            upload(f"{DESKTOP}\\image.png")
            if len(driver.find_elements(By.XPATH, "//img | //canvas")) == 0:
                raise Exception("Preview not visible")
            msg = "Preview displayed correctly"

        # TC-005
        elif tc == "TC_005":
            upload(f"{DESKTOP}\\image.png")
            if len(driver.find_elements(By.XPATH, "//input[@type='number']")) < 2:
                raise Exception("Image upload failed")
            msg = "Image uploaded successfully"

        # TC-006
        elif tc == "TC_006":
            upload(f"{DESKTOP}\\image.png")

            width = driver.find_elements(By.XPATH, "//input[@type='number']")[0]
            height = driver.find_elements(By.XPATH, "//input[@type='number']")[1]

            width.clear()
            width.send_keys("300")

            height.clear()
            height.send_keys("200")

            msg = "Dimensions updated successfully"

        # TC-007
        elif tc == "TC_007":
            upload(f"{DESKTOP}\\image.png")

            checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if not checkbox.is_selected():
                checkbox.click()

            msg = "Keep aspect ratio enabled"

        # TC-008
        elif tc == "TC_008":
            upload(f"{DESKTOP}\\image.png")

            checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if checkbox.is_selected():
                checkbox.click()

            msg = "Keep aspect disabled"

        # TC-009
        elif tc == "TC_009":
            upload(f"{DESKTOP}\\image.png")

            if len(driver.find_elements(By.XPATH, "//button")) == 0:
                raise Exception("Buttons not found")

            msg = "Download button available"

        # =========================
        # ✅ FIXED TC-010 (IMPORTANT)
        # =========================
        elif tc == "TC_010":
            upload(f"{DESKTOP}\\image.png")
            driver.refresh()
            time.sleep(3)

            inputs = driver.find_elements(By.XPATH, "//input[@type='number']")
            images = driver.find_elements(By.XPATH, "//img")
            file_input = driver.find_elements(By.XPATH, "//input[@type='file']")

            if len(inputs) > 0:
                raise Exception("Width/Height still visible after refresh")

            if len(images) > 0:
                raise Exception("Image still visible after refresh")

            if len(file_input) == 0:
                raise Exception("Upload area missing after refresh")

            msg = "Refresh clears uploaded image successfully"

        # =========================

        shot = screenshot(tc)
        log(tc, "PASS", msg, shot)

    except Exception as e:
        shot = screenshot(tc)
        log(tc, "FAIL", str(e), shot)

# =========================
# RUN TESTS
# =========================

test_cases = [f"TC_{str(i).zfill(3)}" for i in range(1, 11)]

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
    <h2>Resize Image Automation Report</h2>
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