# Vehicle_Counting

Using OpenCV to detect and count moving vehicles.

# Prepare(for OS X)

1. Install homebrew(if you don't have it)

    `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    
    or you could find it [here](http://brew.sh)

# Main steps of the image processing:

    1.Read the video frame by frame.
  
    2.Apply some fileters to the frame(dilation, etc.).
  
    3.Use BackgroundSubtractor to split the foreground from background(white-foreground, black-background).
  
    4.Detect the contours of the foreground(moving objects).
  
    5.Calculate the centroid of each moving object.
  
    6.For each centroid, detect if there's a nearby centroid of the last frame. If so, assign them to the same vehicle.
  
    7.For each vehicle, detect whether it crossed the target line.
 
Simply run main_fei_dybg.py.

...

Camshift is not good for tracking vehicle due to the sunlight is too strong at day time.

Problems:

    1. Frame rate might be a problem.

    2. Could not read the RTSP stream.

    3. Strong sunlight will make some light color vehicle 'disappear'.
