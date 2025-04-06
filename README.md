# gamegame
# 🎮 Gesture-Controlled Browser Games

## 🛠 Features

- 🖐️ Real-time hand gesture recognition
- 🕹️ Choose between Temple Run 2 & Subway Surfers
- 📡 UDP socket-based gesture transmission
- 🧠 MediaPipe + OpenCV for detection
- 🎯 Control with intuitive hand signs

## 🎮 Gesture Mapping

| Gesture       | Emoji      | Action    |
|---------------|------------|-----------|
| Point Left    | 👈         | ← Left    |
| Point Right   | 👉         | → Right   |
| Peace (Up)    | ✌️         | ↑ Jump    |
| Thumb+Index   | 🤏         | ↓ Slide   |
| Open Palm     | 🖐️         | Space     |

## 🚀 Run the Project

```bash
# Terminal 1: Start gesture control
python gesture_control.py

# Terminal 2: Launch game and listener
python game_launcher.py
