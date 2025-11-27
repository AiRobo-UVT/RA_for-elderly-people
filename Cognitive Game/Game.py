# -*- coding: utf-8 -*-

#  Core logic for a simple memory / cognitive training game on a NAO robot.
#  
#  The robot:
#  - Waits until it detects the face of a player.
#  - Asks if the player wants to play.
#  - Shows a growing sequence of body parts (head, hands, feet) using movement and LEDs.
#  - The player must touch the corresponding body part in the same order.
#  
#  If the player makes a mistake or takes too long to respond, the game resets
#  and the robot invites the player to try again.

from Helpers import AutonomousLifeHelper, MemoryHelper, ASRHelper, TTSHelper, FaceDetectionHelper, \
    VisionRecognitionHelper, LEDHelper, MovementHelper, TouchHelper
from naoqi import qi
import time
import random
import threading

#  High-level controller for the memory game running on the NAO robot.
class Game:
    ip = "127.0.0.1"  #  IP address of the NAO robot (change if the robot is on another host)
    port = 9559  #  Default NAOqi port
    currentround = 0  #  Counter for the current round of the memory game
    totalrounds = 20  #  Maximum number of rounds the player can go through
    expectedSensor = -1;  #  Which body part the player is expected to touch next
    lost = False;  #  Flag that becomes True when the player makes a mistake or times out
    sensorTouched = False;  #  Tracks whether a touch was detected during the current step
    timer = None

#  Connect to NAOqi, create all helper objects and prepare the robot.
    def __init__(self):
        self.asr = None
        self.ttsStop = None
        self.tts = None

        connection_url = "tcp://" + self.ip + ":" + str(self.port)  #  Build the connection URL for the NAOqi framework
        self.app = qi.Application([self.__class__.__name__, "--qi-url=" + connection_url])  #  Start a NAOqi application so we can access robot services
        self.app.start()

        self.autonomouslifeHelper = AutonomousLifeHelper.AutonomousLifeHelper(self.app.session)  #  Helper that turns autonomous idle behaviours on/off
        self.memoryHelper = MemoryHelper.MemoryHelper(self.app.session)  #  Helper to store small pieces of game state in ALMemory
        self.asrHelper = ASRHelper.ASRHelper(self.app.session, self.memoryHelper)  #  Helper that wraps speech recognition (yes / no answers)
        self.ttsHelper = TTSHelper.TTSHelper(self.app.session)  #  Helper for text-to-speech (robot talking to the player)
        self.ledHelper = LEDHelper.LEDHelper(self.app.session)  #  Helper to control the LEDs (used for feet / ears cues)
        self.faceDetectionHelper = FaceDetectionHelper.FaceDetectionHelper(self.app.session, self.memoryHelper)  #  Helper that detects when a human face is in front of the robot
        self.movementHelper = MovementHelper.MovementHelper(self.app.session)  #  Helper that moves the robot's head, arms and posture
        self.touchHelper = TouchHelper.TouchHelper(self.memoryHelper)  #  Helper that listens for touches on the head, hands and feet
        self.visionRecognitionHelper = VisionRecognitionHelper.VisionRecognitionHelper(self.app.session, self.memoryHelper)  #  Helper that recognizes printed images used in the game
        self.timer = threading.Timer(30, self.Reset)  #  Timer used to limit how long the player has to touch the correct sensor
        self.touchHelper.RightHandTouched(self.RightHandTouched)  #  When the right hand is touched, call Game.RightHandTouched
        self.touchHelper.LeftHandTouched(self.LeftHandTouched)  #  When the left hand is touched, call Game.LeftHandTouched
        self.touchHelper.HeadTouched(self.HeadTouched)  #  When the head is touched, call Game.HeadTouched
        self.touchHelper.LeftFootTouched(self.LeftFootTouched)  #  When the left foot is touched, call Game.LeftFootTouched
        self.touchHelper.RightFootTouched(self.RightFootTouched)  #  When the right foot is touched, call Game.RightFootTouched
        self.Initialize()  #  Put the robot in a neutral posture and enable autonomous life

    def __del__(self):
        self.Reset()

#  Called when the player touches the robot's head sensor.
    def HeadTouched(self):
        self.touchHelper.StopDetecting()
        self.sensorTouched = True;
        if self.expectedSensor != 0:
            self.lost = True;
        self.timer.cancel()
            
#  Called when the player touches the right hand sensor.
    def RightHandTouched(self):
        self.touchHelper.StopDetecting()
        self.sensorTouched = True;
        if self.expectedSensor != 2:
            self.lost = True;
        self.timer.cancel()
            
#  Called when the player touches the left hand sensor.
    def LeftHandTouched(self):
        self.touchHelper.StopDetecting()
        self.sensorTouched = True;
        if self.expectedSensor != 1:
            self.lost = True;
        self.timer.cancel()

#  Called when the player touches the left foot sensor.
    def LeftFootTouched(self):
        self.touchHelper.StopDetecting()
        self.sensorTouched = True;
        if self.expectedSensor != 3:
            self.lost = True;
        self.timer.cancel()

