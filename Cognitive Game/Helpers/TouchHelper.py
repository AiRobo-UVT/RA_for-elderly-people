#  Helper that listens for touch events on the robot's head, hands and feet.

import threading
#  Registers callbacks for the different touch sensors used in the game.
class TouchHelper:
    isDetecting = False
    lock = threading.Lock()

#  Subscribe to NAOqi touch and bumper events.
    def __init__(self, memoryHelper):
        self.LeftHandTouchedCallback = None
        self.RightHandTouchedCallback = None
        self.LeftFootTouchedCallback = None
        self.RightFootTouchedCallback = None
        self.HeadTouchedCallback = None
        self.touch = memoryHelper.memory.subscriber("TouchChanged")
        self.rightBumperPressed = memoryHelper.memory.subscriber("RightBumperPressed")
        self.leftBumperPressed = memoryHelper.memory.subscriber("LeftBumperPressed")
        self.rightbumperid = self.rightBumperPressed.signal.connect(self.RightBumperPressed)
        self.leftbumperid = self.leftBumperPressed.signal.connect(self.LeftBumperPressed)
        self.touchid = self.touch.signal.connect(self.onTouched)
        self.isDetecting = False

    def __del__(self):
        self.StopDetecting()

#  Register which function to call when the head is touched.
    def HeadTouched(self, callback):
        self.HeadTouchedCallback = callback

#  Register which function to call when the left hand is touched.
    def LeftHandTouched(self, callback):
        self.LeftHandTouchedCallback = callback

#  Register which function to call when the right hand is touched.
    def RightHandTouched(self, callback):
        self.RightHandTouchedCallback = callback

#  Register which function to call when the left foot is touched.
    def LeftFootTouched(self, callback):
        self.LeftFootTouchedCallback = callback

#  Register which function to call when the right foot is touched.
    def RightFootTouched(self, callback):
        self.RightFootTouchedCallback = callback

#  Right bumper is used as a quick way to stop all touch detection.
    def RightBumperPressed(self, value):
        with self.lock:
            if self.rightBumperPressed and self.isDetecting and value == 1:
                print("Right Foot Bumper Pressed")
                self.RightFootTouchedCallback()

#  Left bumper is also used to stop touch detection.
    def LeftBumperPressed(self, value):
        with self.lock:
            if self.leftBumperPressed and self.isDetecting and value == 1:
                print("Left Foot Bumper Pressed")
                self.LeftFootTouchedCallback()
  
    def onTouched(self, value):
        with self.lock:
            if self.touch and self.isDetecting and value[0][1]:
                if value[0][0] == "LArm" and self.LeftHandTouchedCallback:
                    print("Touched: " + str(value[0][0]))
                    self.LeftHandTouchedCallback()
                elif value[0][0] == "RArm" and self.RightHandTouchedCallback:
                    print("Touched: " + str(value[0][0]))
                    self.RightHandTouchedCallback()
                elif value[0][0] == "Head" and self.HeadTouchedCallback:
                    print("Touched: " + str(value[0][0]))
                    self.HeadTouchedCallback()
#  Enable touch detection so touches will trigger callbacks.
    def StartDetecting(self):
        self.isDetecting = True

#  Disable touch detection so touches are ignored.
    def StopDetecting(self):
        self.isDetecting = False