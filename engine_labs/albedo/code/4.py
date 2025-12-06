#!/usr/bin/env python3
import time
import picamera

# Настройки
FILENAME = "white.jpg"

# Фиксированная экспозиция (подбирай под яркость сцены)
FIXED_SHUTTER_US = 30000    # 20 ms
FIXED_ISO = 200             # можно 200/400 если темно

with picamera.PiCamera() as camera:
    # Максимальное возможное разрешение камеры автоматически
    camera.resolution = (1640,1213)
    camera.framerate = 1   # нужен низкий fps для длинной выдержки

    # Шаг 1: даём авто-настройкам включиться, чтобы сенсор прогрелся
    camera.iso = FIXED_ISO
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    time.sleep(2.0)

    # Шаг 2: фиксируем экспозицию (АВТО-БОЛЬШЕ НЕ РАБОТАЕТ)
    camera.shutter_speed = FIXED_SHUTTER_US
    camera.exposure_mode = 'off'      # выключаем автоэкспозицию

    # Шаг 3: отключаем авто-баланс белого
    camera.awb_mode = 'off'
    camera.awb_gains = (1.0, 1.0)

    # Небольшая задержка для применения настроек
    time.sleep(0.5)

    # Съёмка кадра в JPEG
    camera.capture(FILENAME, format='jpeg')
    print("Фото сохранено в:", FILENAME)
