#  Helper for moving the robot's body parts used in the game.

#  Provides small movements (head, arms, posture) for the memory game cues.
class MovementHelper:
#  Store references to motion and animation services.
    def __init__(self, session):
        self.LastAnimation = None
        self.movement = session.service("ALAnimationPlayer")
        self.motion = session.service("ALMotion")

    def __del__(self):
        if self.LastAnimation:
            self.LastAnimation.cancel()

#  Play a named animation file using ALAnimationPlayer.
    def Animation(self, animation):
        if self.movement:
            self.LastAnimation = self.movement.run(animation, _async=True)

#  Stop the last running animation, if any.
    def StopAnimation(self):
        if self.LastAnimation:
            self.LastAnimation.cancel()

#  Raise and lower the robot's left arm.
    def RaiseLeftArm(self):
        if self.motion:
            self.motion.angleInterpolation("LShoulderPitch", [1.5, 0.75, 1.5], [0.02, 0.6, 1.2], True)

#  Raise and lower the robot's right arm.
    def RaiseRightArm(self):
        if self.motion:
            self.motion.angleInterpolation("RShoulderPitch", [1.5, 0.75, 1.5], [0.02, 0.6, 1.2], True)

#  Move the head left and right to clearly indicate the "head" body part.
    def MoveHead(self):
        if self.motion:
            self.motion.angleInterpolation("HeadYaw", [0, -0.33, 0.33, 0], [0.01, 0.5, 1.01, 1.5], True)

#  Gently wake the robot from rest so it can move.
    def WakeUp(self):
        if not self.motion.robotIsWakeUp():
            self.motion.wakeUp()

#  Put the robot in a relaxed posture.
    def Rest(self):
        if self.motion.robotIsWakeUp():
            self.motion.rest()