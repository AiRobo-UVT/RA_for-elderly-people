#  Helper for enabling / configuring NAO's autonomous life behaviours.
#  
#  In this game we disable most idle behaviours so the robot does not move
#  unexpectedly while the player is concentrating on the task.

#  Wraps the ALAutonomousLife and ALBasicAwareness services.
class AutonomousLifeHelper:
    def __init__(self, session):
        self.autonomouslife = session.service("ALAutonomousLife")
        self.basicawareness = session.service("ALBasicAwareness")

#  Turn off various autonomous abilities (blinking, background movement, etc.).
    def EnableAutonomousLife(self):
        if self.autonomouslife:
            self.autonomouslife.setAutonomousAbilityEnabled("AutonomousBlinking", False)
            self.autonomouslife.setAutonomousAbilityEnabled("BackgroundMovement", False)
            self.autonomouslife.setAutonomousAbilityEnabled("BasicAwareness", False)
            self.autonomouslife.setAutonomousAbilityEnabled("ListeningMovement", False)
            self.autonomouslife.setAutonomousAbilityEnabled("SpeakingMovement", False)