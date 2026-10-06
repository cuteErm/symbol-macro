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

# Wenn du nur den weißen Teil des Symbols erkennen willst, aktiviere diese Option.
# Dann brauchst du KEIN target.png mehr; die Macro sucht einfach nach weißen Pixels.
USE_WHITE_DETECTION = True
WHITE_MIN_BRIGHTNESS = 200
WHITE_RATIO_MIN = 0.0005  # ca. 0.05 % der Bildfläche

# Optional: nur innerhalb eines bestimmten Bildschirmbereichs suchen.
# Beispiel: REGION = (100, 100, 700, 500)
# None = ganzer Bildschirm
REGION = None

# Wenn target.png existiert, wird Template-Matching bevorzugt.
# Wenn nicht, wird automatisch Weiß-Erkennung benutzt.
if os.path.exists(TARGET_IMAGE):
    template = cv2.imread(TARGET_IMAGE, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Bild konnte nicht geladen werden: {TARGET_IMAGE}")
else:
    template = None

# Zustand
is_running = False


def detect_white_symbol(img_bgr):
    # Nur weiße/helle Pixel berücksichtigen
    # Schwarz/Hintergrund wird ignoriert
    lower = np.array([WHITE_MIN_BRIGHTNESS, WHITE_MIN_BRIGHTNESS, WHITE_MIN_BRIGHTNESS], dtype=np.uint8)
    upper = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(img_bgr, lower, upper)

    # Räumlich etwas glätten, damit kleine Rauschen ignoriert werden
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    white_pixels = cv2.countNonZero(mask)
    total_pixels = img_bgr.shape[0] * img_bgr.shape[1]
    white_ratio = white_pixels / total_pixels
    return white_ratio >= WHITE_RATIO_MIN


def detect_template(img_gray):
    if template is None:
        return False
    result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val >= THRESHOLD


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
print("Hinweis: Weiß-Erkennung ist aktiv, wenn kein target.png vorhanden ist.")

while True:
    try:
        if is_running:
            screenshot = pyautogui.screenshot(region=REGION) if REGION else pyautogui.screenshot()
            img = np.array(screenshot)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            found = False

            if template is not None:
                found = detect_template(img_gray)
            elif USE_WHITE_DETECTION:
                found = detect_white_symbol(img)

            if found:
                delay = random.uniform(MIN_DELAY, MAX_DELAY)
                time.sleep(delay)
                pyautogui.keyDown("f")
                time.sleep(0.05)
                pyautogui.keyUp("f")
                print(f"F gedrückt nach {delay:.2f}s")

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        break
