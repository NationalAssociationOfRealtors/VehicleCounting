# Vehicle_Counting

Using OpenCV to detect and count moving vehicles.

# Prepare(install OpenCV for OS X)

You definetly could install OpenCV from source, but it will be more complicated. Using homebrew is a seay way to go.

  1. Install homebrew (if you don't have it)

    `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    
    or you could find it [here](http://brew.sh)
    
  2. Install Python (if you'd like to use system Python, skip this step)
    
    `brew install python`
    
    Open up the `~/.bash_profile` file (if it does not exist, create it), and append the following

    lines to the file:
    
    `export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH`

    after that, use `which python` to detect the path of current Python

    if the output is `/usr/local/bin/python` , then you are indeed using the Homebrew version of Python. And if your output
    
    is `/usr/bin/python` , then you are still using the system version of Python.
    
    actually I think it is OK to use system Python.
    
  3. Install numpy
  
    `brew install numpy`
    
    then link numpy

    `brew link numpy` 
    
  4. Install OpenCV
  
    `brew tap homebrew/science`

    `brew install opencv --with-contrib --with-ffmpeg --with-tbb`
    
    it is important to add the option `--with-ffmpeg --with-tbb` for decoding some format of video
    
    then set up Python with OpenCV (if you use the system version of Python)
    
    `cd /Library/Python/2.7/site-packages/`
    
    `ln -s /usr/local/Cellar/opencv3/3.1.0_3/lib/python2.7/site-packages/cv2.so cv2.so` (you may need `sudo`)
    
    Then it's done!(I'm not sure if there are useless steps here, if so I'll update it)
    
    You could slso install OpenCV3 use `brew install opencv3`
  
  5. If you can't import cv2, try
    `ln -s -f /usr/local/Cellar/opencv/2.4.13/lib/python2.7/site-packages/cv2.so /usr/local/lib/python2.7/site-packages/cv2.so`

    you may need `sudo`

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

    2. Strong sunlight will make some light color vehicle 'disappear'.
