
import random
import pygame


class MineSweeper():
    def __init__(self, width=30, height=16, bombCount=99):
        self.width = width
        self.height = height
        self.bombCount = bombCount
        self.grid = [[' ' for x in range(self.width)] for x in range(self.height)]
        self.placeBombs()
        self.attributeValue()
        self.clickedGrid = [[False for x in range(self.width)] for x in range(self.height)]

        self.gameFailed = False
        self.gameWon = False
        self.marge = 10
        self.tileSize = 16
        self.tileMarge = 1
        self.windowWidth = self.width * self.tileSize + self.marge * 2
        self.windowHeight = self.height * self.tileSize + self.marge * 2
        self.windowSize = (self.windowWidth, self.windowHeight)
        self.window = pygame.display.set_mode(self.windowSize, 0, 32)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.arialFont = pygame.font.SysFont('Arial Black', 13)

        self.imageFolder = "img/"
        self.undiscoveredTile = self.imageFolder + "undiscovered_tile.png"
        self.discoveredTile = self.imageFolder + "discovered_tile.png"
        self.flag = self.imageFolder + "flag.png"
        self.bomb = self.imageFolder + "bomb.png"
        self.flagedBomb = self.imageFolder + "flaged_bomb.png"
        self.explodedBomb = self.imageFolder + "bomb_exploded.png"
        self.question = self.imageFolder + "question.png"
        self.backgroundColor = (180, 180, 180)
        self.rectangleBackgroundColor = (70, 70, 70)
        self.textColor = [(0, 0, 255),
                          (0, 123, 0),
                          (255, 0, 0),
                          (0, 0, 123),
                          (123, 0, 0),
                          (0, 123, 123),
                          (0, 0, 0),
                          (123, 123, 123)]
        
        self.endTextColor = (20, 20, 20)
        self.endRectangleColor = (220, 220, 220)
        self.endText = "you win!"

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
                    if self.gameFailed or self.gameWon:
                        self.__init__()
                        self.game_loop()
                    if event.button == 1:
                        if self.marge < pos[0] < self.windowWidth - self.marge and self.marge < pos[1] < self.windowHeight - self.marge:
                            self.click_register(x, y)
                    elif event.button == 3:
                        self.right_click_register(x, y)
                    if self.gameFailed is False:
                        self.display_tiles()
                    self.win_test()

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
        if self.clickedGrid[y][x] is True:
            self.window.blit(
                pygame.image.load(self.discoveredTile),
                (self.marge + self.tileSize * x,
                self.marge + self.tileSize * y)
            )
            if type(self.grid[y][x]) is int:
                text = self.arialFont.render(str(self.grid[y][x]), False,
                    self.textColor[self.grid[y][x] - 1])
                text_rect = text.get_rect(center=(
                    self.marge + self.tileSize * x + self.tileSize/2,
                    self.marge + self.tileSize * y + self.tileSize/2))
                self.window.blit(text, text_rect)
        elif self.clickedGrid[y][x] == "F":
            self.window.blit(
                pygame.image.load(self.flag),
                (self.marge + self.tileSize * x,
                self.marge + self.tileSize * y)
            )
        elif self.clickedGrid[y][x] == "?":
            self.window.blit(
                pygame.image.load(self.question),
                (self.marge + self.tileSize * x,
                self.marge + self.tileSize * y)
            )
        else:
            self.window.blit(
                pygame.image.load(self.undiscoveredTile),
                (self.marge + self.tileSize * x,
                self.marge + self.tileSize * y)
            )

    def click_register(self, x, y):
        if self.clickedGrid[x][y] is False:
            self.clickedGrid[x][y] = True
            if self.grid[x][y] == '*':
                self.gameFailed = True
                self.show_bombs(x, y)
            elif self.grid[x][y] == ' ':
                self.discover_tiles(x, y)

    def right_click_register(self, x, y):
        if self.clickedGrid[x][y] == 'F':
            self.clickedGrid[x][y] = '?'
        elif self.clickedGrid[x][y] == '?':
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

    def show_bombs(self, exploded_x, exploded_y):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x] == '*':
                    if self.clickedGrid[y][x] == 'F' or self.clickedGrid[y][x] == '?':
                        self.window.blit(
                            pygame.image.load(self.flagedBomb),
                            (self.marge + self.tileSize * x,
                            self.marge + self.tileSize * y)
                        )
                    else:
                        self.window.blit(
                            pygame.image.load(self.bomb),
                            (self.marge + self.tileSize * x,
                            self.marge + self.tileSize * y)
                        )

        self.window.blit(
            pygame.image.load(self.explodedBomb),
            (self.marge + self.tileSize * exploded_y,
            self.marge + self.tileSize * exploded_x)
        )

    def win_test(self):
        for x in range(self.width):
            for y in range(self.height):
                if (self.grid[y][x] == '*' and self.clickedGrid[y][x] != 'F') or \
                    (self.clickedGrid[y][x] == 'F' and self.grid[y][x] != '*') or \
                    (self.clickedGrid[y][x] is False and self.grid[y][x] != '*'):
                    return False
        self.gameWon = True

    def placeBombs(self):
        bombCount = 0
        while bombCount != self.bombCount:
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if self.grid[x][y] != '*':
                self.grid[x][y] = '*'
                bombCount += 1

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


if __name__ == "__main__":
    MineSweeper().game_loop()
