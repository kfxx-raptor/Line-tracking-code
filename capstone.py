import cv2
import numpy as np

def roi(image, vertices):
    mask = np.zeros_like(image)
    mask_color = 255
    cv2.fillPoly(mask, [np.array(vertices, np.int32)], mask_color)
    return cv2.bitwise_and(image, mask)

def draw_lines(image, hough_lines):
    if hough_lines is None:   
        return image
    for line in hough_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return image

def process(img):
    h, w = img.shape[:2]
    roi_vertices = [(0, 650), (2*w//3, 2*h//3), (w, 1000)]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.dilate(gray, kernel=np.ones((3,3), np.uint8))
    edges = cv2.Canny(gray, 130, 220)
    edges_roi = roi(edges, roi_vertices)
    lines = cv2.HoughLinesP(edges_roi, 1, np.pi/180, threshold=10, minLineLength=15, maxLineGap=2)
    out = draw_lines(img.copy(), lines)
    return out

cap = cv2.VideoCapture("./lane_vid2.mp4")
if not cap.isOpened():
    raise RuntimeError("영상 파일을 열 수 없습니다: ./Data/lane_vid2.mp4")

frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0  


fourcc = cv2.VideoWriter_fourcc(*"mp4v")          
out_path = "lane_detection.mp4"                    
saved_frame = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height))
if not saved_frame.isOpened():
    raise RuntimeError("VideoWriter를 열 수 없습니다. 코덱/경로/해상도 확인")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = process(frame)

    
    if frame.shape[1] != frame_width or frame.shape[0] != frame_height:
        frame = cv2.resize(frame, (frame_width, frame_height))
    if frame.ndim == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    saved_frame.write(frame)


cap.release()
saved_frame.release()
print("Saved to:", out_path)