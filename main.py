import pygame
import sending
import rendering
import constants

pygame.init()
pygame.display.set_caption("DrivingGUI")
screen = pygame.display.set_mode((constants.X, constants.Y))
field_image = pygame.image.load("images/field25.png").convert()
field_image = pygame.transform.smoothscale(field_image, (constants.X, constants.Y))
screen.blit(field_image, (0, 0))
pygame.display.flip()

class Robot:
    def __init__(self, network_pose: sending.CommunicablePose2D, rendering_pose: rendering.RenderablePose):
        self.network_pose = network_pose
        self.rendering_pose = rendering_pose

test = rendering.RenderablePose(sending.Pose2D(144, 144, 0), (255, 0, 0))

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False 

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            test.set_pose_with_pixels(x, y)
            


    test.pose = test.pose.add(sending.Pose2D(theta=0.25))

    screen.blit(field_image, (0,0))
    test.draw(screen)
    screen.fill((0,0,0))

    

pygame.quit()

