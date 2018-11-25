import pygame


class Information:
    def __init__(self, information, rect_bottom, x, background_image):
        self.font = pygame.font.Font('fonts/ARCADE.ttf', 20)
        self.render = self.font.render(information, True, (255, 255, 255),
                                       background_image)
        self.rect = self.render.get_rect()
        self.rect.x = x
        self.rect.bottom = rect_bottom
