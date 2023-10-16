import win32api

screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

print(f"화면 너비: {screen_width}, 화면 높이: {screen_height}")
