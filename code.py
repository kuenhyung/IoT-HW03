import os
import subprocess
import time
from gpiozero import Button, MotionSensor
from datetime import datetime

# 1. 하드웨어 객체 초기화
button = Button(2, pull_up=True)
pir = MotionSensor(4)

print("[INFO] PIR 센서 안정화 대기 중... (10초)")
time.sleep(10)
print("[INFO] 시작!")
print("[INFO] PIR 준비 완료!")

# 2. 저장 경로 설정
SAVE_PATH = "/home/pi/Desktop/captures"
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

def stop_system():
    print("\n[INFO] 시스템을 안전하게 종료합니다.")
    exit()

def take_photo():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{SAVE_PATH}/burglar_{now}.jpg"
    print(f"[EVENT] 움직임 감지! 사진 촬영 시작: {file_name}")
    try:
        subprocess.run([
            "rpicam-still",
            "-o", file_name,
            "-t", "1000",
            "--nopreview"
        ], check=True)
        print(" -> [SUCCESS] 사진이 성공직으로 저장되었습니다.")
    except Exception as e:
        print(f" -> [ERROR] 촬영 중 오류 발생: {e}")

# 4. 이벤트 핸들러
button.when_pressed = stop_system

print("==========================================")
print("  침입자 감지 시스템이 가동되었습니다.   ")
print("  (종료하려면 버튼을 누르거나 Ctrl+C)     ")
print("==========================================")

while True:
    pir.wait_for_motion()
    take_photo()
    pir.wait_for_no_motion()
