import os
import sys
import time
import random
import cv2
import numpy as np
import pyautogui
import keyboard
import ctypes

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
KEY_HOLD_TIME = 0.1

# Windows API für Tastendrücke
SendInput = ctypes.windll.user32.SendInput

# F-Taste = VK_F (0x46)
VK_F = 0x46

# Flags
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ki", KEYBDINPUT)]

def press_key(vk):
    """Taste drücken"""
    x = INPUT(type=1)
    x.ki = KEYBDINPUT(wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYDOWN, time=0, dwExtraInfo=None)
    SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def release_key(vk):
    """Taste loslassen"""
    x = INPUT(type=1)
    x.ki = KEYBDINPUT(wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=None)
    SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def press_and_hold_key(vk, hold_time):
    """Taste drücken, halten, loslassen"""
    press_key(vk)
    time.sleep(hold_time)
    release_key(vk)

print(f"Suche nach: {TARGET_IMAGE}")
print(f"Datei existiert: {os.path.exists(TARGET_IMAGE)}")

if not os.path.exists(TARGET_IMAGE):
    print("FEHLER: target.png nicht gefunden!")
    print(f"Aktueller Ordner: {os.getcwd()}")
    print(f"Dateien im Ordner: {os.listdir('.')}")
    raise FileNotFoundError(f"Datei nicht gefunden: {TARGET_IMAGE}")

template = cv2.imread(TARGET_IMAGE, cv2.IMREAD_GRAYSCALE)
if template is None:
    print("FEHLER: Bild konnte nicht geladen werden!")
    raise ValueError(f"Bild konnte nicht geladen werden: {TARGET_IMAGE}")

print(f"Bild erfolgreich geladen! Größe: {template.shape}")

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
print("Nutzt Windows API (ctypes) für robuste Tastendrücke in Spielen.")

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
                
                # Nutze Windows API mit korrekten Flags
                press_and_hold_key(VK_F, KEY_HOLD_TIME)
                print(f"F gedrückt nach {delay:.2f}s (Windows API)")

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        break
