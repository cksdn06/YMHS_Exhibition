import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import os
import glob
import pyautogui
import time
import qrcode
import cv2
#pip install opencv-python

image_folder = "C:\\Users\\User\\Desktop\\New"

# 카메라를 열고 이미지를 저장하는 함수
def capture_image():
    # 카메라 디바이스 열기 
    # (0은 기본 카메라, 아마 다른카메라로 바꿀듯)
    # ("장치 관리자"로 이동하고 "이미징 장치" 또는 "카메라"를 확인하여 카메라 정보를 얻을 수 있다네)
    # 0, 1, 2, 3이렇게 넣어봐야됨------ㅣ
    cap = cv2.VideoCapture(0)#<--이거-ㅣ
    
    # 추출할 영역의 좌표와 크기 설정
    # 추출할 영역의 좌표와 크기(카메라 화면 요소 구하기.py로 구함)
    x, y, width, height = 152, 10, 326, 430 
    # 원하는 비율로 확대할 크기====>>(n * (18/25), n(화면의 높이)(화면 몇px인지 구하기.py로 구함)) 
    desired_width, desired_height = 622, 864  

    # 저장할 이미지의 번호 초기화
    image_count = 0

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        if ret:
            # 추출할 영역 선택
            roi = frame[y:y+height, x:x+width]
            
            # 좌우 반전
            flipped_roi = cv2.flip(roi, 1) # 1은 좌우 반전을 나타냄
            
            # 선택한 영역을 원하는 비율로 확대
            resized_roi = cv2.resize(flipped_roi, (desired_width, desired_height))
            
            # 전체 화면에 표시
            cv2.imshow('Zoomed and Flipped Camera', resized_roi)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):  # 스페이스바를 눌렀을 때
                image_count += 1
                image_path = os.path.join(image_folder, f'image{image_count}.jpg')
                cv2.imwrite(image_path, resized_roi)
                print(f'이미지 {image_path} 저장됨.') 

    # 카메라 디바이스 해제 및 OpenCV 창 닫기
    cap.release()
    cv2.destroyAllWindows()

# 버튼을 눌렀을 때 실행되는 함수
def on_button_click():
    capture_image()

# 이미지 생성 함수
def create_image():
    #여기서는 이전에 만들어졌던 output.jpg를 삭제함(output폴더) 없으면 skip
    def delete_images(directory, image_extensions):
        if not os.path.exists(directory):
            print(f"The directory '{directory}' does not exist. Skipping image deletion.")
            return

        for extension in image_extensions:
            pattern = os.path.join(directory, f'*.{extension}')
            image_files = glob.glob(pattern)

            if not image_files:
                print(f"No {extension} files found in '{directory}'. Skipping image deletion.")
                continue

            for image_file in image_files:
                os.remove(image_file)
                print(f"Deleted: {image_file}")

    if __name__ == "__main__":
        target_directory = "C:\\Users\\User\\Desktop\\output"
        valid_image_extensions = ["jpg", "jpeg", "png", "gif"]

        delete_images(target_directory, valid_image_extensions)\
    
    # 원하는 인치 단위 크기 설정
    width_inch = 4
    height_inch = 6
    dpi = 300  # DPI (인치 당 도트 수)

    # 이미지 비율 설정
    image_width_inch = 1.8
    image_height_inch = 2.5

    # 픽셀로 크기 계산
    width_px = int(width_inch * dpi)
    height_px = int(height_inch * dpi)

    image_width_px = int(image_width_inch * dpi)
    image_height_px = int(image_height_inch * dpi)

    # 새 이미지를 생성합니다.
    new_image = Image.new('RGB', (width_px, height_px))

    # 이미지를 로드하고 크기 조정
    image1 = Image.open("C:\\Users\\User\\Desktop\\New\\image1.jpg")
    image2 = Image.open("C:\\Users\\User\\Desktop\\New\\image2.jpg")
    image3 = Image.open("C:\\Users\\User\\Desktop\\New\\image3.jpg")
    image4 = Image.open("C:\\Users\\User\\Desktop\\New\\image4.jpg")

    # 크기 조정 (ANTIALIAS)
    image1 = image1.resize((image_width_px, image_height_px), Image.ANTIALIAS)
    image2 = image2.resize((image_width_px, image_height_px), Image.ANTIALIAS)
    image3 = image3.resize((image_width_px, image_height_px), Image.ANTIALIAS)
    image4 = image4.resize((image_width_px, image_height_px), Image.ANTIALIAS)

    # 이미지를 삽입
    new_image.paste(image1, (int(dpi * 0.1), int(dpi * 0.1)))
    new_image.paste(image2, (image_width_px + int(dpi * 0.3), int(dpi * 0.1)))
    new_image.paste(image3, (int(dpi * 0.1), image_height_px + int(dpi * 0.3)))
    new_image.paste(image4, (image_width_px + int(dpi * 0.3), image_height_px + int(dpi * 0.3)))

    # 여백 및 텍스트 추가
    padding = int(dpi * 0.1)  # 0.1 인치 여백
    draw = ImageDraw.Draw(new_image)
    font_size = int(dpi * 0.3)  # 원하는 폰트 크기 설정
    font = ImageFont.load_default()  # 기본 폰트 사용
    font = ImageFont.truetype("arial.ttf", font_size)  # 폰트 크기 설정

    text = "Yeungnam 4cut"
    text_color = (255, 255, 255)  # 텍스트 색상 설정
    text_position = ((padding + image_width_px) * 0.5, height_px - padding - int(dpi * 0.5))  # 텍스트 위치 설정
    draw.text(text_position, text, fill=text_color, font=font)

    # 결과 이미지 저장(output폴더에 저장)
    output_folder = "C:\\Users\\User\\Desktop\\output"
    output_filename = "output.jpg"
    output_path = os.path.join(output_folder, output_filename)
    new_image.save(output_path, dpi=(dpi, dpi))
    
    #처음 4장을 지움(New폴더)
    def delete_images(directory, image_extensions):
        if not os.path.exists(directory):
            print(f"The directory '{directory}' does not exist. Skipping image deletion.")
            return

        for extension in image_extensions:
            pattern = os.path.join(directory, f'*.{extension}')
            image_files = glob.glob(pattern)

            if not image_files:
                print(f"No {extension} files found in '{directory}'. Skipping image deletion.")
                continue

            for image_file in image_files:
                os.remove(image_file)
                print(f"Deleted: {image_file}")

    if __name__ == "__main__":
        target_directory = "C:\\Users\\User\\Desktop\\New"
        valid_image_extensions = ["jpg", "jpeg", "png", "gif"]

        delete_images(target_directory, valid_image_extensions)

