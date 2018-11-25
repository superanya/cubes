import pygame
import sys
from field_attributes.field import Field
from accessory_files.score import Score
from accessory_files.information import Information
from accessory_files import pygame_textinput


class Game:
    def __init__(self,
                 caption,
                 back_image_filename,
                 frame_rate,
                 colors,
                 size='small'):
        self.background_image = \
            pygame.image.load(back_image_filename).convert()
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
        self.table_of_records = self.set_table_of_records()
        self.current_user = pygame_textinput.TextInput()

    @staticmethod
    def set_table_of_records():
        table_of_records = {}
        with open("texts/table_of_records.txt") as table:
            for text in table.readlines():
                if text.find(":") > 0:
                    user, records = text.split(":")
                    table_of_records[user] = [int(i) for i in records.split(',')]
                else:
                    break
        return table_of_records

    def write_table(self):
        with open("texts/table_of_records.txt", 'w') as table_text:
            table_text.write('\n'.join('{}: {}'.format(user, ', '.join(map(str,
                                                                           set(self.table_of_records[user][0:10]))))
                                       for user in self.table_of_records))

    def update_table(self):
        current_user = self.current_user.get_text()
        if current_user in self.table_of_records:
            self.table_of_records[current_user].append(self.total_score)
        else:
            self.table_of_records[current_user] = [self.total_score]
        self.table_of_records[current_user].sort(reverse=True)
        self.write_table()

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
            width = 28
            height = 4
            colors = colors[0:4]
        if size == "middle 1":
            width = 28
            height = 6
            colors = colors[0:5]
        if size == "middle 2":
            width = 28
            height = 8
            colors = colors[1:6]
        if size == "big":
            width = 28
            height = 10
            colors = colors
        return width, height, colors

    def update(self):
        return self.object.update()

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
                    self.exit()
                    self.update_table()
                for block in self.object.blocks:
                    if block.rect.x < pos[0] < \
                            27 + block.rect.x and \
                            block.rect.y < pos[1] < \
                            block.rect.y + 27:
                        score, color = self.object.remove((block.rect.x / 26,
                                                           block.rect.y / 26))
                        self.update_score(score)
                        self.update_color_information(self.background_image, color, score)

    def exit(self):
        exit_window_surface = pygame.display.set_mode((700, 393))
        font = pygame.font.Font("fonts/ARCADE.ttf", 40)
        exit_message = font.render('Game over. Please, enter your name: ', True, (0, 0, 0))
        while True:
            exit_window_surface.fill((225, 225, 225))
            exit_window_surface.blit(exit_message, (0, 10))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            current_user = self.current_user.update(events)
            exit_window_surface.blit(self.current_user.get_surface(), (0, 50))
            pygame.display.update()
            if current_user:
                self.game_over = True
                break

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))
            self.surface.blit(self.score.render,
                              self.score.rect)
            for information in self.information_about_colors:
                self.surface.blit(information.render,
                                  information.rect)
            self.surface.blit(
                pygame.font.Font('fonts/ARCADE.ttf', 25).render(
                    self.start_new_game[2], 1,
                    self.start_new_game[3]),
                (self.start_new_game[0], self.start_new_game[1]))
            self.handle_events()
            self.draw()
            is_exit = self.update()
            if is_exit:
                self.exit()
                self.update_table()
            pygame.display.update()
            self.clock.tick(self.frame_rate)
