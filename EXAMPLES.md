# Examples

## Basic usage

Run the camera demo:
```bash
python main.py
```

## Edge detection mode

Press `1` to enable edge detection. Good for finding object boundaries without AI.

Use cases:
- Shape detection
- Outline detection
- Lane finding for autonomous vehicles

## Motion detection mode

Press `2` to enable motion detection. Compares frames to find movement.

Use cases:
- Security cameras
- Activity monitoring
- Gesture detection

## ROI processing mode

Press `3` to enable ROI (region of interest) processing. Only processes the center of the frame.

Saves about 75% CPU since most interesting stuff happens in the center anyway.

Use cases:
- Dashboard cameras (focus on road ahead)
- Doorbell cameras (focus on door area)
- Drone landing systems (focus on landing pad)

## Frame skipping

Press `+` to skip more frames (faster, less accurate)
Press `-` to skip fewer frames (slower, more accurate)

Processing every 5th frame can save 80% CPU with minimal accuracy loss for many applications.

## Combining techniques

Best results come from combining:
- ROI processing (75% CPU savings)
- Frame skipping every 3rd frame (66% CPU savings)
- Simple algorithms like edge detection instead of deep learning

Total savings: run on 1/12th the CPU power of full frame processing with AI.

