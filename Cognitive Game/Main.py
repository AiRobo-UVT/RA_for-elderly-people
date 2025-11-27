# -*- coding: utf-8 -*-

#  Entry point for the NAO cognitive training game.
#  
#  This script:
#  - Creates the main Game controller.
#  - Starts face detection so the robot waits for a person.
#  - Keeps the program running so NAOqi callbacks can work.

from Game import Game

#  Create the main game controller object
main = Game()
#  Start looking for a human face and call main.FaceDetected when one is found
main.faceDetectionHelper.DetectFace(main.FaceDetected)
print("Started!")

#  Keep the script alive so the game can continue responding to events
while True:
    pass