import pygame
import math
import rendering
import sending
import json

METERS_TO_INCHES = 39.37
METERS_TO_PIXELS = METERS_TO_INCHES * rendering.INCHES_TO_PIXELS

with open('default_navgrid.json', 'r') as file:
    data = json.load(file)

node_size_pixels = data["nodeSizeMeters"] * METERS_TO_PIXELS

collision_rects = []
for y_nodes, row in enumerate(data["grid"]):
    for x_nodes, node in enumerate(row):
        if node:
            collision_rects.append(pygame.Rect(x_nodes*node_size_pixels, y_nodes*node_size_pixels, node_size_pixels, node_size_pixels))

def show_obstacles(screen: pygame.Surface):
    for y_nodes, row in enumerate(data["grid"]):
        for x_nodes, node in enumerate(row):
            if node:
                pygame.draw.rect(screen, (0,0,255), (x_nodes*node_size_pixels, y_nodes*node_size_pixels, node_size_pixels, node_size_pixels))


def check_collides(pose: sending.Pose2D):
    for point in get_rotated_points(pose):
        if is_blocked_point(point):
            return True
    return False

def get_rotated_points(pose: sending.Pose2D):
    angle_deg = pose.theta
    angle_rad = math.radians(-angle_deg)
    cx, cy = pose.x * rendering.INCHES_TO_PIXELS, pose.y * rendering.INCHES_TO_PIXELS
    width, height = rendering.ROBOT_FRAME_DIMENSIONS_INCHES[0] * rendering.INCHES_TO_PIXELS, rendering.ROBOT_FRAME_DIMENSIONS_INCHES[1] * rendering.INCHES_TO_PIXELS
    dx, dy = width / 2, height / 2

    corners = [
        (-dx, -dy),
        (dx, -dy),
        (dx, dy),
        (-dx, dy),
    ]

    rotated = []
    for x, y in corners:
        rx = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        ry = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        rotated.append((cx + rx, rendering.FIELD_DIMENSIONS_INCHES[1] * rendering.INCHES_TO_PIXELS - cy + ry))

    return rotated

def render_points(screen: pygame.Surface, points):
    for point in points:
        pygame.draw.circle(screen, (255, 0, 255), point, 1)


def is_blocked_point(point):
    x, y = point
    for y_nodes, row in enumerate(data["grid"]):
        for x_nodes, node_value in enumerate(row):
            if x > x_nodes * node_size_pixels and x < (x_nodes + 1) * node_size_pixels and y > y_nodes * node_size_pixels and y < (y_nodes + 1) * node_size_pixels:
                return node_value
