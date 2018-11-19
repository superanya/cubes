import random
import pygame
import sys
from field import Field
from score import Score
from information import Information


class Game:
    def __init__(self,
                 caption,
                 back_image_filename,
                 frame_rate,
                 colors,
                 size='small'):
        self.background_image = \
            pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.set_field_parameters(size, colors)
        self.width, self.height, self.colors = \
            self.set_field_parameters(size, colors)
        self.object = Field(self.colors, self.width, self.height)
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((700, 393))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.total_score = 0
        self.score = Score(self.background_image, 393, self.total_score)
        self.start_new_game = [525, 365, 'Start new game', (255, 255, 255)]
        self.height_information = 365
        self.width_information = 0
        self.information_about_colors = \
            self.set_information_about_colors(back_image_filename)

    def set_information_about_colors(self, back_image_filename, color_remove=None, count=0):
        iteration = 0
        information_about_colors = []
        for color in self.colors:
            if color.value is color_remove:
                self.object.color2count[color.name] -= count
            text = '{}: {}'.format(color.name,
                                   self.object.color2count[color.name])
            information_about_colors.append(
                Information(text,
                            self.height_information,
                            self.width_information,
                            back_image_filename))
            self.height_information -= 20
            iteration += 1
            if iteration == 4:
                self.width_information = 525
                self.height_information = 365
        return information_about_colors

    def update_score(self, score):
        self.total_score += score
        self.score = Score(self.background_image, 393, self.total_score)

    def update_color_information(self, back_image_filename, color_remove, count):
        self.height_information = 365
        self.width_information = 0
        self.information_about_colors = self.set_information_about_colors(back_image_filename,
                                                                          color_remove, count)

    @staticmethod
    def set_field_parameters(size, colors):
        if size == "small":
            width = 50
            height = 4
            colors = colors[0:4]
        if size == "middle 1":
            width = 100
            height = 6
            colors = colors[0:5]
        if size == "middle 2":
            width = 150
            height = 8
            colors = colors[1:6]
        if size == "big":
            width = 200
            height = 10
            colors = colors
        return width, height, colors

    def update(self):
        self.object.update()

    def draw(self):
        self.object.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.start_new_game[0] < pos[0] < \
                        self.start_new_game[0] + 155 and \
                        self.start_new_game[1] < pos[1] < \
                        self.start_new_game[1] + 50:
                    self.game_over = True
                for block in self.object.blocks:
                    if block.rect.x < pos[0] < \
                            27 + block.rect.x and \
                            block.rect.y < pos[1] < \
                            block.rect.y + 27:
                        score, color = self.object.remove((block.rect.x / 26,
                                                           block.rect.y / 26))
                        self.update_score(score)
                        self.update_color_information(self.background_image, color, score)

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))
            self.surface.blit(self.score.render,
                              self.score.rect)
            for information in self.information_about_colors:
                self.surface.blit(information.render,
                                  information.rect)
            self.surface.blit(
                pygame.font.Font('ARCADE.ttf', 25).render(
                    self.start_new_game[2], 1,
                    self.start_new_game[3]),
                (self.start_new_game[0], self.start_new_game[1]))
            self.handle_events()
            self.draw()
            self.update()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