# 인쇄 실행 함수
def run_script():
    # output file의 경로 가져오기
    desktop_path = os.path.expanduser("C:\\Users\\User\\Desktop\\output")

    #이 밑의 실행문은 컴퓨터에 따라 다르게 함
    
    # output file에 있는 output.jpg 파일 열기
    file_path = os.path.join(desktop_path, 'output.jpg')
    os.startfile(file_path)
    time.sleep(2)  # 파일이 열릴 때까지 대기

    # Ctrl+P를 누르기
    pyautogui.hotkey('ctrl', 'p')

    time.sleep(5)  # 인쇄창이 열릴 때까지 대기
    
    #여기말이여 컴퓨터에 따라 다르게 함(Ai실 컴퓨터)
    for _ in range(12):
        pyautogui.press('tab')
    
    #진짜 인쇄하기
    #pyautogui.hotkey('enter')
    
    #인쇄 준비될때까지 기다리기
    time.sleep(3)
    # alt + f4를 누르기(이거는 인쇄창 없에기)
    pyautogui.hotkey('alt', 'f4')
    # alt + f4를 누르기(이거는 사진창 없에기)
    pyautogui.hotkey('alt', 'f4')

# QR 코드 (**폐지됨**)
def create_qr_code():
    # INSTAGRAM QR (@com_on_official)
    url = "https://www.instagram.com/com_on_official/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 이미지 저장하지 않고 바로 열기
    img.show()
# GUI 생성
root = tk.Tk()
root.title("이미지 생성 및 인쇄")

# 폰트 설정
custom_font = ("Helvetica", 30)

# 버튼 설정
cap_button = tk.Button(root, text="이미지 캡처", command=on_button_click, font=custom_font, width=20, height=3)
create_button = tk.Button(root, text="이미지 생성", command=create_image, font=custom_font, width=20, height=3)
run_button = tk.Button(root, text="인쇄", command=run_script, font=custom_font, width=20, height=3)
button = tk.Button(root, text="QR 코드 생성", command=create_qr_code, font=custom_font, width=20, height=3)
label = tk.Label(root, text="")

cap_button.pack()
create_button.pack()
run_button.pack()
button.pack()
label.pack()

root.mainloop()
