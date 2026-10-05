

import RPi.GPIO as GPIO
import time

PIN2 = 11       # BOARD 實體腳位 11（GPIO17）
FREQ = 523      # 蜂鳴器頻率
SHORT = 0.2     # 短音
LONG = 0.6      # 長音
GAP = 0.2       # 每一聲之間的間隔

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN2, GPIO.OUT)

voice = GPIO.PWM(PIN2, FREQ)
voice.start(0)  # 先以 0% duty 啟動，保持安靜


def beep(duration):
    """讓蜂鳴器發聲指定時間。"""
    voice.ChangeDutyCycle(50)
    time.sleep(duration)
    voice.ChangeDutyCycle(0)
    time.sleep(GAP)


def play_sos():
    # S：三短音
    for _ in range(3):
        beep(SHORT)

    time.sleep(0.4)  # 字母之間稍微停頓

    # O：三長音
    for _ in range(3):
        beep(LONG)

    time.sleep(0.4)

    # S：三短音
    for _ in range(3):
        beep(SHORT)


try:
    while True:
        play_sos()
        time.sleep(2)  # 完整 SOS 播放完畢後停兩秒

except KeyboardInterrupt:
    print("\n程式停止")

finally:
    voice.stop()
    GPIO.cleanup()