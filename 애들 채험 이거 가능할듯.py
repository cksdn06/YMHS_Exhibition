import cv2
import numpy as np
import time
import pyautogui
import subprocess

# 메모장 실행
subprocess.Popen(["notepad.exe"])

# 카메라 캡처 초기화
cap = cv2.VideoCapture(0)

start_time = None
current_shape = None

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 프레임 크기 조정
    frame = cv2.resize(frame, (640, 480))

    # 손 모양 검출을 위한 프레임 복사본
    frame_copy = frame.copy()

    # 색상을 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 손 색상 범위 정의 (이 범위는 예시이며 실제로는 튜닝이 필요)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # 마스크 만들기
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # 마스크에서 손 모양 추출
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 가장 큰 손 모양 선택
        max_contour = max(contours, key=cv2.contourArea)

        # 손 모양을 프레임에 그리기
        cv2.drawContours(frame, [max_contour], 0, (0, 255, 0), 2)
        
        # 중간 좌표 계산
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(frame, "skin", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)


        # 현재 시간 측정
        if start_time is None:
            start_time = time.time()

        # 손 모양 주위에 근사적인 도형 검출
        epsilon = 0.04 * cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, epsilon, True)

        # 근사 도형이 원인지, 삼각형인지, 사각형인지 확인
        shape = ""
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            shape = "Rectangle"
        else:
            shape = "Circle"
        
        # 각 모양 이름을 화면에 표시
        cv2.putText(frame, shape, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 3초간 유지될 때 메모장에 입력
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3:
            if current_shape != shape:
                if shape == "Circle":
                    pyautogui.write("a")
                elif shape == "Triangle":
                    pyautogui.write("b")
                elif shape == "Rectangle":
                    pyautogui.write("c")
                current_shape = shape
                start_time = None

    # 화면에 프레임 표시
    cv2.imshow('Hand Detection', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 카메라 릴리스 및 창 닫기
cap.release()
cv2.destroyAllWindows()
