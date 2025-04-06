import cv2
import mediapipe as mp

# Init
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(1)

# Define ROI boxes: (x1, y1, x2, y2)
LEFT_ROI = (1, 100, 200, 440)
RIGHT_ROI = (400, 100, 634, 456)

print("🧪 ROI Test Running... Show your index finger in the LEFT or RIGHT boxes.")

def point_inside_roi(point, roi):
    x, y = point
    x1, y1, x2, y2 = roi
    return x1 <= x <= x2 and y1 <= y <= y2

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        h, w, _ = frame.shape

        # Draw ROI rectangles and labels
        cv2.rectangle(frame, LEFT_ROI[:2], LEFT_ROI[2:], (0, 255, 0), 2)
        cv2.putText(frame, "LEFT", (LEFT_ROI[0], LEFT_ROI[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.rectangle(frame, RIGHT_ROI[:2], RIGHT_ROI[2:], (0, 0, 255), 2)
        cv2.putText(frame, "RIGHT", (RIGHT_ROI[0], RIGHT_ROI[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                # Index finger tip
                x = int(hand.landmark[8].x * w)
                y = int(hand.landmark[8].y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                if point_inside_roi((x, y), LEFT_ROI):
                    print("👈 LEFT detected")
                elif point_inside_roi((x, y), RIGHT_ROI):
                    print("👉 RIGHT detected")

        cv2.imshow("ROI Test - Left/Right Only", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

except KeyboardInterrupt:
    print("🛑 Stopped by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
