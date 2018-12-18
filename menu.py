from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, \
    QWidget, QTableWidget, QTableWidgetItem, QLabel, QActionGroup, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon, QFont
from game import Game
import sys
from enum import Enum
from field_attributes.field import Field


class Color(Enum):
    CRIMSON = (220, 20, 60)
    MEDIUMBLUE = (0, 0, 205)
    DARKORANGE = (255, 140, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 128, 0)
    INDIANRED = (205, 92, 92)
    INDIGO = (75, 0, 130)


COLORS = [color for color in Color]


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.colors = COLORS
        self.qp = QPainter()
        self.init_game()
        self.size2handler = {}
        self.previous_size = "small"
        self.setMouseTracking(True)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Cubes')
        self.setWindowIcon(QIcon('icons/cube.png'))
        self.menu = self.menuBar()
        self.statusBar()
        self.file = self.menu.addMenu('&File')
        self.settings = self.menu.addMenu('&Settings')
        self.exit = QAction('Exit', self)
        self.table_of_records = QAction('Table of records', self)
        self.table_of_records.setStatusTip('Show table of records')
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')
        self.file.addAction(self.table_of_records)
        self.file.addAction(self.exit)
        self.init_settings()
        self.exit.triggered.connect(self.close)
        self.table_of_records.triggered.connect(self.show_table_of_records)

    def init_settings(self):
        self.sizes = QActionGroup(self)
        self.small = QAction('Small', self, checkable=True)
        self.small.setChecked(True)
        self.small.triggered.connect(lambda: self.set_size('small'))
        self.sizes.addAction(self.small)
        self.settings.addAction(self.small)
        self.size2handler['small'] = self.small
        self.middle1 = QAction('Middle 1', self, checkable=True)
        self.middle1.triggered.connect(lambda: self.set_size('middle1'))
        self.sizes.addAction(self.middle1)
        self.settings.addAction(self.middle1)
        self.size2handler['middle1'] = self.middle1
        self.middle2 = QAction('Middle 2', self, checkable=True)
        self.middle2.triggered.connect(lambda: self.set_size('middle2'))
        self.sizes.addAction(self.middle2)
        self.settings.addAction(self.middle2)
        self.size2handler['middle2'] = self.middle2
        self.big = QAction('Big', self, checkable=True)
        self.big.triggered.connect(lambda: self.set_size('big'))
        self.sizes.addAction(self.big)
        self.settings.addAction(self.big)
        self.size2handler['big'] = self.big

        self.small.setStatusTip('A small field. Has 10x10 size and 4 colors')
        self.middle1.setStatusTip('A middle field. '
                                  'Has 14x14 size and 5 colors')
        self.middle2.setStatusTip('A middle field. '
                                  'Has 14x14 size and 6 colors')
        self.big.setStatusTip('A big field. Has 25x25 size and 7 colors')

    def set_size(self, size):
        if self.game.total_score != 0:
            if not self.game.exit():
                if self.previous_size != size:
                    self.size2handler[self.previous_size].setChecked(True)
                    self.size2handler[size].setChecked(False)
                return
        self.size2handler[size].setChecked(True)
        self.init_game(size)
        self.previous_size = size

    def closeEvent(self, event):
        self.game.exit()
        event.accept()

    def init_game(self, size='small'):
        self.game = Game(self.colors, size)
        self.setCentralWidget(self.game)

    def show_table_of_records(self):
        w = QWidget(self, Qt.Window)
        w.setWindowModality(Qt.WindowModal)
        w.setFixedSize(300, 200)
        w.setWindowTitle('Table of records')
        w.setWindowIcon(QIcon('icons/trophy.png'))
        w.move(self.geometry().center() - w.rect().center() - QPoint(0, 30))
        table = QTableWidget(self)
        vbox = QVBoxLayout()
        table.setColumnCount(4)
        table.setRowCount(10)
        sizes = ["small", "middle1", "middle2", "big"]
        table.setHorizontalHeaderLabels(sizes)
        with open('texts/best_results.txt') as f:
            best_results = eval(f.read())
        for size in best_results:
            for item in best_results[size]:
                row = best_results[size].index(item)
                column = sizes.index(size)
                item = item[0], str(item[1])
                table.setItem(row, column, QTableWidgetItem(', '.join(item)))
        vbox.addWidget(table)
        vbox.addStretch(1)
        w.setLayout(vbox)
        w.show()

    def paintEvent(self, QPaintEvent):
        self.qp.begin(self)
        self.draw_rectangles(QPaintEvent)
        self.drawText(QPaintEvent)
        self.qp.end()

    def drawText(self, QPaintEvent):
        x, y = self.game.width * 22 + 10, 40
        self.qp.setPen(QColor(0, 0, 0))
        self.qp.setFont(QFont('fonts/ARCADE.ttf', 15))
        self.qp.drawText(x, y, "Score: {}".format(self.game.total_score))
        self.qp.setFont(QFont('fonts/ARCADE.ttf', 10))
        for i in self.game.information_about_colors:
            y = y + 25
            self.qp.drawText(x, y, i)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            pos = event.pos().x(), event.pos().y()
            for (x, y) in self.game.object.blocks2coordinates:
                if x * 22 < pos[0] < 23 + x * 22 and \
                        y * 22 < pos[1] < y * 22 + 23:
                    score, color, is_exit = self.game.object.remove((x, y))
                    self.game.information_about_colors = \
                        self.game.set_information_about_colors(color, score)
                    self.game.update_score(score)
                    if is_exit:
                        self.game.exit()
        self.update()

    def draw_rectangles(self, QPaintEvent):
        for (x, y) in self.game.object.blocks2coordinates:
            color = self.game.object.blocks2coordinates[(x, y)][0].color
            self.qp.setPen(QColor(color[0], color[1], color[2]))
            self.qp.setBrush(QColor(color[0], color[1], color[2]))
            self.qp.drawRect(x * 22, y * 22, 20, 20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Menu()
    myapp.show()
    sys.exit(app.exec_())
