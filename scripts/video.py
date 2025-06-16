import cv2
from ultralytics import YOLO
from tkinter import Tk, filedialog
import os

# Hide Tkinter root window
Tk().withdraw()

# Ask user to pick a video file
video_path = filedialog.askopenfilename(
    title="Select a video file",
    filetypes=[("Video files", "*.mp4 *.avi *.mov")]
)
if not video_path:
    raise ValueError("No video file selected.")

# Ask user to pick a model file
model_path = filedialog.askopenfilename(
    title="Select a YOLO model (.pt)",
    filetypes=[("YOLO model", "*.pt *.pth")]
)
if not model_path:
    raise ValueError("No model file selected.")

# Ask for confidence threshold
conf = input("Enter confidence threshold (e.g., 0.25): ").strip()
conf = float(conf) if conf else 0.25

# Load model
model = YOLO(model_path)
model.conf = conf

# Open video
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), f"Cannot open video: {video_path}"

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
video_length = frame_count / fps
print(f"\nVideo: {os.path.basename(video_path)} | FPS: {fps:.2f} | Frames: {frame_count} | Duration: {video_length:.2f}s")

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or can't read frame.")
        break

    # Inference
    results = model(frame)[0]
    annotated_frame = results.plot()

    # Display
    cv2.imshow("YOLOv8 Live Inference (Q=Quit, D=+5s, A=-5s)", annotated_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('d'):
        # Forward 5 seconds
        curr = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(curr + 5 * fps, frame_count - 1))
    elif key == ord('a'):
        # Backward 5 seconds
        curr = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(curr - 5 * fps, 0))

cap.release()
cv2.destroyAllWindows()
