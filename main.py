import pygame
import sending
import rendering
import constants
import user_interface
from networktables import NetworkTables

sending.NetworkTableWrapper()

pygame.init()
pygame.display.set_caption("DrivingGUI")
screen = pygame.display.set_mode((constants.X, constants.Y + constants.MENU_HEIGHT))

field_image = pygame.image.load("images/field25.png").convert()
field_image = pygame.transform.smoothscale(field_image, (constants.X, constants.Y))

screen.blit(field_image, (0, 0))
pygame.display.flip()

font = pygame.font.SysFont(None, 36)

mode_toggle_boolean: sending.SendableBoolean = sending.SendableBoolean(False, "GUI_control_mode")

def on_click_mode_toggle_button(button, event):
    mode_toggle_boolean.set_value(button.parent.value)

mode_toggle_button: user_interface.ToggleButton = user_interface.ToggleButton(0, 0, (0, 255, 0), (255, 0, 0), "Mouse", "Joysticks", on_click_mode_toggle_button)

connected_indicator = user_interface.BooleanIndicator(0, 1, (0, 255, 0), (255, 0, 0), "Connected", "Disconnected")

def connection_listener(connected, info):
    connected_indicator.value = connected

NetworkTables.addConnectionListener(connection_listener)

menu_border_rect = pygame.Rect(0, constants.Y, constants.X, constants.MENU_BORDER_THICKNESS)


class Robot:
    def __init__(self, network_pose: sending.SendablePose2D, rendering_pose: rendering.RenderablePose):
        self.network_pose = network_pose
        self.rendering_pose = rendering_pose

    def set_pose_with_pixels(self, x, y):
        self.rendering_pose.set_pose_with_pixels(x, y)
        self.network_pose.set_pose(self.rendering_pose.pose)


robot = Robot(sending.SendablePose2D(sending.Pose2D(17.5, 17.5, 0), "TargetPose"), rendering.RenderablePose(sending.Pose2D(17.5, 17.5, 0), (255, 0, 0)))
user_interface_updater = user_interface.UserInterfaceUpdater()

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 3):
                x, y = event.pos
                robot.set_pose_with_pixels(x, y)
            if event.button == 1:
                user_interface_updater.on_click_event(event)


    user_interface_updater.periodic(screen)
    screen.blit(field_image, (0,0))
    pygame.draw.rect(screen, (80, 80, 80), menu_border_rect)
    robot.rendering_pose.draw(screen)
    screen.fill((30,30,30))


pygame.quit()