#  Called when the player touches the right foot sensor.
    def RightFootTouched(self):
        self.touchHelper.StopDetecting()
        self.sensorTouched = True;
        if self.expectedSensor != 4:
            self.lost = True;
        self.timer.cancel()

#  Handle the player's spoken answer (yes / no) and run the game rounds.
    def ASRCallback_Main(self, result, confidence):
#  Player answered "yes" with enough confidence: start the game rounds.
        if result == "yes" and confidence > 0.495:
            self.asrHelper.StopListening()
            self.currentround = 0
            self.lost = False
            self.cancelled = False
            history = []  #  This list keeps the full sequence of body parts the player must remember
            while self.currentround < self.totalrounds:  #  Keep adding a new body part at the end of the sequence until all rounds are complete
                print("Current Round: " + str(self.currentround) )
                currentPart = random.randint(0,4)  #  Pick a random body part: 0=head, 1=left hand, 2=right hand, 3=left foot, 4=right foot
                history.append(currentPart)
                for i in history:  #  First, SHOW the full sequence to the player using movement / LEDs
                    if i == 0:
                        self.movementHelper.MoveHead()
                        self.ttsHelper.Speak("Head")
                    elif i == 1:
                        self.movementHelper.RaiseLeftArm()
                        self.ttsHelper.Speak("Left Arm.")
                    elif i == 2: 
                        self.movementHelper.RaiseRightArm()
                        self.ttsHelper.Speak("Right Arm.")
                    elif i == 3:
                        self.ledHelper.TurnOnLed("LeftFootLeds", 100, 0.01)
                        self.ttsHelper.Speak("Left Foot.")
                        self.ledHelper.TurnOffLed("LeftFootLeds")
                    elif i == 4:
                        self.ledHelper.TurnOnLed("RightFootLeds", 100, 0.01)
                        self.ttsHelper.Speak("Right Foot.")
                        self.ledHelper.TurnOffLed("RightFootLeds")
                for idx, i in enumerate(history):  #  Then, ASK the player to REPEAT the sequence by touching the correct sensors
                    self.touchHelper.StartDetecting()  #  Start listening for any touch on the robot
                    self.timer = threading.Timer(30, self.Reset)  #  Timer used to limit how long the player has to touch the correct sensor
                    self.expectedSensor = i  #  Remember which body part we expect (used by the touch callbacks)
                    self.sensorTouched = False;
                    self.ledHelper.TurnOnLed("EarLeds", 100, 1)  #  Turn on the ear LEDs so the player knows the robot is waiting for a touch
                    self.timer.start()
                    while self.timer.is_alive():  #  Wait here until the player touches something or the time runs out
                        time.sleep(0.1)
                    if self.timer:
                        self.timer.cancel()
                    time.sleep(0.1)
                    self.ledHelper.TurnOffLed("EarLeds")
                    if self.lost:  #  If the player failed this step, stop asking for more touches in this round
                        break
                    if idx is not len(history) and not self.lost:  #  If there are more steps in the sequence, give positive feedback before continuing
                        self.ttsHelper.Speak("Yes.") 
                self.currentround += 1  #  Move on to the next round (sequence gets one step longer)
                if self.totalrounds == self.currentround:  #  Player completed all rounds successfully
                    self.ttsHelper.Speak("Well done, you have an amazing memory!")
                    self.Reset()
                    break;
                elif self.lost:  #  The player made a mistake somewhere in the sequence
                    if not self.cancelled:
                         self.ttsHelper.Speak("I think I managed to confuse you!")
                    self.Reset()
                    break;
                self.ttsHelper.Speak("Correct!")
#  Player answered no: remind them to train their memory and reset the game.
        elif result == "no" and confidence > 0.5:
            self.asrHelper.StopListening()
            self.ttsHelper.Speak("You must exercise your memory just like your body.")
            self.Reset()

#  Called once a human face is detected in front of the robot.
    def FaceDetected(self):
        self.faceDetectionHelper.StopDetecting()
        self.ttsHelper.Speak("Hello. It is time for your daily cognitive training. Are you ready?")
        self.asrHelper.Listen(["yes", "no"], self.ASRCallback_Main, 30, self.Reset)

#  Stop any ongoing activity and return the robot to the initial waiting state.
    def Reset(self):
        print("Resetting...")
        self.lost = True
        self.cancelled = True
        self.asrHelper.StopListening()
        self.movementHelper.StopAnimation()
        self.memoryHelper.ClearMemory()
        self.faceDetectionHelper.StopDetecting()
        self.visionRecognitionHelper.StopDetecting()
        self.ledHelper.TurnOffLed("EarLeds")
        time.sleep(15)
        self.faceDetectionHelper.DetectFace(self.FaceDetected)

#  Prepare the robot: clear memory, relax posture and then wake it up for the game.
    def Initialize(self):
        self.memoryHelper.ClearMemory()
        self.movementHelper.Rest()  #  Put the robot into a resting posture
        time.sleep(5)
        self.autonomouslifeHelper.EnableAutonomousLife()  #  Turn off some autonomous behaviours so they do not interfere with the game
        time.sleep(5)
        self.movementHelper.WakeUp()  #  Gently wake the robot up so it is ready to interact
        time.sleep(5)