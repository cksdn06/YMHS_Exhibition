import cv2

# 전역 변수
selecting_area = False
initial_x, initial_y, final_x, final_y = -1, -1, -1, -1

def mouse_callback(event, x, y, flags, param):
    global selecting_area, initial_x, initial_y, final_x, final_y

    if event == cv2.EVENT_LBUTTONDOWN:
        initial_x, initial_y = x, y
        selecting_area = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if selecting_area:
            final_x, final_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        selecting_area = False
        final_x, final_y = x, y

# 카메라 디바이스 열기 (0은 기본 카메라를 나타냅니다. 다른 카메라를 사용하려면 카메라 번호를 변경하세요.)
cap = cv2.VideoCapture(0)

cv2.namedWindow('Select Area')
cv2.setMouseCallback('Select Area', mouse_callback)

while True:
    ret, frame = cap.read()

    if ret:
        if not selecting_area:
            # 화면 전체를 표시
            cv2.imshow('Select Area', frame)
        else:
            # 선택한 영역 표시
            selected_frame = frame.copy()
            cv2.rectangle(selected_frame, (initial_x, initial_y), (final_x, final_y), (0, 255, 0), 2)
            cv2.imshow('Select Area', selected_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# 선택한 영역 좌표와 크기 출력
if initial_x != -1 and initial_y != -1 and final_x != -1 and final_y != -1:
    x, y = min(initial_x, final_x), min(initial_y, final_y)
    width, height = abs(final_x - initial_x), abs(final_y - initial_y)
    print(f"Selected Area - x: {x}, y: {y}, width: {width}, height: {height}")

# 카메라 디바이스 해제 및 OpenCV 창 닫기
cap.release()
cv2.destroyAllWindows()
