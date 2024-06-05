import math

def calculate_angle(x1, y1, x2, y2):
    delta_y = y2 - y1
    delta_x = x2 - x1
    theta = math.atan2(delta_y, delta_x)
    theta_deg = math.degrees(theta)
    return theta_deg