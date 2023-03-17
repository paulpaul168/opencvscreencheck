# Screen Crack Detection and Color Detection using OpenCV

This repository contains a Python script that uses OpenCV library to detect cracks on a screen and determine its color.

# Installation

To use this script, you must have OpenCV and NumPy installed. You can install them using pip:

```python
pip install opencv-python numpy
```

# Usage

To use this script, simply run the main.py file:
```python
python main.py
```

A window will open showing the live feed from your webcam. When a screen is detected, the script will draw a green rectangle around it. If a crack is detected on the screen, the script will draw a red contour around it and print "Screen is cracked" in the console. The script will also determine the dominant color of the screen and print it in the console.

# Contributing

Contributions are welcome! If you find a bug or want to add a new feature, feel free to open an issue or submit a pull request.

# License

This project is licensed under the MIT License - see the LICENSE file for details.