import pygame


class Score:
    def __init__(self, background_image, rect_bottom, score):
        self.score = score
        self.font = pygame.font.Font('fonts/ARCADE.ttf', 25)
        self.render = self.font.render('Score: ' + str(self.score), True,
                                       (255, 255, 255), background_image)
        self.rect = self.render.get_rect()
        self.rect.x = 0
        self.rect.bottom = rect_bottom
