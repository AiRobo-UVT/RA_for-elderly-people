# NAO Cognitive Training Game

This project is a simple memory / cognitive training game for the NAO robot.  
The robot:

- Waits until it detects a person’s face.
- Asks if the player wants to play.
- Shows a growing sequence of body parts (head, hands, feet) using movement and LEDs.
- The player must touch the corresponding body parts in the correct order.

If the player makes a mistake or takes too long, the game resets and the robot invites them to try again.

---

## Requirements

- A NAO robot with NAOqi running.
- SSH and SFTP access to the robot.
- The robot’s built-in Python (usually Python 2.7 on NAO).
- NAOqi services enabled for:
  - `ALAutonomousLife`
  - `ALBasicAwareness`
  - `ALSpeechRecognition`
  - `ALAnimatedSpeech`
  - `ALFaceDetection`
  - `ALVisionRecognition`
  - `ALLeds`
  - `ALMotion`
  - `ALAnimationPlayer`

The game uses English speech recognition:
- yes
- no

---

## Project Structure

```text
Game/
  Main.py                  # Entry point
  Game.py                  # Main game logic (rounds, sequences, state)
  Helpers/
    ASRHelper.py           # Speech recognition helper (yes/no)
    AutonomousLifeHelper.py
    FaceDetectionHelper.py
    LEDHelper.py
    MemoryHelper.py
    MovementHelper.py
    TouchHelper.py
    TTSHelper.py
    VisionRecognitionHelper.py
```

---

## 1. Uploading the Project to the Robot (SFTP)

1. Open your SFTP client (or use the `sftp` command).
2. Connect to the robot:

   ```bash
   sftp <robot-user>@<robot-ip>
   ```

   Example:

   ```bash
   sftp nao@192.168.1.50
   ```

3. On the robot, choose a folder to store the game, e.g. `/home/nao/Game`.

4. Upload the `Game` folder from your computer to the robot, for example:

   ```bash
   put -r Game
   ```

   After this, you should have something like:

   ```text
   /home/nao/Game/Main.py
   /home/nao/Game/Game.py
   /home/nao/Game/Helpers/...
   ```

---

## 2. Connecting via SSH

1. From your terminal, connect to the robot with SSH:

   ```bash
   ssh <robot-user>@<robot-ip>
   ```

   Example:

   ```bash
   ssh nao@192.168.1.50
   ```

2. Navigate to the game folder:

   ```bash
   cd ~/Game
   ```

---

## 3. Running the Game

From the `Game` folder on the robot, run:

```bash
python Main.py
```

You should see a message like:

```text
Started!
```

The robot will then:

- Wait for a face to be detected.
- Ask the player if they are ready to play.
- Start the memory game when the player answers `"yes"`.

---

## 4. Stopping the Game

To stop the game:

- Press `Ctrl + C` in the SSH terminal to stop the Python script, or
- Reboot the robot if needed.

---

## 5. Notes & Customization

- Language:  
  The spoken prompts are in English. Inline comments in the code include English translations for each phrase to make it easier to adapt.

- IP & Port:  
  The game uses `ip = "127.0.0.1"` and `port = 9559` in `Game.py`.  
  If your NAOqi instance runs on a different IP or port, update these values accordingly.

- Rounds:  
  The number of rounds (`totalrounds`) is defined in `Game.py`. You can adjust it to make the game shorter or longer for your users.

---
