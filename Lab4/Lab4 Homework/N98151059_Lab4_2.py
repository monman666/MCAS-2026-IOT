
import RPi.GPIO as GPIO
import time

# 使用 BCM GPIO 編號
GPIO.setmode(GPIO.BCM)

# 超音波感測器腳位
TRIG_y = 23  # GPIO23，實體 Pin 16
ECHO_r = 24  # GPIO24，實體 Pin 18（需降壓）

# 設定輸入輸出模式
GPIO.setup(TRIG_y, GPIO.OUT)
GPIO.setup(ECHO_r, GPIO.IN)


def measure_distance():
    GPIO.output(TRIG_y, False)
    time.sleep(0.05)

    # 發送 10 微秒觸發訊號
    GPIO.output(TRIG_y, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_y, False)

    # 等待 ECHO 變成高電位
    timeout = time.monotonic() + 0.03

    while GPIO.input(ECHO_r) == 0:
        if time.monotonic() > timeout:
            raise TimeoutError("等待 ECHO 訊號超時")

    pulse_start = time.monotonic()

    # 等待 ECHO 變回低電位
    timeout = pulse_start + 0.03

    while GPIO.input(ECHO_r) == 1:
        if time.monotonic() > timeout:
            raise TimeoutError("ECHO 高電位超時")

    pulse_end = time.monotonic()

    # 計算距離（cm）
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    return round(distance, 2)


try:
    print("程式啟動，按 Ctrl+C 停止測試...")

    while True:
        try:
            distance = measure_distance()

            # LAB4-2 距離判斷
            if distance < 20:
                status = "注意！！！"
            else:
                status = "沒事"

            print(f"距離：{distance:.2f} cm | 狀態：{status}")

        except TimeoutError as err:
            print("測量失敗：", err)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n停止測量中...")

finally:
    GPIO.cleanup()
    print("GPIO 已清理，程式結束。")
