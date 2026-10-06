import os
import sys
import time
import random
import cv2
import numpy as np
import pyautogui
import keyboard

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

TARGET_IMAGE = resource_path("target.png")
THRESHOLD = 0.85
CHECK_INTERVAL = 0.05
MIN_DELAY = 0.5
MAX_DELAY = 1.5

if not os.path.exists(TARGET_IMAGE):
    raise FileNotFoundError(f"Datei nicht gefunden: {TARGET_IMAGE}")

template = cv2.imread(TARGET_IMAGE, cv2.IMREAD_GRAYSCALE)
if template is None:
    raise ValueError(f"Bild konnte nicht geladen werden: {TARGET_IMAGE}")

# Zustand
is_running = False

def toggle_macro():
    global is_running
    is_running = not is_running
    status = "GESTARTET" if is_running else "GESTOPPT"
    print(f"Macro {status} (F10 zum Umschalten)")

def stop_program():
    print("Programm beendet (ESC).")
    sys.exit(0)

keyboard.add_hotkey("f10", toggle_macro)
keyboard.add_hotkey("esc", stop_program)

print("Macro bereit. F10 zum Starten/Stoppen, ESC zum Beenden.")

while True:
    try:
        if is_running:
            screenshot = pyautogui.screenshot()
            img = np.array(screenshot)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            if max_val >= THRESHOLD:
                delay = random.uniform(MIN_DELAY, MAX_DELAY)
                time.sleep(delay)
                pyautogui.keyDown("f")
                time.sleep(0.05)
                pyautogui.keyUp("f")
                print(f"F gedrückt nach {delay:.2f}s")

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        break
