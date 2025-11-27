#  Helper that waits until a human face is detected in front of the robot.

#  Subscribes to the ALFaceDetection service and reports when a face appears.
class FaceDetectionHelper:
    shouldDetectFace = False

#  Subscribe to the FaceDetected event and store the callback reference.
    def __init__(self, session, memoryHelper):
        self.faceDetection = session.service("ALFaceDetection")
        self.memoryHelper = memoryHelper
        self.subscriber = self.memoryHelper.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.onFaceRecognized)
        self.callback = None

    def __del__(self):
        self.StopDetecting()

#  Start looking for a face and remember which callback to call when one is found.
    def DetectFace(self, callback):
        if self.faceDetection:
            self.callback = callback
            self.faceDetection.subscribe(self.__class__.__name__, 1000, 0)
            self.faceDetection.setTrackingEnabled(True)
            self.faceDetection.setRecognitionEnabled(False)
            self.shouldDetectFace = True

#  Stop face detection and ignore further events.
    def StopDetecting(self):
        if self.faceDetection:
            self.shouldDetectFace = False
            self.faceDetection.setTrackingEnabled(False)
            self.faceDetection.setRecognitionEnabled(False)

#  Internal NAOqi callback when a face is detected.
    def onFaceRecognized(self, result):
        if self.callback and self.shouldDetectFace:
            print("Face Detected!")
            self.callback()