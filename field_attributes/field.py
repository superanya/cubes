import random
import pygame
from field_attributes.block import Block


class Field:
    def __init__(self, colors, width=-1, height=-1, field=None):
        self.width = width
        self.height = height
        self.colors = colors
        self.color2count = {}
        self.field = self.generate_random_field() if not field else field
        self.blocks = pygame.sprite.Group()
        self.blocks2coordinates = self.set_blocks2coordinates()

    def set_blocks2coordinates(self):
        blocks2coordinates = {}
        block2neighbours = {}
        for i in range(self.width):
            for j in range(self.height):
                color = self.field[i][j]
                if color is not None:
                    block = Block(i, j, color, 25, 25)
                    block.rect.x = i * 26
                    block.rect.y = j * 26
                    self.blocks.add(block)
                    blocks2coordinates[(i, j)] = (block, [])
                    block2neighbours[block] = []
        self.set_neighbours(blocks2coordinates)
        return blocks2coordinates

    @staticmethod
    def set_correct_neighbour(block_coordinates,
                              neighbour_coordinates, blocks2coordinates):
        if neighbour_coordinates in blocks2coordinates:
            blocks2coordinates[block_coordinates][1].append(
                blocks2coordinates[neighbour_coordinates])

    def set_neighbours(self, blocks2coordinates):
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in blocks2coordinates:
                    blocks2coordinates[(x, y)][1].append(
                        blocks2coordinates[(x, y)])
                    if x < self.width - 1:
                        self.set_correct_neighbour((x, y),
                                                   (x + 1, y),
                                                   blocks2coordinates)
                    if y < self.height - 1:
                        self.set_correct_neighbour((x, y),
                                                   (x, y + 1),
                                                   blocks2coordinates)
                    if x > 0:
                        self.set_correct_neighbour((x, y),
                                                   (x - 1, y),
                                                   blocks2coordinates)
                    if y > 0:
                        self.set_correct_neighbour((x, y),
                                                   (x, y - 1),
                                                   blocks2coordinates)
        return blocks2coordinates

    def get_blocks_remove(self, neighbours, block, blocks_remove):
        same_neighbours = list(filter(lambda x:
                                      x[0] not in blocks_remove and
                                      x[0].color == block.color,
                                      neighbours))
        if len(same_neighbours) != 0:
            for i in same_neighbours:
                blocks_remove.append(i[0])
                self.get_blocks_remove(i[1], i[0], blocks_remove)
        return blocks_remove

    def remove(self, block_coordinates):
        block = self.blocks2coordinates[block_coordinates][0]
        block_neighbours = self.blocks2coordinates[block_coordinates][1]
        blocks_remove = [block]
        blocks_remove = self.get_blocks_remove(block_neighbours,
                                               block, blocks_remove)
        if len(blocks_remove) > 1:
            for i in blocks_remove:
                block = self.blocks2coordinates[(i.coordinates[0],
                                                 i.coordinates[1])][0]
                self.blocks.remove(block)
                self.field[i.coordinates[0]][i.coordinates[1]] = None
        self.field = self.create_new_field(self.field)
        lists_to_remove = list(filter(lambda x: x == [], self.field))
        for i in lists_to_remove:
            self.field.remove(i)
        self.update()
        return len(blocks_remove) if len(blocks_remove) > 2 else 0, block.color

    def set_block_color(self):
        color = random.choice(self.colors)
        for i in self.colors:
            if color == i:
                if color.name in self.color2count:
                    self.color2count[color.name] += 1
                else:
                    self.color2count[color.name] = 1
        return color.value

    def update(self):
        width = 0
        for i in self.field:
            if len(i) > width:
                width = len(i)
        for i in self.field:
            while len(i) < width:
                i.append(None)
        self.width = len(self.field)
        self.height = width
        self.blocks = pygame.sprite.Group()
        self.blocks2coordinates = self.set_blocks2coordinates()
        return self.is_exit()

    def is_exit(self):
        for i in range(self.width):
            for j in range(self.height):
                if (i, j) in self.blocks2coordinates:
                    block = self.blocks2coordinates[(i, j)][0]
                    block_neighbours = self.blocks2coordinates[(i, j)][1]
                    blocks_remove = [block]
                    blocks_remove = self.get_blocks_remove(block_neighbours,
                                                           block, blocks_remove)
                if len(blocks_remove) > 1:
                    return False
        return True

    @staticmethod
    def create_new_field(field):
        new_field = []
        number = 0
        for i in field:
            new_field.append([])
            for j in i:
                if j is not None:
                    new_field[number].append(j)
            number += 1
        return new_field

    def generate_random_field(self):
        mas = []
        for i in range(self.width):
            mas.append([])
            for j in range(self.height):
                mas[i].append(self.set_block_color())
        return mas

    def __str__(self):
        field = ''
        for i in self.field:
            field += '{0}\n'.format(
                ' '.join(str(j) if j is not None else '' for j in i))
        return field

    def draw(self, surface):
        self.blocks.draw(surface)
