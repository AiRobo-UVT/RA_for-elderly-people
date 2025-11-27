#  Helper around NAO's ALSpeechRecognition service.
#  
#  The game uses this to listen for very simple spoken answers
#  and call a callback when one of the expected words is recognized.

import threading


#  Controls speech recognition for short answers in the game.
class ASRHelper:
    shouldListen = False

#  Save references to NAOqi services and subscribe to the WordRecognized event.
    def __init__(self, session, memoryHelper):
        self.timer = None
        self.asr = session.service("ALSpeechRecognition")
        if self.asr:
            self.asr.setLanguage("English")
        self.memoryHelper = memoryHelper
        self.subscriber = self.memoryHelper.memory.subscriber("WordRecognized")
        self.callback = None

#  Start speech recognition with the given vocabulary and a timeout.
    def Listen(self, vocabulary, callback, timeout, callbackTimeout):
        if self.asr:
            self.shouldListen = True
            self.asr.pause(True)
            self.asr.setVocabulary(vocabulary, True)
            self.asr.subscribe(self.__class__.__name__)
            self.asr.pause(False)
            self.callback = callback
            self.subscriber.signal.connect(self.onWordRecognized)
            self.timer = threading.Timer(timeout, callbackTimeout)
            self.timer.start()

#  Stop listening for speech and cancel any running timeout.
    def StopListening(self):
        if self.asr:
            if self.timer:
                self.timer.cancel()
            self.asr.pause(True)
            self.shouldListen = False

#  Internal callback: called automatically when a word is recognized.
    def onWordRecognized(self, result):
        if self.callback and self.shouldListen:
            if self.timer:
                self.timer.cancel()
            print("Word recognized:" + result[0][6:][:6] + " Confidence: " + str(result[1]))
            self.callback(result[0][6:][:6], result[1])