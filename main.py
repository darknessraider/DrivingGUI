import pygame
import sending
import rendering
import constants

pygame.init()
pygame.display.set_caption("DrivingGUI")
screen = pygame.display.set_mode((constants.X, constants.Y + constants.MENU_HEIGHT))

field_image = pygame.image.load("images/field25.png").convert()
field_image = pygame.transform.smoothscale(field_image, (constants.X, constants.Y))

screen.blit(field_image, (0, 0))
pygame.display.flip()

font = pygame.font.SysFont(None, 36)

mode_toggle_rect = pygame.Rect(constants.MODE_BUTTON_X, constants.MODE_BUTTON_Y, constants.MODE_BUTTON_WIDTH, constants.MODE_BUTTON_HEIGHT)
GUI_control_mode: sending.SendableBoolean = sending.SendableBoolean(False, "GUI_control_mode")

menu_border_rect = pygame.Rect(0, constants.Y, constants.X, constants.MENU_BORDER_THICKNESS)


class Robot:
    def __init__(self, network_pose: sending.SendablePose2D, rendering_pose: rendering.RenderablePose):
        self.network_pose = network_pose
        self.rendering_pose = rendering_pose

    def set_pose_with_pixels(self, x, y):
        self.rendering_pose.set_pose_with_pixels(x, y)
        self.network_pose.set_pose(self.rendering_pose.pose)

robot = Robot(sending.SendablePose2D(sending.Pose2D(17.5, 17.5, 0), "TargetPose"), rendering.RenderablePose(sending.Pose2D(17.5, 17.5, 0), (255, 0, 0)))

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 3):
                x, y = event.pos
                robot.set_pose_with_pixels(x, y)
            if event.button == 1 and mode_toggle_rect.collidepoint(event.pos):
                GUI_control_mode.set_value(not GUI_control_mode.value)


    screen.blit(field_image, (0,0))
    mode_toggle_string = "GUI" if GUI_control_mode.value else "JOYSTICKS"
    text_surface = font.render(mode_toggle_string, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=mode_toggle_rect.center)
    mode_toggle_color = (0, 200, 0) if GUI_control_mode.value else (200, 0, 0)
    pygame.draw.rect(screen, mode_toggle_color, mode_toggle_rect)
    pygame.draw.rect(screen, (80, 80, 80), menu_border_rect)
    screen.blit(text_surface, text_rect)
    robot.rendering_pose.draw(screen)
    screen.fill((30,30,30))

    

pygame.quit()

