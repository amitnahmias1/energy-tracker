import cv2
import numpy as np

# Initialize video capture (0 for default camera)
cap = cv2.VideoCapture(0)

# Variables to store previous health bar position
prev_health_bar_y = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding or other image processing techniques
    _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours to find the health bar
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Adjust these conditions based on your health bar design
        if w > h * 7 and h > 22:
            # Extract the region of interest (ROI) corresponding to the health bar
            print(cv2.boundingRect(contour))

            health_bar_roi = frame[y:y + h, x:x + w]

            # Monitor changes in the health bar position
            if abs(y - prev_health_bar_y) > 5:
                pass #print("Health bar is changing!")

            # Update the previous health bar position
            prev_health_bar_y = y

            # Draw a rectangle around the health bar
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Health Bar Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()