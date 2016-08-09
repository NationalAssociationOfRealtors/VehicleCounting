import os
import sys
import math
import cv2
import numpy as np

from vehicle_counter_fei import VehicleCounter

# ============================================================================

# Colours for drawing on processed frames    
DIVIDER_COLOUR = (255, 255, 0)
BOUNDING_BOX_COLOUR = (255, 0, 0)
CENTROID_COLOUR = (0, 0, 255)

# ============================================================================

def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)

# ============================================================================


def combined_nearby_centroid(centroid_pool):
    centroid_combined = []
    for (i, centroid) in enumerate(centroid_pool):
        flag = 0
        for entry in centroid_combined:
            if centroid in entry:
                flag = 1
                break
        if flag == 0:
            centroid_combined.append([centroid])
        for j in range(i, len(centroid_pool)):
            #if math.sqrt((centroid[0] - centroid_pool[j][0]) ** 2 + (centroid[1] - centroid_pool[j][1]) ** 2) <= 200: #abs(centroid[0] - centroid_pool[j][0]) < 90 and abs(centroid[1] - centroid_pool[j][1]) < 90:
            if abs(centroid[0] - centroid_pool[j][0]) < 100 and abs(centroid[1] - centroid_pool[j][1]) < 40:    
                for entry in centroid_combined:
                    if centroid in entry and centroid_pool[j] not in entry:
                        entry.append(centroid_pool[j])
    return centroid_combined

def detect_vehicles(fg_mask):

    MIN_CONTOUR_WIDTH = 15
    MIN_CONTOUR_HEIGHT = 15

    # Find the contours of any vehicles in the image
    contours, hierarchy = cv2.findContours(fg_mask
        , cv2.RETR_EXTERNAL
        , cv2.CHAIN_APPROX_SIMPLE)

    matches = []
    centroid_aftercal = []
    for (i, contour) in enumerate(contours):
        #print contours
        (x, y, w, h) = cv2.boundingRect(contour)
        contour_valid = (w >= MIN_CONTOUR_WIDTH) and (h >= MIN_CONTOUR_HEIGHT)

        if not contour_valid:
            continue

        centroid = get_centroid(x, y, w, h)

        matches.append(centroid)
    print matches
    centroid_combined = combined_nearby_centroid(matches)
    for entry in centroid_combined:
                tempx = []
                tempy = []
                for centroid in entry:
                    tempx.append(centroid[0])
                    tempy.append(centroid[1])
                centroid_aftercal.append((sum(tempx) / len(tempx), sum(tempy) / len(tempy)))
    return centroid_aftercal

# ============================================================================

def filter_mask(fg_mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # Fill any small holes
    closing = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    # Remove noise
    #opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    # Dilate to merge adjacent blobs
    dilation = cv2.dilate(opening, kernel, iterations = 2)

    return dilation

# ============================================================================

def process_frame(frame, bg_subtractor, car_counter):

    # Create a copy of source frame to draw into
    processed = frame.copy()

    # Draw dividing line -- we count cars as they cross this line.
    cv2.line(processed, (car_counter.divider, frame.shape[0]), (car_counter.divider, 290), DIVIDER_COLOUR, 1)
    cv2.line(processed, (car_counter.divider2, frame.shape[0]), (car_counter.divider2, 290), DIVIDER_COLOUR, 1)
    cv2.line(processed, (car_counter.divider3, frame.shape[0]), (car_counter.divider3, 290), DIVIDER_COLOUR, 1)
    cv2.line(processed, (car_counter.divider, 250), (car_counter.divider, 140), DIVIDER_COLOUR, 1)
    cv2.line(processed, (car_counter.divider2, 250), (car_counter.divider2, 140), DIVIDER_COLOUR, 1)
    # Remove the background
    fg_mask = bg_subtractor.apply(frame, None, 0.01)
    fg_mask = filter_mask(fg_mask)

    matches = detect_vehicles(fg_mask)

    for (i, match) in enumerate(matches):
        centroid = match

        # Mark the bounding box and the centroid on the processed frame
        # NB: Fixed the off-by one in the bottom right corner
        #cv2.rectangle(processed, (x, y), (x + w - 1, y + h - 1), BOUNDING_BOX_COLOUR, 1)
        cv2.circle(processed, centroid, 2, CENTROID_COLOUR, -1)

    car_counter.update_count(matches, processed)

    return processed
    #return fg_mask
# ============================================================================

def main():
    bg_subtractor = cv2.BackgroundSubtractorMOG2()

    car_counter = None # Will be created after first frame is captured

    # Set up image source

    #cap = cv2.VideoCapture("flow.mp4")
    cap = cv2.VideoCapture("rtsp://crtlabs:Abudabu1!@430n.crtlabs.org:554/videoMain")
    while True:
        ret, frame = cap.read()
        if not ret:
            print 'failed'
        else:
            if car_counter is None:
                # We do this here, so that we can initialize with actual frame size
                #car_counter = VehicleCounter(frame.shape[:2], frame.shape[1] / 2)
                car_counter = VehicleCounter(frame.shape[:2], frame.shape[1] / 3)
                #print frame.shape
            # Archive raw frames from video to disk for later inspection/testing

            processed = process_frame(frame, bg_subtractor, car_counter)

            #cv2.imshow('Source Image', frame)
            cv2.imshow('Processed Image', processed)

            c = cv2.waitKey(10)
            if c == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

# ============================================================================

if __name__ == "__main__":

    main()