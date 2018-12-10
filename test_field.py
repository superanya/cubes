import unittest
import sys
from menu import Color
from field_attributes.field import Field

COLORS = [color for color in Color]
COLORS_VALUES = [color.value for color in Color]
field = '(220, 20, 60) (220, 20, 60) (0, 0, 205)\n' \
        '(220, 20, 60) (255, 140, 0) (0, 0, 205)\n' \
        '(220, 20, 60) (0, 0, 205) (255, 140, 0)\n'

FIELD = Field(COLORS, 3, 3, [[(220, 20, 60), (220, 20, 60), (0, 0, 205)],
                             [(220, 20, 60), (255, 140, 0), (0, 0, 205)],
                             [(220, 20, 60), (0, 0, 205), (255, 140, 0)]])
TEST = Field(COLORS, 3, 3)


class TestField(unittest.TestCase):
    def test_generate_random_field(self):
        for i in range(TEST.width):
            for j in range(TEST.height):
                self.assertTrue(TEST.blocks2coordinates[(i, j)][0].color
                                in COLORS_VALUES)

    def test_make_field(self):
        self.assertEqual(field, FIELD.__str__())

    def test_set_block2coordinates(self):
        self.assertEqual((220, 20, 60),
                         FIELD.blocks2coordinates[(0, 0)][0].color)

    def test_get_blocks_remove(self):
        neighbours = FIELD.blocks2coordinates[(0, 0)][1]
        block = FIELD.blocks2coordinates[(0, 0)][0]
        blocks_remove = [block]
        self.assertEqual([FIELD.blocks2coordinates[(0, 0)][0],
                         FIELD.blocks2coordinates[(0, 1)][0],
                         FIELD.blocks2coordinates[(0, 2)][0]],
                         FIELD.get_blocks_remove(neighbours, block,
                                                 blocks_remove))

    def test_set_neighbours(self):
        neighbours = FIELD.blocks2coordinates[(0, 0)][1]
        self.assertEqual([FIELD.blocks2coordinates[(0, 0)][0],
                          FIELD.blocks2coordinates[(1, 0)][0],
                          FIELD.blocks2coordinates[(0, 1)][0]],
                         [i[0] for i in neighbours])

    def test_get_blocks_remove(self):
        block = FIELD.blocks2coordinates[(0, 0)]
        blocks_remove = [block[0]]
        blocks_remove = FIELD.get_blocks_remove(block[1],
                                                block[0],
                                                blocks_remove)
        self.assertEqual([FIELD.blocks2coordinates[(0, 0)][0],
                          FIELD.blocks2coordinates[(1, 0)][0],
                          FIELD.blocks2coordinates[(2, 0)][0],
                          FIELD.blocks2coordinates[(0, 1)][0]],
                         blocks_remove)

    def test_remove_start(self):
        field_remove = Field(COLORS, 3, 3, [[(220, 20, 60),
                                             (220, 20, 60),
                                             (0, 0, 205)],
                                            [(220, 20, 60),
                                             (255, 140, 0),
                                             (0, 0, 205)],
                                            [(220, 20, 60), (0, 0, 205),
                                             (255, 140, 0)]])
        field_remove.remove((0, 0))
        new_field = '  (0, 0, 205)\n' \
                    ' (255, 140, 0) (0, 0, 205)\n' \
                    ' (0, 0, 205) (255, 140, 0)\n'
        self.assertEqual(new_field, field_remove.__str__())

    def test_remove_middle(self):
        field_remove = Field(COLORS, 3, 3, [[(220, 20, 60),
                                             (220, 20, 60),
                                             (0, 0, 205)],
                                            [(220, 20, 60),
                                             (255, 140, 0),
                                             (0, 0, 205)],
                                            [(220, 20, 60), (0, 0, 205),
                                             (255, 140, 0)]])
        field_remove.remove((0, 1))
        new_field = '  (0, 0, 205)\n' \
                    ' (255, 140, 0) (0, 0, 205)\n' \
                    ' (0, 0, 205) (255, 140, 0)\n'
        self.assertEqual(new_field, field_remove.__str__())

    def test_remove_end(self):
        field_remove = Field(COLORS, 3, 3, [[(220, 20, 60),
                                             (220, 20, 60),
                                             (0, 0, 205)],
                                            [(220, 20, 60),
                                             (255, 140, 0),
                                             (0, 0, 205)],
                                            [(220, 20, 60), (0, 0, 205),
                                             (255, 140, 0)]])
        field_remove.remove((2, 0))
        new_field = '  (0, 0, 205)\n' \
                    ' (255, 140, 0) (0, 0, 205)\n' \
                    ' (0, 0, 205) (255, 140, 0)\n'
        self.assertEqual(new_field, field_remove.__str__())

    def test_situation_without_remove(self):
        FIELD.remove((2, 2))
        self.assertEqual([[(220, 20, 60),
                           (220, 20, 60),
                           (0, 0, 205)],
                          [(220, 20, 60),
                           (255, 140, 0), (0, 0, 205)],
                          [(220, 20, 60), (0, 0, 205),
                           (255, 140, 0)]], FIELD.field)

    def test_is_exit(self):
        field = Field(COLORS, 1, 1, [[(220, 20, 60)], [(0, 0, 205)]])
        self.assertTrue(field.is_exit())


if __name__ == '__main__':
    unittest.main()
