"""
Camera demo with embedded optimization techniques.

Shows different ways to reduce CPU usage for computer vision on low power hardware.
Includes edge detection, motion detection, ROI processing, and frame skipping.
"""

print("Loading...", flush=True)

import cv2
import numpy as np
import time

print("Loaded", flush=True)

def edge_detection(frame):
    """
    Applies Canny edge detection to find object boundaries.
    Converts to grayscale first since edges work on intensity.
    
    Args:
        frame: BGR image from camera
        
    Returns:
        Binary image where white pixels are edges
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges

def motion_detection(frame, prev_frame):
    """
    Detects motion by comparing current frame to previous frame.
    Finds pixels that changed between frames.
    
    Args:
        frame: Current BGR frame
        prev_frame: Previous BGR frame (or None for first frame)
        
    Returns:
        tuple: (motion_mask, motion_percentage) or (None, 0) if no previous frame
    """
    if prev_frame is None:
        return None, 0
    
    diff = cv2.absdiff(frame, prev_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    motion_pixels = np.count_nonzero(thresh)
    motion_percent = (motion_pixels / thresh.size) * 100
    
    return thresh, motion_percent

def roi_processing(frame):
    """
    Processes only the center region of the frame.
    Saves CPU by ignoring edges where nothing important usually happens.
    
    Args:
        frame: Input BGR frame
        
    Returns:
        tuple: (display_frame_with_box, roi_region)
    """
    h, w = frame.shape[:2]
    roi_x1, roi_y1 = w // 4, h // 4
    roi_x2, roi_y2 = 3 * w // 4, 3 * h // 4
    
    roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
    
    display = frame.copy()
    cv2.rectangle(display, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)
    
    return display, roi

def main():
    print("\nCamera Demo")
    print("Opening camera...")
    
    cap = None
    
    for camera_idx in [0, 1, 2]:
        print(f"Trying camera {camera_idx}...")
        cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, test_frame = cap.read()
            if ret:
                print(f"Opened camera {camera_idx}")
                break
            else:
                cap.release()
                cap = None
        else:
            cap = None
    
    if cap is None or not cap.isOpened():
        print("\nCouldn't open camera")
        print("Check if another app is using it")
        input("\nPress Enter to exit...")
        return
    
    print("\nControls:")
    print("  1 - Edge detection")
    print("  2 - Motion detection")
    print("  3 - ROI processing")
    print("  4 - Normal view")
    print("  + - Skip more frames")
    print("  - - Skip fewer frames")
    print("  q - Quit")
    print()
    
    mode = 'original'
    frame_skip = 2
    frame_count = 0
    prev_frame = None
    fps_history = []
    last_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to get frame")
            break
        
        frame_count += 1
        
        if frame_count % frame_skip != 0:
            continue
        
        current_time = time.time()
        elapsed = current_time - last_time
        if elapsed > 0:
            fps = 1.0 / elapsed
            fps_history.append(fps)
            if len(fps_history) > 30:
                fps_history.pop(0)
        last_time = current_time
        
        process_start = time.perf_counter()
        
        display = frame.copy()
        info_text = ""
        
        if mode == 'edge':
            edges = edge_detection(frame)
            display = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            info_text = "Edge Detection"
            
        elif mode == 'motion':
            motion_mask, motion_pct = motion_detection(frame, prev_frame)
            if motion_mask is not None:
                display = cv2.cvtColor(motion_mask, cv2.COLOR_GRAY2BGR)
                cv2.putText(display, f"Motion: {motion_pct:.1f}%", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            info_text = "Motion Detection"
            prev_frame = frame.copy()
            
        elif mode == 'roi':
            display, roi = roi_processing(frame)
            info_text = "ROI Processing"
            
        else:
            info_text = "Original"
        
        process_time = (time.perf_counter() - process_start) * 1000
        
        avg_fps = np.mean(fps_history) if fps_history else 0
        
        cv2.putText(display, f"Mode: {info_text}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(display, f"FPS: {avg_fps:.1f} | {process_time:.1f}ms", (10, display.shape[0] - 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(display, f"Skip: 1/{frame_skip}", (10, display.shape[0] - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        cv2.imshow('Camera Demo', display)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('1'):
            mode = 'edge'
            print("Mode: Edge Detection")
        elif key == ord('2'):
            mode = 'motion'
            prev_frame = None
            print("Mode: Motion Detection")
        elif key == ord('3'):
            mode = 'roi'
            print("Mode: ROI Processing")
        elif key == ord('4'):
            mode = 'original'
            print("Mode: Original")
        elif key == ord('+') or key == ord('='):
            frame_skip = min(10, frame_skip + 1)
            print(f"Skip: 1/{frame_skip}")
        elif key == ord('-') or key == ord('_'):
            frame_skip = max(1, frame_skip - 1)
            print(f"Skip: 1/{frame_skip}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    if fps_history:
        print(f"\nAvg FPS: {np.mean(fps_history):.1f}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
