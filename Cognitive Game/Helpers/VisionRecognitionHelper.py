#  Helper that waits for NAO to recognize one of a set of images (tags).

import threading
#  Wraps the ALVisionRecognition service and filters events to specific tags.
class VisionRecognitionHelper:
    shouldDetectImage = False
    
#  Subscribe to the PictureDetected event and keep the timer/callback references.
    def __init__(self, session, memoryHelper):
        self.timer = None
        self.imageDetection = session.service("ALVisionRecognition")
        self.memoryHelper = memoryHelper
        self.subscriber = self.memoryHelper.memory.subscriber("PictureDetected")
        self.callback = None

    def __del__(self):
        self.StopDetecting()

#  Start looking for any of the given tags and call the callback when one is seen.
    def DetectImage(self, tags, callback, timeout, callbackTimeout):
        if self.imageDetection:
            self.tags = tags
            self.shouldDetectImage = True
            self.signalid = self.subscriber.signal.connect(self.onImageDetected)
            self.callback = callback
            self.imageDetection.subscribe(self.__class__.__name__, 1000, 0)
            self.timer = threading.Timer(timeout, callbackTimeout)
            self.timer.start()

#  Stop looking for images and cancel any timeout.
    def StopDetecting(self):
        self.shouldDetectImage = False
        if self.imageDetection:
            try:
                if self.timer:
                    self.timer.cancel()
                self.imageDetection.disconnect()
                if self.signalid:
                    self.subscriber.signal.disconnect()
            except:
                pass

#  Internal callback: triggered when NAO detects an image.
    def onImageDetected(self, result):
        if len(result) > 0 and self.shouldDetectImage:
            label = str(result[1][0][0][0]).strip()
            print("Image Detected, Label: " + label)
            if label in self.tags:
                self.shouldDetectImage = False
                if self.timer:
                    self.timer.cancel()
                print("Filtered Image Detected, Label: " + label)
                if self.callback:
                    self.callback(str(result[1][0][0][0]))