import cv2
import numpy as np

def detect_blinking_red_light(source=0):
    # Initialize video capture (0 for webcam, or provide a video file path)
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    # Read the first frame to initialize 'previous_frame'
    ret, prev_frame = cap.read()
    if not ret:
        return

    # Convert previous frame to grayscale for simpler subtraction logic
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        blurred_frame = cv2.GaussianBlur(frame,(5,5),0)
        gray = cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2HSV) 


        # 2. FRAME SUBTRACTION (Detects Motion/Blinking)
        # Calculate absolute difference between current and previous frame
        frame_diff = cv2.absdiff(prev_gray, gray)
        
        # Threshold the difference to get binary motion mask
        # Pixels with a change > 30 are considered "moving/blinking"
        _, motion_mask = cv2.threshold(frame_diff, 1, 255, cv2.THRESH_BINARY)

        # 3. COLOR FILTERING (Detects Red)
        # Red wraps around 180 in HSV, so we need two ranges
        lower_red1 = np.array([0, 100, 100]) 
        upper_red1 = np.array([10, 200, 255])
        lower_red2 = np.array([160, 100, 100]) # 170 ko 160 kiya thoda range badhane ke liye
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 + mask2

        # 4. COMBINE & CLEAN
        final_mask = cv2.bitwise_and(motion_mask, red_mask)
        subtraction_view = cv2.bitwise_and(frame,frame,mask = final_mask)
        # Eroding se chota noise khatam ho jata hai
        kernel = np.ones((3,3), np.uint8)
        final_mask = cv2.erode(final_mask, kernel, iterations=1)
        final_mask = cv2.dilate(final_mask, kernel, iterations=2)

        # 5. SMART DETECTION
        contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if 50 < area < 5000: # Limit range: na bohot chota, na bohot bada
                x, y, w, h = cv2.boundingRect(contour)
                
                # Draw a green rectangle around the blinking red light
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Blinking Red Light", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Show the result
        cv2.imshow("Detection Feed", frame)
        cv2.imshow("only blinking light",subtraction_view)
        # cv2.imshow("orignal feed",frame)
        
        # Optional: Show the mask to understand what the computer 'sees'
        # cv2.imshow("Debug Mask", final_mask)

        # Update previous frame
        prev_gray = gray.copy()

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the function
if __name__ == "__main__":
    detect_blinking_red_light()