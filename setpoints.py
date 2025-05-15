import sending
import rendering
import constants
import pygame


class SetPoint:
    def __init__(self, pose: sending.Pose2D):
        self.pose = pose;
        self.render_pose = rendering.RenderablePose(pose, (0, 0, 255), True)
        SetPointUpdater.set_points.append(self)


    def is_clicked(self, pos):
        x = self.pose.x * rendering.INCHES_TO_PIXELS
        y = constants.Y - (self.pose.y * rendering.INCHES_TO_PIXELS)

        rotated_rectangle = pygame.transform.rotate(self.render_pose.rectangle, self.pose.theta)
        rect_rect = rotated_rectangle.get_rect(center=(x, y))
        return rect_rect.collidepoint(pos)


class SetPointUpdater:
    set_points: list[SetPoint] = []

    @staticmethod
    def register_setpoint(point: SetPoint):
        SetPointUpdater.set_points.append(point)


    @staticmethod
    def draw_points(screen: pygame.Surface):
        for setpoint in SetPointUpdater.set_points:
            setpoint.render_pose.draw(screen);


    @staticmethod
    def get_clicked_setpoint(pos):
        for setpoint in SetPointUpdater.set_points:
            if setpoint.is_clicked(pos):
                return setpoint
        return None

