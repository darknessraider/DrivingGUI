import pygame
import sending
import rendering
import constants
import user_interface
import receiving
import setpoints
import obstacle_detection
import datetime
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

mode_toggle_button = user_interface.ToggleButton(0, 0, (0, 255, 0), (255, 0, 0), "Mouse", "Joysticks", on_click_mode_toggle_button)

safe_mode_button = user_interface.ToggleButton(1, 0, true_text="safe", false_text="unsafe", default_value=True)

unsafe_move_popup = user_interface.PopUp("cannot move there", datetime.timedelta(seconds=0.5))

connected_indicator = user_interface.BooleanIndicator(0, 1, (0, 255, 0), (255, 0, 0), "Connected", "Disconnected")

raise_elevator_command = sending.NamedCommand("PrepareLevel4")

def raise_elevator_on_click(button, event):
    raise_elevator_command.run()

raise_elevator = user_interface.StandardMenuButton(0, 2, color=(0, 0, 255), text="Raise Elevator", on_click=raise_elevator_on_click)

def connection_listener(connected, info):
    connected_indicator.value = connected

NetworkTables.addConnectionListener(connection_listener)

menu_border_rect = pygame.Rect(0, constants.Y, constants.X, constants.MENU_BORDER_THICKNESS)


class Robot:
    def __init__(self, network_pose: sending.SendablePose2D, rendering_pose: rendering.RenderablePose):
        self.network_pose = network_pose
        self.rendering_pose = rendering_pose

    def set_pose_with_pixels(self, x, y):
        original_pose = self.rendering_pose.pose.copy()

        self.rendering_pose.set_pose_with_pixels(x, y)

        if obstacle_detection.check_collides(self.rendering_pose.pose) and safe_mode_button.value:
            unsafe_move_popup.activate()
            self.rendering_pose.pose = original_pose

        self.network_pose.set_pose(self.rendering_pose.pose)


    def set_rotation(self, theta):
        original_pose = self.rendering_pose.pose.copy()

        self.rendering_pose.pose.theta = theta

        if obstacle_detection.check_collides(self.rendering_pose.pose) and safe_mode_button.value:
            unsafe_move_popup.activate()
            self.rendering_pose.pose = original_pose

        self.network_pose.set_pose(self.rendering_pose.pose)


targetRobotState = Robot(sending.SendablePose2D(sending.Pose2D(17.5, 17.5, 0), "TargetPose"), rendering.RenderablePose(sending.Pose2D(17.5, 17.5, 0), (255, 0, 0)))
currentPose = receiving.ReceivablePose2D("current_pose")
currentRenderPose = rendering.RenderablePose(currentPose.get_pose(), (0, 255, 0))

test_setpoint = setpoints.SetPoint(sending.Pose2D(75, 75, 0))
test_setpoint_2 = setpoints.SetPoint(sending.Pose2D(100, 100, 0))

user_interface_updater = user_interface.UserInterfaceUpdater()

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 3):
                x, y = event.pos

                targetRobotState.set_pose_with_pixels(x, y)

            if event.button == 1:
                user_interface_updater.on_click_event(event)
                clicked_set_point = setpoints.SetPointUpdater.get_clicked_setpoint(event.pos)

                if clicked_set_point != None:
                    targetRobotState.network_pose.set_pose(clicked_set_point.render_pose.pose.copy())
                    targetRobotState.rendering_pose.pose = clicked_set_point.render_pose.pose.copy()


        if event.type == pygame.MOUSEWHEEL:
            targetRobotState.set_rotation(targetRobotState.rendering_pose.pose.theta + event.y * 10)

    currentRenderPose.pose = currentPose.get_pose()

    screen.blit(field_image, (0, 0))
    pygame.draw.rect(screen, (80, 80, 80), menu_border_rect)
    currentRenderPose.draw(screen)
    targetRobotState.rendering_pose.draw(screen)
    setpoints.SetPointUpdater.draw_points(screen)
    user_interface_updater.periodic(screen)
    pygame.display.flip()
    screen.fill((30,30,30))


pygame.quit()

