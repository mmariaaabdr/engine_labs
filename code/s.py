import picamera, time

with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    time.sleep(2)
    camera.capture('test.jpg')