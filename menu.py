import sys
import pygame
from game import Game
from enum import Enum
pygame.init()


class Color(Enum):
    CRIMSON = (220, 20, 60)
    MEDIUMBLUE = (0, 0, 205)
    DARKORANGE = (255, 140, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 128, 0)
    INDIANRED = (205, 92, 92)
    INDIGO = (75, 0, 130)


COLORS = [color for color in Color]


class Menu:
    def __init__(self, back_image_filename, paragraphs):
        self.paragraphs = paragraphs
        self.background_image = \
            pygame.image.load(back_image_filename)
        self.surface = pygame.display.set_mode((700, 393))
        self.size = "small"
        self.paragraphs_settings = [[300, 150, 'Small',
                                     (250, 20, 147),
                                    (165, 42, 42), 0],
                                    [300, 190, 'Middle 1',
                                     (250, 20, 147),
                                     (139, 0, 139), 1],
                                    [300, 230, 'Middle 2',
                                     (250, 20, 147),
                                     (139, 0, 139), 2],
                                    [300, 270, 'Big',
                                     (250, 20, 147),
                                     (139, 0, 139), 3]]
        self.settings = Settings("images/arseniy-chebynkin-106.jpg",
                                 self.paragraphs_settings)

    def render(self, surface, font, num_paragraph):
        for i in self.paragraphs:
            if num_paragraph == i[5]:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
            else:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))

    def start(self):
        font_menu = pygame.font.Font('fonts/ARCADE.ttf', 25)
        paragraph = 0
        self.surface.blit(self.background_image, (0, 0))
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for i in self.paragraphs:
                if i[0] < mouse_pos[0] < i[0] + 155 and \
                        i[1] < mouse_pos[1] < i[1] + 50:
                    paragraph = i[5]
            self.render(self.surface, font_menu, paragraph)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.type == pygame.K_ESCAPE:
                        sys.exit()
                if e.type == pygame.K_UP:
                    if paragraph > 0:
                        paragraph -= 1
                if e.type == pygame.K_DOWN:
                    if paragraph < self.paragraphs.length - 1:
                        paragraph += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if paragraph == 0:
                        game = Game("Cubes", "images/back.jpg",
                                    60, COLORS,
                                    "texts/table_of_records.TXT", self.size)
                        game.run()
                        main()
                    if paragraph == 1:
                        previous_paragraph = self.settings.chosen_paragraph
                        self.settings.start()
                        self.size = self.settings.size

                        if previous_paragraph != \
                                self.settings.chosen_paragraph:
                            self.paragraphs_settings[previous_paragraph][4] = \
                                (139, 0, 139)
                        self.paragraphs_settings[
                            self.settings.chosen_paragraph][4] = \
                            (165, 42, 42)

                        self.settings.size = None
                        game = Game("Cubes", "images/back.jpg",
                                    60, COLORS,
                                    "texts/table_of_records.TXT",
                                    self.size)
                        game.run()
                        main()
                    if paragraph == 2:
                        sys.exit()
            pygame.display.flip()


class Settings:
    def __init__(self, back_image_filename, paragraphs):
        self.paragraphs = paragraphs
        self.background_image = \
            pygame.image.load(back_image_filename).convert()
        self.surface = pygame.display.set_mode((700, 393))
        self.size = None
        self.stop = False
        self.chosen_paragraph = 0

    def render(self, surface, font, num_paragraph):
        for i in self.paragraphs:
            if num_paragraph == i[5]:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
            else:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))

    def start(self):
        font_menu = pygame.font.Font('fonts/ARCADE.ttf', 25)
        paragraph = 0
        self.surface.blit(self.background_image, (0, 0))
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for i in self.paragraphs:
                if i[0] < mouse_pos[0] < i[0] + 155 and \
                        i[1] < mouse_pos[1] < i[1] + 50:
                    paragraph = i[5]
            self.render(self.surface, font_menu, paragraph)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.type == pygame.K_ESCAPE:
                        sys.exit()
                if e.type == pygame.K_UP:
                    if paragraph > 0:
                        paragraph -= 1
                if e.type == pygame.K_DOWN:
                    if paragraph < self.paragraphs.length - 1:
                        paragraph += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if paragraph == 0:
                        self.size = "small"
                    if paragraph == 1:
                        self.size = "middle 1"
                    if paragraph == 2:
                        self.size = "middle 2"
                    if paragraph == 3:
                        self.size = "big"
                    self.chosen_paragraph = paragraph
            if self.size is not None:
                break
            pygame.display.flip()


menu = Menu("images/arseniy-chebynkin-106.jpg", [[300, 150, 'Game',
                                                  (250, 20, 147),
                                                  (139, 0, 139), 0],
                                                 [300, 185, 'Settings',
                                                  (250, 20, 147),
                                                  (139, 0, 139), 1],
                                                 [300, 215, 'Leave',
                                                  (250, 20, 147),
                                                  (139, 0, 139), 2]])


def main():
    menu.start()


if __name__ == '__main__':
    main()
