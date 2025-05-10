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
        self.parent = parent
        UserInterfaceUpdater().register_button(self)


    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)


class ToggleButton:
    def __init__(self, row: int, column: int, true_color: tuple, false_color: tuple, on_click:Callable=(lambda event, self: None), default_value: bool=False):
        self.value: bool = default_value

        def toggle_on_click(button, event):
            self.value = not self.value
            on_click(button, event)

        self.button: StandardMenuButton = StandardMenuButton(row, column, true_color if self.value else false_color, toggle_on_click, self)

        def toggle_color_on_click(button, event):
            toggle_on_click(button, event)
            self.button.color = true_color if self.value else false_color

        self.button.on_click = toggle_color_on_click


class BooleanIndicator:
    def __init__(self, row: int, column: int, true_color: tuple, false_color: tuple):
        self.value: bool = False

        if row > constants.MENU_HEIGHT / constants.STANDARD_BUTTON_HEIGTH:
            raise Exception(f"There is only room for {int(constants.MENU_HEIGHT / constants.STANDARD_BUTTON_HEIGTH)} row(s)")

        if column > constants.X / constants.STANDARD_BUTTON_WIDTH:
            raise Exception(f"There is only room for {int(constants.X / constants.STANDARD_BUTTON_WIDTH)} columns(s)")

        self.X = column * constants.STANDARD_BUTTON_WIDTH
        self.Y = row * constants.STANDARD_BUTTON_HEIGTH + constants.Y + constants.MENU_BORDER_THICKNESS
        self.rect = pygame.Rect(self.X, self.Y, constants.STANDARD_BUTTON_WIDTH, constants.STANDARD_BUTTON_HEIGTH) 

        self.true_color = true_color
        self.false_color = false_color

        UserInterfaceUpdater().register_indicator(self)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.true_color if self.value else self.false_color, self.rect)


class UserInterfaceUpdater:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserInterfaceUpdater, cls).__new__(cls)
            cls.instance.buttons = []
            cls.instance.indicators = []
        return cls.instance

    def register_button(self, button: StandardMenuButton):
        if not hasattr(self, 'buttons'):
            self.buttons: list[StandardMenuButton] = []
        self.buttons.append(button)

    def register_indicator(self, indicator: BooleanIndicator):
        if not hasattr(self, 'indicators'):
            self.indicators: list = []
        self.indicators.append(indicator)

    def periodic(self, screen):
        for button in self.buttons:
            button.draw(screen)
        for indicator in self.indicators:
            indicator.draw(screen)

    def on_click_event(self, event):
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                button.on_click(button, event)

