from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, \
    QInputDialog
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QBasicTimer
from accessory_files.score import Score
from field_attributes.field import Field


class Game(QWidget):
    def __init__(self, colors, width, height):
        super().__init__()

        self.colors = colors
        self.width = width
        self.height = height
        self.game_over = False
        self.object = Field(self.colors, self.width, self.height)
        self.total_score = 0
        self.isWaitingAfterLine = False
        self.table_of_records_file = "texts/table_of_records.txt"
        self.init_ui()
        self.information_about_colors = self.set_information_about_colors()
        self.table_of_records = self.set_table_of_records()

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
        table_of_records = {}
        with open(self.table_of_records_file) as table:
            for text in table.readlines():
                if text.find(":") > 0:
                    user, records = text.split(":")
                    table_of_records[user] = [int(i) for i in
                                              records.split(',')]
                else:
                    break
        return table_of_records

    def write_table(self):
        with open(self.table_of_records_file, 'w') as table_text:
            table_text.write('\n'.join('{}: {}'.format(user,
                                                       ', '.join(map(str,
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

    def update_score(self, score):
        self.total_score += score

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.button_quit = QPushButton('New game', self)
        self.button_quit.setFont(QFont('fonts/ARCADE.ttf', 15))
        x, y = self.width * 22 + 5, self.height * 22 - 40
        self.button_quit.setFixedWidth(115)
        self.button_quit.setFixedHeight(40)
        self.button_quit.adjustSize()
        self.button_quit.move(x, y)

        self.button_quit.clicked.connect(self.exit)

        self.repaint()

    def exit(self):
        le = QLineEdit(self)
        le.move(130, 22)
        text, ok = QInputDialog.getText(self, 'Game is over',
                                        'Enter your name:')
        if not ok:
            return False
        if ok:
            le.setText(str(text))
            if self.total_score != 0:
                self.update_table(text)
            self.new_game()
            return True

    def update_table(self, current_user):
        if current_user in self.table_of_records:
            self.table_of_records[current_user].append(self.total_score)
        else:
            self.table_of_records[current_user] = [self.total_score]
        self.table_of_records[current_user].sort(reverse=True)
        self.write_table()

    def new_game(self):
        self.total_score = 0
        self.object = Field(self.colors, self.width, self.height)
        self.information_about_colors = self.set_information_about_colors()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            pos = event.pos().x(), event.pos().y()
            for (x, y) in self.object.blocks2coordinates:
                if x * 22 < pos[0] < 23 + x * 22 and \
                        y * 22 < pos[1] < y * 22 + 23:
                    score, color, is_exit = self.object.remove((x, y))
                    self.information_about_colors = \
                        self.set_information_about_colors(color, score)
                    self.update_score(score)
                    self.init_ui()
                    if is_exit:
                        self.exit()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_rectangles(qp)
        self.drawText(qp)
        qp.end()

    def drawText(self, qp):
        x, y = self.width * 22 + 10, 30
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('fonts/ARCADE.ttf', 15))
        qp.drawText(x, y, "Score: {}".format(self.total_score))
        qp.setFont(QFont('fonts/ARCADE.ttf', 10))
        for i in self.information_about_colors:
            y = y + 25
            qp.drawText(x, y, i)

    def draw_rectangles(self, qp):
        for (x, y) in self.object.blocks2coordinates:
            color = self.object.blocks2coordinates[(x, y)][0].color
            qp.setPen(QColor(color[0], color[1], color[2]))
            qp.setBrush(QColor(color[0], color[1], color[2]))
            qp.drawRect(x * 22, y * 22, 20, 20)






