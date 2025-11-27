#  Helper for text-to-speech (animated speech) output.

#  Wraps the ALAnimatedSpeech service so the robot can speak to the player.
class TTSHelper:
    def __init__(self, session):
        self.tts = session.service("ALAnimatedSpeech")

#  Say the given text out loud (and print it to the console for debugging).
    def Speak(self, text):
        if self.tts:
            print("Speak: " + text)
            self.tts.say(text)