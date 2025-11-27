#  Small helper to control the robot's LEDs (ears, feet, etc.).

#  Wraps the ALLeds service with simple on/off helper methods.
class LEDHelper:
    def __init__(self, session):
        self.led = session.service("ALLeds")

#  Fade the given LED group to the requested intensity for a certain duration.
    def TurnOnLed(self, LED, Intensity, Duration):
        if self.led:
            fadeOp = self.led.fade(LED, Intensity / 100.,
                                   Duration, _async=True)
            fadeOp.wait()
#  Quickly turn the given LED group off.
    def TurnOffLed(self, LED):
        if self.led:
            fadeOp = self.led.fade(LED, 0 / 100.,
                                   0, _async=True)
            fadeOp.wait()