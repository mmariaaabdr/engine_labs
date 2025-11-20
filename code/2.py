#!/usr/bin/env python3
from picamera2 import Picamera2
import numpy as np
import cv2
from time import sleep

def main():
    picam2 = Picamera2()

    # Максимальное разрешение сенсора
    sensor_size = picam2.sensor_resolution  # например (3280, 2464) для IMX219
    print("Sensor resolution:", sensor_size)

    # Конфигурация: основной поток + RAW
    config = picam2.create_still_configuration(
        main={"size": sensor_size},          # максимальное разрешение JPEG/array
        raw={"format": "SRGGB10"}           # RAW Bayer 10 бит
    )
    picam2.configure(config)

    picam2.start()

    # --- Фиксируем экспозицию и отключаем авто ---
    # Время экспозиции в микросекундах (подбери под свою яркость)
    FIXED_EXPOSURE_US = 20000  # 20 ms, если темно — увеличь
    FIXED_ANALOG_GAIN = 1.0

    # Отключаем авто-экспозицию и авто-баланс белого
    picam2.set_controls({
        "AeEnable": False,
        "ExposureTime": FIXED_EXPOSURE_US,
        "AnalogueGain": FIXED_ANALOG_GAIN,
        "AwbEnable": False
    })

    # Дать камере время применить настройки
    sleep(2.0)

    # ---------- Съёмка файлов ----------

    # JPEG
    picam2.capture_file("image.jpg", name="main")
    print("Saved JPEG: image.jpg")

    # RAW (DNG)
    picam2.capture_file("image.dng", name="raw")
    print("Saved RAW DNG: image.dng")

    # ---------- Получение numpy-массивов ----------

    # RGB-массив (после ISP, как JPEG, но без компрессии)
    rgb = picam2.capture_array("main")  # shape (H, W, 3), dtype=uint8

    # RAW Bayer-массив
    raw = picam2.capture_array("raw")   # shape (H_raw, W_raw), dtype=uint16

    # ---------- Сохранение numpy в .txt ----------
    # ВНИМАНИЕ: файлы могут быть ОЧЕНЬ большими при макс. разрешении.

    # Сохраним RGB как H*W строк по 3 значения (R,G,B)
    h, w, c = rgb.shape
    rgb_flat = rgb.reshape(-1, c)
    np.savetxt("image_rgb.txt", rgb_flat, fmt="%d")
    print("Saved RGB array as TXT: image_rgb.txt")

    # Сохраним RAW Bayer как 2D массив (строки = строки сенсора)
    np.savetxt("image_raw.txt", raw, fmt="%d")
    print("Saved RAW Bayer array as TXT: image_raw.txt")

    picam2.stop()

if __name__ == "__main__":
    main()
