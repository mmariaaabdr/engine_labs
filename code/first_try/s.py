import picamera, time

with picamera.PiCamera() as camera:
    camera.resolution = (1640, 1213)
    time.sleep(2)
    camera.capture('red.jpg')