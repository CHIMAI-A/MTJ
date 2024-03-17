import serial
import cv2
import numpy as np
from tkinter import Tk, Label, Button

# Initialize serial communication with Arduino
ser = serial.Serial('COM3', 9600)  # Update COM port accordingly


# Function to capture camera frame and send it to Arduino
def capture_frame():
    ser.write(b'snapshot\n')

# Function to read classification results from Arduino
def read_results():
    result = ser.readline().decode().strip()
    # Update UI with classification result
    label.config(text=result)

# Function to display live stream from Arduino
def display_stream():
    while True:
        # Capture frame from Arduino
        frame = ser.readline()
        # Debug: Print frame size and content
        print("Frame size:", len(frame))
        # Convert frame to OpenCV format
        frame_np = np.frombuffer(frame, dtype=np.uint8)
        frame_cv = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
        # Debug: Print frame dimensions
        if frame_cv is not None:
            print("Frame dimensions:", frame_cv.shape)
            # Display frame in UI
            cv2.imshow('Live Stream', frame_cv)
            # Check for key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Invalid frame received")
    cv2.destroyAllWindows()

# Create Tkinter window
root = Tk()
root.title('Live Stream Classification')

# Create label to display classification result
label = Label(root, text='Classification Result')
label.pack()

# Create button to capture frame
capture_button = Button(root, text='Capture Frame', command=capture_frame)
capture_button.pack()

# Create button to read classification result
read_button = Button(root, text='Read Results', command=read_results)
read_button.pack()

# Start displaying live stream
display_stream()

# Close serial connection when window is closed
root.protocol("WM_DELETE_WINDOW", lambda: ser.close())

# Run Tkinter event loop
root.mainloop()
