import unittest
from game import Game
from menu import Color

COLORS = [color for color in Color]

game = Game("Cubes", "images/back.jpg", 60, COLORS, "texts/test_table.TXT", 'big')


class TestGame(unittest.TestCase):
    def test_game_parameters(self):
        self.assertEqual(COLORS, game.colors)
        self.assertEqual(27, game.width)
        self.assertEqual(10, game.height)
        self.assertTrue(7, len(game.information_about_colors))

    def test_update_score(self):
        game.update_score(100)
        self.assertEqual(100, game.total_score)


if __name__ == '__main__':
    unittest.main()
