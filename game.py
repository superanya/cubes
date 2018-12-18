from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, \
    QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QBasicTimer
from accessory_files.score import Score
from field_attributes.field import Field


class Game(QWidget):
    def __init__(self, colors, size):
        super().__init__()

        self.size = size
        self.width, self.height, self.colors = \
            self.init_field_size(colors, self.size)
        self.game_over = False
        self.object = Field(self.colors, self.width, self.height)
        self.total_score = 0
        self.isWaitingAfterLine = False
        self.table_of_records_file = "texts/best_results.txt"
        self.init_ui()
        self.information_about_colors = self.set_information_about_colors()
        self.table_of_records = self.set_table_of_records()
        self.best_results = {}

    @staticmethod
    def init_field_size(COLORS, size):
        if size == 'small':
            width = 10
            height = 10
            colors = COLORS[0:4]
        if size == 'middle1':
            width = 14
            height = 14
            colors = COLORS[0:5]
        if size == 'middle2':
            width = 14
            height = 14
            colors = COLORS[0:6]
        if size == 'big':
            width = 25
            height = 25
            colors = COLORS
        return width, height, colors

    def set_information_about_colors(self, color_remove=None, count=0):
        information_about_colors = []
        for color in self.colors:
            if color.value is color_remove:
                self.object.color2count[color.name] -= count
            text = '{}: {}'.format(color.name,
                                   self.object.color2count[color.name])
            information_about_colors.append(text)
        return information_about_colors

    def set_table_of_records(self):
        with open(self.table_of_records_file) as f:
            table_of_records = eval(f.read())
        return table_of_records

    def write_table(self):
        with open(self.table_of_records_file, 'w') as table_text:
            table_text.write(str(self.table_of_records))

    def update_score(self, score):
        self.total_score += score

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.button_quit = QPushButton('New game', self)
        self.button_quit.setFont(QFont('fonts/ARCADE.ttf', 15))
        x, y = self.width * 22 + 5, self.height * 22 - 60
        self.button_quit.setFixedWidth(140)
        self.button_quit.setFixedHeight(40)
        self.button_quit.adjustSize()
        self.button_quit.move(x, y)

        self.button_quit.clicked.connect(self.exit)

    def exit(self):
        if self.total_score != 0:
            le = QLineEdit(self)
            le.move(130, 22)
            text, ok = QInputDialog.getText(self, 'Game is over',
                                            'Enter your name:')
            if not ok:
                return False
            le.setText(str(text))
            self.update_table(text)
            self.new_game()
            return True

    def update_table(self, current_user):
        self.table_of_records[self.size].append((current_user,
                                                 self.total_score))
        self.write_best_results()
        self.write_table()

    def write_best_results(self):
            for size in self.table_of_records:
                self.table_of_records[size] = sorted(list(set(
                    self.table_of_records[size])),
                    key=lambda record: record[1])
                self.table_of_records[size].reverse()
                self.table_of_records[size] = \
                    self.table_of_records[size][0:10]

    def new_game(self):
        self.total_score = 0
        self.object = Field(self.colors, self.width, self.height)
        self.information_about_colors = self.set_information_about_colors()
