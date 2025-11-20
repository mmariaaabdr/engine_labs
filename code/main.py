from picamera2 import Picamera2

picam2 = Picamera2()

config = picam2.create_still_configuration(
    main={"size": (1920, 1080)},
    raw={"format": "SRGGB10"}
)

picam2.configure(config)
picam2.start()

# raw
picam2.capture_file("frame.dng", name="raw")

# jpeg
picam2.capture_file("frame.jpg", name="main")

picam2.stop()
