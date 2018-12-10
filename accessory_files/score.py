from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui


class Score:
    def __init__(self, score):
        self.score = score
        self.score = QLabel('Score:  {}'.format(score))
        self.score.setFont(QtGui.QFont('fonts/Arcade.ttf', 15, QtGui.QFont.Bold))
        self.score.adjustSize()

