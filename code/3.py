#!/usr/bin/env python3
import time
import numpy as np
import picamera
import picamera.array

# Имя базового кадра (без расширения)
BASE_NAME = "frame"

# Фиксированная экспозиция (подбери под свою яркость сцены)
FIXED_SHUTTER_US = 20000   # 20 000 мкс = 1/50 c
FIXED_ISO = 100            # можно 200 / 400 если темно

def main():
    with picamera.PiCamera() as camera:
        # Максимальное разрешение для твоего модуля (V1/V2/HQ)
        camera.resolution = camera.MAX_RESOLUTION
        # Низкий fps, чтобы не ограничивать длинную выдержку
        camera.framerate = 1

        # 1) даём автоэкспозиции немного поработать, чтобы сенсор "проснулся"
        camera.iso = FIXED_ISO
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'auto'
        time.sleep(2.0)

        # 2) фиксируем выдержку и выключаем автоэкспозицию
        camera.shutter_speed = FIXED_SHUTTER_US
        camera.exposure_mode = 'off'     # теперь экспозиция фиксирована

        # 3) отключаем авто-баланс белого
        camera.awb_mode = 'off'
        # единичные усиления по красному/синему (без перекоса цвета)
        camera.awb_gains = (1.0, 1.0)

        time.sleep(0.5)   # немного подождать, чтобы всё применилось

        # ---------- JPEG на диск ----------
        jpg_name = BASE_NAME + ".jpg"
        camera.capture(jpg_name, format='jpeg')
        print("JPEG сохранён в", jpg_name)

        # ---------- RGB-массив + txt ----------
        # Снова снимаем кадр, но сразу в массив (как RGB)
        with picamera.array.PiRGBArray(camera) as rgb_stream:
            camera.capture(rgb_stream, format='rgb')
            rgb = rgb_stream.array   # shape (H, W, 3), dtype=uint8

        h, w, c = rgb.shape
        rgb_flat = rgb.reshape(-1, c)    # каждая строка = [R G B]

        rgb_txt_name = BASE_NAME + "_rgb.txt"
        np.savetxt(rgb_txt_name, rgb_flat, fmt="%d")
        print("RGB массив сохранён в", rgb_txt_name)

        # ---------- RAW Bayer + txt ----------
        # Берём «сырые» данные сенсора (Bayer) через PiBayerArray
        with picamera.array.PiBayerArray(camera) as bayer_stream:
            # Важно: формат 'jpeg' + bayer=True — так прошивка добавляет сырые данные
            camera.capture(bayer_stream, format='jpeg', bayer=True)
            raw_bayer = bayer_stream.array   # numpy-массив raw Bayer

        # raw_bayer обычно 2D или 3D в зависимости от версии picamera.
        # Для простоты сохраняем как 2D:
        raw_bayer_2d = raw_bayer.reshape(raw_bayer.shape[0], -1)

        raw_txt_name = BASE_NAME + "_raw_bayer.txt"
        np.savetxt(raw_txt_name, raw_bayer_2d, fmt="%d")
        print("RAW Bayer массив сохранён в", raw_txt_name)

if __name__ == "__main__":
    main()
