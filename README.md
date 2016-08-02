# Vehicle_Counting

# Main steps of the image processing:
    1.Read the video frame by frame.
  
    2.Apply some fileters to the frame(dilation, etc.).
  
    3.Use BackgroundSubtractor to split the foreground from background(white-foreground, black-background).
  
    4.Detect the contours of the foreground(moving objects).
  
    5.Calculate the centroid of each moving object.
  
    6.For each centroid, detect if there's a nearby centroid of the last frame. If so, assign them to the same vehicle.
  
    7.For each vehicle, detect whether it crossed the target line.

Simply run main_fei_dybg.py.

Using OpenCV lib to detect and track vehicles. 

...

Problems:

1. Frame rate.

2. Streaming from cam.
