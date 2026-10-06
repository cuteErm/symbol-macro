import cv2
import numpy as np
from PIL import ImageGrab

TEMPLATE_PATH = "target.png"
THRESHOLD = 0.85

try:
    template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("NOT_FOUND")
        raise SystemExit

    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    if max_val >= THRESHOLD:
        print("FOUND")
    else:
        print("NOT_FOUND")

except Exception:
    print("NOT_FOUND")
