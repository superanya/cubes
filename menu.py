from PyQt5.QtWidgets import QApplication, QMainWindow, QAction,\
                            QWidget, QLabel, QActionGroup, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon
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
        self.init_game()
        self.setMouseTracking(True)
        self.setGeometry(0, 0, 800, 600)
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
        self.small.setCheckable(True)
        self.sizes.addAction(self.small)
        self.settings.addAction(self.small)
        self.middle1 = QAction('Middle 1', self, checkable=True)
        self.middle1.triggered.connect(lambda: self.set_size('middle1'))
        self.middle1.setCheckable(True)
        self.sizes.addAction(self.middle1)
        self.settings.addAction(self.middle1)
        self.middle2 = QAction('Middle 2', self, checkable=True)
        self.middle2.triggered.connect(lambda: self.set_size('middle2'))
        self.middle2.setCheckable(True)
        self.sizes.addAction(self.middle2)
        self.settings.addAction(self.middle2)
        self.big = QAction('Big', self, checkable=True)
        self.big.triggered.connect(lambda: self.set_size('big'))
        self.big.setCheckable(True)
        self.sizes.addAction(self.big)
        self.settings.addAction(self.big)

        self.small.setStatusTip('A small field. Has 10x10 size and 4 colors')
        self.middle1.setStatusTip('A middle field. '
                                  'Has 14x14 size and 5 colors')
        self.middle2.setStatusTip('A middle field. '
                                  'Has 14x14 size and 6 colors')
        self.big.setStatusTip('A big field. Has 25x25 size and 7 colors')

    def set_size(self, size):
        if self.game.exit():
            self.init_game(size)

    def closeEvent(self, event):
        if self.game.exit():
            sys.exit()
        else:
            event.ignore()

    def init_game(self, size='small'):
        self.width, self.height, self.colors = self.init_field_size(size)
        self.game = Game(self.colors, self.width, self.height)
        self.setCentralWidget(self.game)

    def init_field_size(self, size):
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

    def paintEvent(self, e):
        self.game.paintEvent(e)

    def show_table_of_records(self):
        w = QWidget(self, Qt.Window)
        w.setWindowModality(Qt.WindowModal)
        w.resize(300, 200)
        w.setWindowTitle('Table of records')
        w.setWindowIcon(QIcon('icons/trophy.png'))
        w.move(self.geometry().center() - w.rect().center() - QPoint(0, 30))
        vbox = QVBoxLayout()
        with open('texts/table_of_records.txt') as f:
            for line in f.readlines():
                user_stats = QLabel(line)
                vbox.addWidget(user_stats)
        vbox.addStretch(1)
        w.setLayout(vbox)
        w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Menu()
    myapp.show()
    sys.exit(app.exec_())
