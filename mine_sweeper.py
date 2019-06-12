
import random
import pygame


class MineSweeper():
    def __init__(self, width=30, height=16, tile_size=25, proba=0.85):
        # proba: easy=0.90, medium=0.86, hard=0.83
        self.width = width
        self.height = height
        self.grid = [[[' ' if random.random() < proba else '*'][0] for x in range(self.width)] for x in range(self.height)]
        self.clickedGrid = [[False for x in range(self.width)] for x in range(self.height)]
        self.attributeValue()

        self.gameFailed = False
        self.marge = 15
        self.tileSize = tile_size
        self.tileMarge = 1.5
        self.windowWidth = self.width * self.tileSize + self.marge * 2
        self.windowHeight = self.height * self.tileSize + self.marge * 2
        self.windowSize = (self.windowWidth, self.windowHeight)
        self.window = pygame.display.set_mode(self.windowSize, 0, 32)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.arialFont = pygame.font.SysFont('Arial Black', 20)

        self.backgroundColor = (180, 180, 180)
        self.rectangleBackgroundColor = (70, 70, 70)
        self.hiddenTileColor = (120, 120, 120)
        self.emptyTileColor = (220, 220, 220)
        self.textColor = [(0, 51, 153),
                          (0, 51, 0),
                          (128, 0, 0),
                          (0, 0, 153),
                          (153, 0, 0),
                          (20, 20, 20),
                          (20, 20, 20),
                          (20, 20, 20)]
        self.bombColor = (10, 10, 10)

    def game_loop(self):
        pygame.init()
        self.init_display()
        while True:
            pygame.display.update()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = int((pos[1] - self.marge) / self.tileSize)
                    y = int((pos[0] - self.marge) / self.tileSize)
                    if self.gameFailed:
                        self.__init__()
                        self.game_loop()
                    if event.button == 1:
                        if self.marge < pos[0] < self.windowWidth - self.marge and self.marge < pos[1] < self.windowHeight - self.marge:
                            self.click_register(x, y)
                    elif event.button == 3:
                        self.right_click_register(x, y)
                    if self.gameFailed is False:
                        self.display_tiles()

    def init_display(self):
        self.display_background()
        self.display_tiles()

    def display_background(self):
        self.window.fill(self.backgroundColor)
        self.window.fill(
            self.rectangleBackgroundColor,
            pygame.Rect((
            (self.marge - self.tileMarge, self.marge - self.tileMarge),
            (self.windowWidth - self.marge * 2 + self.tileMarge * 2, self.windowHeight - self.marge * 2 + self.tileMarge * 2)
        )))

    def display_tiles(self):
        for x in range(self.width):
            for y in range(self.height):
                self.display_one_tile(x, y)

    def display_one_tile(self, x, y):
        self.window.fill(
            [self.emptyTileColor if self.clickedGrid[y][x] is True else self.hiddenTileColor][0],
            pygame.Rect((
                (self.marge + self.tileSize * x + self.tileMarge, self.marge + self.tileSize * y + self.tileMarge),
                (self.tileSize - self.tileMarge * 2, self.tileSize - self.tileMarge * 2)
            )))

        if self.clickedGrid[y][x] is True:
            if type(self.grid[y][x]) is int:
                self.window.blit(self.arialFont.render(str(self.grid[y][x]), False,
                    self.textColor[self.grid[y][x] - 1]),
                    (self.marge + self.tileSize * x + self.tileMarge + self.tileSize * 5/30,
                     self.marge + self.tileSize * y + self.tileMarge - self.tileSize * 5/30)
                )

        elif self.clickedGrid[y][x] == "F":
            self.display_flag(x, y)

    def display_flag(self, x, y):
        self.window.fill(
            (200, 20, 20),
            pygame.Rect((
                (self.marge + self.tileSize * x + self.tileMarge + (self.tileSize - self.tileMarge * 2)/4,
                 self.marge + self.tileSize * y + self.tileMarge + (self.tileSize - self.tileMarge * 2)/4),
                ((self.tileSize - self.tileMarge * 2)/2, (self.tileSize - self.tileMarge * 2)/2)
            )))

    def click_register(self, x, y):
        if self.clickedGrid[x][y] is False:
            self.clickedGrid[x][y] = True
            if self.grid[x][y] == '*':
                self.gameFailed = True
                self.show_bombs()
            elif self.grid[x][y] == ' ':
                self.discover_tiles(x, y)

    def right_click_register(self, x, y):
        if self.clickedGrid[x][y] == 'F':
            self.clickedGrid[x][y] = False
        elif self.clickedGrid[x][y] is False:
            self.clickedGrid[x][y] = 'F'

    def discover_tiles(self, x, y):
        for n in range(-1, 2):
            for m in range(-1, 2):
                u = x + n
                v = y + m
                if 0 <= u <= (self.height - 1) and 0 <= v <= (self.width - 1):
                    if self.grid[u][v] == ' ' or type(self.grid[u][v]) is int:
                        self.click_register(u, v)

    def show_bombs(self):
        # remember flags
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x] == '*':
                    self.window.fill(
                        (10, 10, 10),
                        pygame.Rect((
                            (self.marge + self.tileSize * x + self.tileMarge,
                             self.marge + self.tileSize * y + self.tileMarge),
                            (self.tileSize - self.tileMarge * 2, self.tileSize - self.tileMarge * 2)
                        )))
                    if self.clickedGrid[y][x] == 'F':
                        self.display_flag(x, y)

    def win_test(self):
        for x in range(self.width):
            for y in range(self.height):
                pass #TODO

    def display(self):
        for x in self.grid:
            for y in x:
                print(y, end=' ')
            print()

    def advancedDisplay(self):
        for x in self.grid:
            for y in x:
                if y == 1:
                    p = '\033[94m1\033[0m'
                elif y == 2:
                    p = '\033[92m2\033[0m'
                elif y == 3:
                    p = '\033[91m3\033[0m'
                elif y == 4:
                    p = '\033[94m4\033[0m'
                elif y == 5:
                    p = '\033[92m5\033[0m'
                else:
                    p = y
                print(p, end=' ')
            print()

    def attributeValue(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y] != '*':
                    c = 0
                    for n in range(-1, 2):
                        for m in range(-1, 2):
                            u = x+n
                            v = y+m
                            if 0 <= u and u <= (self.height - 1) and 0 <= v and v <= (self.width - 1):
                                if self.grid[u][v] == '*':
                                    c += 1
                    if c > 0:
                        self.grid[x][y] = c
                    else:
                        self.grid[x][y] = ' '


MineSweeper().game_loop()
