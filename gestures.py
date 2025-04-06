import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(1)
prev_x, prev_y = 0, 0
direction = ""
threshold = 0.08  # Movement threshold for stability

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Use index fingertip (landmark 8) instead of wrist
            x = hand_landmarks.landmark[8].x
            y = hand_landmarks.landmark[8].y

            dx = x - prev_x
            dy = y - prev_y

            # Determine dominant direction
            if abs(dx) > threshold or abs(dy) > threshold:
                if abs(dx) > abs(dy):
                    direction = "Right" if dx > 0 else "Left"
                else:
                    direction = "Down" if dy > 0 else "Up"

                prev_x, prev_y = x, y  # Update only when there's valid movement

    cv2.putText(frame, f"Direction: {direction}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Direction Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
