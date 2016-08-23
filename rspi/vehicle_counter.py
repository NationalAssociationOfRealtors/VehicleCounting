import logging
import math

import cv2
import numpy as np

# ============================================================================

CAR_COLOURS = [ (0,0,255), (0,106,255), (0,216,255), (0,255,182), (0,255,76)
    , (144,255,0), (255,255,0), (255,148,0), (255,0,178), (220,0,255) ]

# ============================================================================

class Vehicle(object):
    def __init__(self, id, position):
        self.id = id
        self.positions = [position]
        self.frames_since_seen = 0
        self.counted1 = False
        self.counted2 = False
        self.counted3 = False
        self.counted4 = False
        self.counted5 = False
        self.counted6 = False

    def add_position(self, new_position):
        self.positions.append(new_position)
        self.frames_since_seen = 0

    def draw(self, output_image):
        car_colour = CAR_COLOURS[self.id % len(CAR_COLOURS)]
        for point in self.positions:
            cv2.circle(output_image, point, 2, car_colour, -1)
            cv2.polylines(output_image, [np.int32(self.positions)]
                , False, car_colour, 1)


# ============================================================================

class VehicleCounter(object):
    def __init__(self, shape, divider1, divider2, divider3, divider4, divider5, divider6):

        #self.height, self.width = shape

        self.divider1a_x, self.divider1a_y = divider1[0][0], divider1[0][1]
        self.divider1b_x, self.divider1b_y = divider1[1][0], divider1[1][1]
        self.divider2a_x, self.divider2a_y = divider2[0][0], divider2[0][1]
        self.divider2b_x, self.divider2b_y = divider2[1][0], divider2[1][1]
        self.divider3a_x, self.divider3a_y = divider3[0][0], divider3[0][1]
        self.divider3b_x, self.divider3b_y = divider3[1][0], divider3[1][1]
        self.divider4a_x, self.divider4a_y = divider4[0][0], divider4[0][1]
        self.divider4b_x, self.divider4b_y = divider4[1][0], divider4[1][1]
        self.divider5a_x, self.divider5a_y = divider5[0][0], divider5[0][1]
        self.divider5b_x, self.divider5b_y = divider5[1][0], divider5[1][1]
        self.divider6a_x, self.divider6a_y = divider6[0][0], divider6[0][1]
        self.divider6b_x, self.divider6b_y = divider6[1][0], divider6[1][1]
        
        self.vehicles = []
        self.next_vehicle_id = 0
        self.vehicle_count1 = 0
        self.vehicle_count2 = 0
        self.vehicle_count3 = 0
        self.vehicle_count4 = 0
        self.vehicle_count5 = 0
        self.vehicle_count6 = 0
        self.max_unseen_frames = 3

    @staticmethod
    def get_vector(a, b):
        """Calculate vector (distance, angle in degrees) from point a to point b.

        Angle ranges from -180 to 180 degrees.
        Vector with angle 0 points straight down on the image.
        Values increase in clockwise direction.
        """
        dx = float(b[0] - a[0])
        dy = float(b[1] - a[1])

        distance = math.sqrt(dx**2 + dy**2)

        if dy > 0:
            angle = math.degrees(math.atan(-dx/dy))
        elif dy == 0:
            if dx < 0:
                angle = 90.0
            elif dx > 0:
                angle = -90.0
            else:
                angle = 0.0
        else:
            if dx < 0:
                angle = 180 - math.degrees(math.atan(dx/dy))
            elif dx > 0:
                angle = -180 - math.degrees(math.atan(dx/dy))
            else:
                angle = 180.0        

        return distance, angle 


    @staticmethod
    def is_valid_vector(a):
        distance, angle = a
        #threshold_distance = max(10.0, -0.008 * angle**2 + 0.4 * angle + 25.0)
        #return (distance <= threshold_distance)
        return distance <= 45

    def update_vehicle(self, vehicle, matches):
        # Find if any of the matches fits this vehicle
        for i, match in enumerate(matches):
            centroid = match
            vector = self.get_vector(vehicle.positions[-1], centroid)
            if self.is_valid_vector(vector):
                vehicle.add_position(centroid)
                return i

        # No matches fit...        
        vehicle.frames_since_seen += 1

        return None


    def update_count(self, matches, output_image = None):

        # First update all the existing vehicles
        for vehicle in self.vehicles:
            i = self.update_vehicle(vehicle, matches)
            if i is not None:
                del matches[i]

        # Add new vehicles based on the remaining matches
        for match in matches:
            centroid = match
            new_vehicle = Vehicle(self.next_vehicle_id, centroid)
            self.next_vehicle_id += 1
            self.vehicles.append(new_vehicle)

        # Count any uncounted vehicles that are past the divider
        for vehicle in self.vehicles:
            if not vehicle.counted1 and len(vehicle.positions) > 1 and (vehicle.positions[-1][0] > self.divider1a_x > vehicle.positions[-2][0]) and  self.divider1a_y > vehicle.positions[-1][1] > self.divider1b_y:
                #print vehicle.last_position
                self.vehicle_count1 += 1
                vehicle.counted1 = True
            if not vehicle.counted2 and len(vehicle.positions) > 1 and (vehicle.positions[-1][0] > self.divider2a_x > vehicle.positions[-2][0]) and self.divider2a_y > vehicle.positions[-1][1] > self.divider2b_y:
                self.vehicle_count2 += 1
                vehicle.counted2 = True
            if not vehicle.counted3 and len(vehicle.positions) > 1 and (vehicle.positions[-1][0] > self.divider3a_x > vehicle.positions[-2][0]) and self.divider3a_y > vehicle.positions[-1][1] > self.divider3b_y:
                self.vehicle_count3 += 1
                vehicle.counted3 = True
            if not vehicle.counted4 and len(vehicle.positions) > 1 and (vehicle.positions[-1][0] < self.divider4a_x < vehicle.positions[-2][0]) and self.divider4a_y > vehicle.positions[-1][1] > self.divider4b_y:
                self.vehicle_count4 += 1
                vehicle.counted4 = True
            if not vehicle.counted5 and len(vehicle.positions) > 1 and (vehicle.positions[-1][0] < self.divider5a_x < vehicle.positions[-2][0]) and self.divider5a_y > vehicle.positions[-1][1] > self.divider5b_y:
                self.vehicle_count5 += 1
                vehicle.counted5 = True
            if not vehicle.counted6 and len(vehicle.positions) > 1 and (vehicle.positions[-1][0] < self.divider6a_x < vehicle.positions[-2][0]) and self.divider6a_y > vehicle.positions[-1][1] > self.divider6b_y:
                self.vehicle_count6 += 1
                vehicle.counted6 = True
        # Optionally draw the vehicles on an image
        if output_image is not None:
            for vehicle in self.vehicles:
                vehicle.draw(output_image)

            # cv2.putText(output_image, ("%02d" % self.vehicle_count1), (42, 10)
            #     , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            # cv2.putText(output_image, ("%02d" % self.vehicle_count2), (142, 10)
            #     , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            # cv2.putText(output_image, ("%02d" % self.vehicle_count3), (242, 10)
            #     , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            # cv2.putText(output_image, ("%02d" % self.vehicle_count4), (342, 10)
            #     , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            # cv2.putText(output_image, ("%02d" % self.vehicle_count5), (442, 10)
            #     , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            # cv2.putText(output_image, ("%02d" % self.vehicle_count6), (542, 10)
            #     , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)

            print self.vehicle_count1
            print self.vehicle_count2
            print self.vehicle_count3
            print self.vehicle_count4
            print self.vehicle_count5
            print self.vehicle_count6

            #cv2.putText(output_image, ("%02d" % ((self.vehicle_count + self.vehicle_count2) / 2)), (242, 10)
            #    , cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
        # Remove vehicles that have not been seen long enough
        removed = [ v.id for v in self.vehicles
            if v.frames_since_seen >= self.max_unseen_frames ]
        self.vehicles[:] = [ v for v in self.vehicles
            if not v.frames_since_seen >= self.max_unseen_frames ]
        for id in removed:
            break
