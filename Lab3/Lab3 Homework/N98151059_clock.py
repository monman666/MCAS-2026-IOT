#!/usr/bin/env python3

from time import sleep, localtime
from tm1637 import TM1637

# BCM GPIO 編號
CLK = 23
DIO = 24


class Clock:
    def __init__(self, display):
        self.display = display
        self.show_colon = False

    def run(self):
        while True:
            # 取得樹莓派目前時間
            current_time = localtime()

            # 切換冒號亮／滅
            self.show_colon = not self.show_colon

            # 顯示 HH:MM
            self.display.numbers(
                current_time.tm_hour,
                current_time.tm_min,
                self.show_colon
            )

            sleep(1)


if __name__ == "__main__":
    tm = TM1637(CLK, DIO)
    tm.brightness(7)

    clock = Clock(tm)

    try:
        clock.run()

    except KeyboardInterrupt:
        print("\n時鐘程式停止")

    finally:
        tm.show("    ")