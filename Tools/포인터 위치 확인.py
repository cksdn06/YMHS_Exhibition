import pyautogui

# 현재 마우스 커서 위치 확인
x, y = pyautogui.position()
print(f"현재 마우스 위치: x={x}, y={y}")