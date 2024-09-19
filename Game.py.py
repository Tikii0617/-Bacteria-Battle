import cv2
import time
import math

WINDOW_NAME = "Microscope Camera - Euglena Detection"

import cv2
import numpy as np

def preprocess(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection to detect faded edges
    edges = cv2.Canny(blurred, 50, 150)

    # Apply morphological closing to fill gaps in edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Additional dilation to merge close contours
    dilated = cv2.dilate(closed, kernel, iterations=1)

    # Apply binary threshold to the closed image
    _, thresh = cv2.threshold(dilated, 50, 255, cv2.THRESH_BINARY)


    return thresh


# Function to detect Euglena-like shapes using contours
def detect_euglena(thresh_frame, original_frame):
    # Find contours in the thresholded frame
    contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize counts for each half
    left_count = 0
    right_count = 0

    # Get the width of the frame to determine the middle
    frame_width = original_frame.shape[1]
    middle = frame_width // 2
    
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)

        # Calculate area and filter based on size (tuned to capture Euglena)
        area = cv2.contourArea(contour)
        
        if 100 < area < 8000:  # Adjust this range to capture smaller objects like Euglena
            # Draw bounding boxes around detected Euglena-like shapes
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(original_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Optionally draw contours
            cv2.drawContours(original_frame, [approx], -1, (0, 255, 0), 2)
            
            # Determine which half the bacteria is in
            # Check if the bounding box is predominantly in the left half or the right half
            if x + w <= middle:
                left_count += 1
            elif x >= middle:
                right_count += 1
            else:
                right_count += 1

    return left_count, right_count


def track_bacteria(prev_gray, current_gray, original_frame, feature_params, lk_params):
    p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)
    if p0 is not None:
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, current_gray, p0, None, **lk_params)
        if p1 is not None:
            good_new = p1[st == 1]
            good_old = p0[st == 1]
            for (new, old) in (zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                a, b, c, d = int(a), int(b), int(c), int(d)
                cv2.line(original_frame, (a, b), (c, d), (0, 255, 0), 2)
                cv2.circle(original_frame, (a, b), 5, (0, 0, 255), -1)

def display_message(frame, message, duration):
    cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow(WINDOW_NAME, frame)
    cv2.waitKey(duration)

def clear_score_area(frame):
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 60), (0, 0, 0), -1)

def display_final_result(frame, player1_count, player2_count):
    frame[:] = (0, 0, 0)
    cv2.putText(frame, "Time's up!", (frame.shape[1] // 2 - 100, frame.shape[0] // 2 - 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    cv2.putText(frame, f"Final Scores:", (frame.shape[1] // 2 - 100, frame.shape[0] // 2 + 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Player 1: {player1_count}", (frame.shape[1] // 2 - 100, frame.shape[0] // 2 + 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Player 2: {player2_count}", (frame.shape[1] // 2 - 100, frame.shape[0] // 2 + 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.imshow(WINDOW_NAME, frame)
    cv2.waitKey(5000)

cap = cv2.VideoCapture(0)  # Use DirectShow instead of MSMF
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()


feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
prev_gray = None

messages = ["Start game", "3...", "2...", "1...", "Catch Euglena !!"]
for message in messages:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    display_message(frame, message, 1000)

game_duration = 60
start_time = time.time()

player1_count = 0
player2_count = 0

# Initialize counters and smoothing parameters
smoothing_window_size = 10
left_counts = []
right_counts = []

while True:
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    processed_frame = preprocess(frame)

    # Detect and mark Euglena-like shapes
    left_count, right_count = detect_euglena(processed_frame, frame)

    # Append counts to lists and maintain window size
    left_counts.append(left_count)
    right_counts.append(right_count)
    
    if len(left_counts) > smoothing_window_size:
        left_counts.pop(0)
    if len(right_counts) > smoothing_window_size:
        right_counts.pop(0)
    
    # Calculate smoothed counts
    smoothed_left_count = int(np.mean(left_counts))
    smoothed_right_count = int(np.mean(right_counts))

    current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is not None:
        track_bacteria(prev_gray, current_gray, frame, feature_params, lk_params)

    prev_gray = current_gray.copy()

    frame_height, frame_width = frame.shape[:2]
    cv2.line(frame, (frame_width // 2, 0), (frame_width // 2, frame_height), (255, 255, 255), 2)

    clear_score_area(frame)

    cv2.putText(frame, f'Player 1: {smoothed_left_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 2))
    cv2.putText(frame, f'Player 2: {smoothed_right_count}', (frame_width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 2))

    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if time.time() - start_time > game_duration:
        break

display_final_result(frame, left_count, right_count)

cap.release()
cv2.destroyAllWindows()
