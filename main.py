import pyautogui
import socket
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Launch Chromium browser and open Temple Run 2
options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/chromium-browser"  # Path to Chromium
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

# Path to chromedriver
service = Service("/var/home/ujjain/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://poki.com/en/g/temple-run-2")

# Allow iframe to load
time.sleep(10)
print("🕹️ Move your mouse over the game window and click it to activate input focus.")

# Mapping gestures to keyboard keys
key_map = {
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "space": "space"  # Jump or similar action
}

# UDP server to receive gestures
def listen_for_gestures():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 5050))
    print("📡 Listening for gesture commands on port 5050...")

    while True:
        data, _ = sock.recvfrom(1024)
        direction = data.decode().strip()
        print(f"👋 Gesture received: {direction}")
        if direction in key_map:
            pyautogui.press(key_map[direction])
            print(f"⬅️ Pressed key: {key_map[direction]}")

# Start gesture listener thread
gesture_thread = threading.Thread(target=listen_for_gestures, daemon=True)
gesture_thread.start()

# Keep script alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("👋 Exiting...")
    driver.quit()
