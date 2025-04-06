import cv2
import mediapipe as mp
import time
import socket

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(1)

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 5050)

# ROI positions for left and right (x1, y1, x2, y2)
LEFT_ROI = (1, 100, 200, 440)
RIGHT_ROI = (400, 100, 634, 456)

# State tracking
direction = ""
cooldown = 0.5           
last_action_time = time.time()

print("👁️ Watching your hands... ROI for Left/Right, Gestures for Up/Down/Space")
 
#    ROI helper
def point_inside_roi(point, roi):
    x, y = point
    x1, y1, x2, y2 = roi
    return x1 <= x <= x2 and y1 <= y <= y2
 
# Finger logic
def finger_states(landmarks):
    fingers = []
    fingers.append(landmarks[4].x < landmarks[3].x)                          # Thumb
    fingers.append(landmarks[8].y < landmarks[6].y)                          # Index
    fingers.append(landmarks[12].y < landmarks[10].y)                        # Middle
    fingers.append(landmarks[16].y < landmarks[14].y)                        # Ring
    fingers.append(landmarks[20].y < landmarks[18].y)                        # Pinky
    return fingers  # [Thumb, Index, Middle, Ring, Pinky]

# Gesture-based UP/DOWN/SPACE
def gesture_classify(landmarks):
    fingers = finger_states(landmarks)

    # ✌️ Up: index + middle
    if fingers == [False, True, True, False, False]:
        return "up"

    # 🤏 Down: thumb and index close, others folded
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    dist = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    if dist < 0.05 and fingers[2:] == [False, False, False]:
        return "down"

    # 🖐️ Space: all fingers extended
    if fingers == [True, True, True, True, True]:
        return "space"

    return None

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        h, w, _ = frame.shape

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                index_x = int(hand.landmark[8].x * w)
                index_y = int(hand.landmark[8].y * h)
                new_direction = None

                # ROI-based: Left/Right
                if point_inside_roi((index_x, index_y), LEFT_ROI):
                    new_direction = "left"
                elif point_inside_roi((index_x, index_y), RIGHT_ROI):
                    new_direction = "right"
                else:
                    # Gesture-based: Up/Down/Space
                    new_direction = gesture_classify(hand.landmark)

                # Send command if changed or cooldown passed
                if new_direction and (new_direction != direction or time.time() - last_action_time > cooldown):
                    direction = new_direction
                    sock.sendto(direction.encode(), server_address)
                    print(f"📤 Sent: {direction}")
                    last_action_time = time.time()

except KeyboardInterrupt:
    print("🛑 Shutting down hand tracking.")

finally:
    cap.release()
    cv2.destroyAllWindows()
