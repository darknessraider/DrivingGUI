import pygame
import sending
import constants 
import math

ROBOT_FRAME_DIMENSIONS_INCHES = (35, 35)
FIELD_DIMENSIONS_INCHES = (690, 317)
INCHES_TO_PIXELS = constants.X / FIELD_DIMENSIONS_INCHES[0]
BORDER_THICKNESS = 5

class RenderablePose:
    def __init__(self, pose: sending.Pose2D, color: tuple, hollow: bool=False):
        self.arrow_image = pygame.image.load("images/arrow.png").convert_alpha()
        px_array = pygame.PixelArray(self.arrow_image)
        px_array.replace((0,0,0), (255, 255, 255))
        del px_array

        #self.arrow_image = pygame.transform.rotate(self.arrow_image, 90)

        self.hollow = hollow

        arrow_width = self.arrow_image.get_width() // 10
        arrow_height = self.arrow_image.get_height() // 10

        self.arrow_image = pygame.transform.smoothscale(self.arrow_image, (arrow_width, arrow_height))

        self.color = color
        self.pose: sending.Pose2D = pose

        self.rectangle = pygame.Surface((ROBOT_FRAME_DIMENSIONS_INCHES[0] * INCHES_TO_PIXELS, 
                                         ROBOT_FRAME_DIMENSIONS_INCHES[1] * INCHES_TO_PIXELS), 
                                         pygame.SRCALPHA)


    def draw(self, screen: pygame.Surface):
        x = self.pose.x * INCHES_TO_PIXELS
        y = constants.Y - (self.pose.y * INCHES_TO_PIXELS)
        if self.hollow:
            pygame.draw.rect(self.rectangle, self.color, self.rectangle.get_rect(), width=10)
        else:
            self.rectangle.fill(self.color)

        arrow_rect = self.arrow_image.get_rect(center=(self.rectangle.get_width() // 2,
                                                       self.rectangle.get_height() // 2))

        self.rectangle.blit(self.arrow_image, arrow_rect)
        rotated_rectangle = pygame.transform.rotate(self.rectangle, self.pose.theta)
        rect_rect = rotated_rectangle.get_rect(center=(x, y)) 
        screen.blit(rotated_rectangle, rect_rect.topleft)


    def set_pose_with_pixels(self, x, y):
        self.pose.x = x * (1/INCHES_TO_PIXELS)
        self.pose.y = FIELD_DIMENSIONS_INCHES[1] - (y * (1/INCHES_TO_PIXELS))

