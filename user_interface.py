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
        if self.parent:
            self.parent.draw(screen)


class ToggleButton:
    def __init__(self, row: int,
                       column: int,
                       true_color: tuple = (0,255,0),
                       false_color: tuple = (255,0,0),
                       true_text: str = "on",
                       false_text: str = "off",
                       on_click:Callable = (lambda event, self: None), 
                       default_value: bool=False):
        self.value: bool = default_value

        def toggle_on_click(button, event):
            self.value = not self.value
            on_click(button, event)

        self.button: StandardMenuButton = StandardMenuButton(row, column, true_color if self.value else false_color, toggle_on_click, self)

        def toggle_color_on_click(button, event):
            toggle_on_click(button, event)
            self.button.color = true_color if self.value else false_color

        self.true_text = true_text
        self.false_text = false_text
        self.button.on_click = toggle_color_on_click
        self.font = pygame.font.SysFont(None, 36)


    def draw(self, screen: pygame.Surface):
        text = self.font.render(self.true_text if self.value else self.false_text, True, (255, 255, 255))
        screen.blit(text, self.button.rect)


class BooleanIndicator:
    def __init__(self, row: int, column: int, true_color: tuple, false_color: tuple, true_text: str, false_text: str):
        self.value: bool = False

        if row > (constants.MENU_HEIGHT / constants.STANDARD_BUTTON_HEIGTH) - 1:
            raise Exception(f"There is only room for {int(constants.MENU_HEIGHT / constants.STANDARD_BUTTON_HEIGTH)} row(s)")

        if column > (constants.X / constants.STANDARD_BUTTON_WIDTH) - 1:
            raise Exception(f"There is only room for {int(constants.X / constants.STANDARD_BUTTON_WIDTH)} columns(s)")

        self.X = column * constants.STANDARD_BUTTON_WIDTH
        self.Y = row * constants.STANDARD_BUTTON_HEIGTH + constants.Y + constants.MENU_BORDER_THICKNESS
        self.rect = pygame.Rect(self.X, self.Y, constants.STANDARD_BUTTON_WIDTH, constants.STANDARD_BUTTON_HEIGTH) 

        self.true_color = true_color
        self.false_color = false_color
        self.true_text = true_text
        self.false_text = false_text
        self.font = pygame.font.SysFont(None, 30)

        UserInterfaceUpdater().register_indicator(self)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.true_color if self.value else self.false_color, self.rect)
        text = self.font.render(self.true_text if self.value else self.false_text, True, (255, 255, 255))
        screen.blit(text, self.rect)


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

