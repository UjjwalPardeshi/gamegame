from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/chromium-browser"
service = Service("/var/home/ujjain/chromedriver-linux64/chromedriver")

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://poki.com/en/g/temple-run-2")

# Wait for page to load and list iframes
time.sleep(5)
iframes = driver.find_elements(By.TAG_NAME, "iframe")
print(f"Found {len(iframes)} iframes")

canvas = None
for idx, iframe in enumerate(iframes):
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe)
        print(f"Switched to iframe {idx}")

        # Check for canvas inside this iframe
        canvas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        print("Canvas found!")
        break

    except Exception as e:
        print(f"No canvas in iframe {idx}: {e}")
        continue

if canvas:
    try:
        canvas.click()
        canvas.send_keys(Keys.SPACE)
        time.sleep(2)
        canvas.send_keys(Keys.ARROW_UP)
        time.sleep(1)
        canvas.send_keys(Keys.ARROW_LEFT)
        time.sleep(1)
        canvas.send_keys(Keys.ARROW_DOWN)
        time.sleep(10)
    except Exception as e:
        print("Interaction failed:", e)
else:
    print("❌ Could not find canvas in any iframe.")

driver.quit()
