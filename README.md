# Embedded Camera

Playing around with ways to save CPU and power when doing computer vision on cheap hardware. Has edge detection, motion detection, and frame skipping.

## What it does

- Edge detection with Canny
- Motion detection by comparing frames
- ROI processing that only looks at center of frame
- Frame skipping to process every Nth frame
- FPS counter

Testing techniques that work on low power boards without needing a GPU.

## Python version matters

Use Python 3.11 or 3.12. If you're on Python 3.14, the app will crash right after printing "Loading..." because numpy doesn't have stable Windows builds for it yet. You'll see scary warnings about experimental builds and crashes being expected. That's the problem.

Python 3.13 might work but I haven't tested it. 3.12 is your safest bet.

Check what you have:
```
python --version
```

If it says 3.14, go download 3.12 from python.org first.

## Setup

If you have Python 3.12 as your default:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

If Python 3.14 is your default but you installed 3.12:
```
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Controls

1 = edge detection
2 = motion detection  
3 = ROI processing
4 = normal view
+ = skip more frames (faster, less accurate)
- = skip fewer frames (slower, more accurate)
q = quit

## Troubleshooting

### Crashes after "Loading..." with no window

This is the Python 3.14 problem. You'll see warnings about numpy being experimental and crashes expected. The import of cv2 fails silently because numpy can't load properly.

Fix it:
```
Remove-Item -Recurse -Force venv
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

You need to delete the old venv and make a new one with Python 3.12.

### Still crashing silently

OpenCV versions 4.11 and newer have DLL loading issues on some Windows setups. The requirements.txt file pins it to 4.10.0.84 which works. If pip grabbed the wrong version somehow:

```
pip uninstall opencv-python -y
pip install -r requirements.txt
```

### Camera won't open

Close anything else using your camera. On Windows check your privacy settings to make sure apps can access the camera. Test if Python can see it:
```
python -c "import cv2; cap = cv2.VideoCapture(0); print('Works' if cap.isOpened() else 'Nope'); cap.release()"
```

### Import errors

Make sure the venv is activated. You should see (venv) in your terminal prompt. If not, run:
```
.\venv\Scripts\Activate.ps1
```

Then install dependencies again:
```
pip install -r requirements.txt
```

## How it works

Edge detection uses Canny algorithm to find boundaries in the image. Motion detection subtracts the previous frame from current frame to see what changed. ROI mode only processes the middle 50% of the frame which cuts CPU usage by about 75%. Frame skipping just processes every 2nd or 3rd frame instead of all of them.

The FPS counter and processing time show you what's actually happening performance-wise. Try different modes and watch how the numbers change.

Good for battery powered stuff or boards with weak CPUs where you can't afford to process every pixel of every frame.

## Tech

OpenCV handles camera and image processing. Numpy does the array math. Standard computer vision stuff with no deep learning so it runs on anything that can handle Python.
