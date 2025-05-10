from os import DirEntry
from typing import Callable
import constants
import pygame
import sending

class StandardMenuButton:
    def __init__(self, row: int, column: int, color: tuple, on_click:Callable=(lambda event, self: None), parent=None):
        if row > constants.MENU_HEIGHT / constants.STANDARD_BUTTON_HEIGTH:
            raise Exception(f"There is only room for {int(constants.MENU_HEIGHT / constants.STANDARD_BUTTON_HEIGTH)} row(s)")

        if column > constants.X / constants.STANDARD_BUTTON_WIDTH:
            raise Exception(f"There is only room for {int(constants.X / constants.STANDARD_BUTTON_WIDTH)} columns(s)")

        self.X = column * constants.STANDARD_BUTTON_WIDTH
        self.Y = row * constants.STANDARD_BUTTON_HEIGTH + constants.Y + constants.MENU_BORDER_THICKNESS
        self.rect = pygame.Rect(self.X, self.Y, constants.STANDARD_BUTTON_WIDTH, constants.STANDARD_BUTTON_HEIGTH) 
        self.on_click = on_click
        self.color = color
        ButtonChecker().register_button(self)


    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)

class ToggleButton:
    def __init__(self, row: int, column: int, color: tuple, on_click:Callable=(lambda event, self: None), default_value: bool=False):
        self.value: bool = default_value

        def toggle_on_click():
            self.value = not self.value
            on_click()

        self.button: StandardMenuButton = StandardMenuButton(row, column, color, toggle_on_click, self)


class DirectSendableToggleButton:
    def __init__(self, row: int, column: int, color: tuple, on_click:Callable=(lambda event, self: None), default_value: bool=False):
        self.boolean: sending.SendableBoolean = sending.SendableBoolean(default_value, "GUI_control_mode")

        def toggle_on_click():
            self.boolean.set_value(not self.boolean.value)
            on_click()

        self.button: StandardMenuButton = StandardMenuButton(row, column, color, toggle_on_click, self)



class ButtonChecker:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ButtonChecker, cls).__new__(cls)
        return cls.instance

    def register_button(self, button: StandardMenuButton):
        if not hasattr(self, 'buttons'):
            self.buttons: list[StandardMenuButton] = []
        self.buttons.append(button)

    def periodic(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def on_click_event(self, event):
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                button.on_click()

