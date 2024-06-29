from machine import Pin, I2C
import time

# I2Cの設定
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# BH1750のI2Cアドレス（スキャン結果に基づいて修正）
BH1750_ADDR = 0x23

# BH1750の操作モード
POWER_ON = 0x01
RESET = 0x07
CONT_H_RES_MODE = 0x10

def read_bh1750():
    i2c.writeto(BH1750_ADDR, bytes([POWER_ON]))  # センサーの電源をオン
    time.sleep(0.05)
    i2c.writeto(BH1750_ADDR, bytes([RESET]))  # センサーをリセット
    time.sleep(0.05)
    i2c.writeto(BH1750_ADDR, bytes([CONT_H_RES_MODE]))  # 測定モードの設定
    time.sleep(0.18)  # 測定時間の待機
    data = i2c.readfrom(BH1750_ADDR, 2)
    lux = int.from_bytes(data, 'big') / 1.2
    return lux

while True:
    try:
        lux = read_bh1750()
        print("Brightness: {:.2f} lx".format(lux))
    except OSError as e:
        print("Error reading BH1750:", e)
    time.sleep(1)

