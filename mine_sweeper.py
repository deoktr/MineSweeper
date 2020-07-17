#
# Remake of the classic Minesweeper game
#

import datetime
import random
import pygame


class MineSweeper:
    """
    Classic MineSweeper remake
    """

    def __init__(self, width=30, height=16, bomb_count=99):
        self.width = width
        self.height = height
        self.bomb_count = bomb_count

        # ALGORITHM
        self.grid = None
        self.clicked_grid = [
            [False for x in range(self.width)] for x in range(self.height)
        ]
        self.first_click = True
        self.game_failed = False
        self.game_won = False
        self.bomb_left = self.bomb_count
        self.timer = 0
        self.start_time = None

        # UI/PYGAME
        self.margin = 10
        self.top_bar = 32
        self.tile_size = 16
        self.border = 1
        self.face_size = 26
        self.window_width = self.width * self.tile_size + self.margin * 2
        self.window_height = (
            self.height * self.tile_size + self.margin * 3 + self.top_bar
        )
        self.window_size = (self.window_width, self.window_height)
        self.window = pygame.display.set_mode(self.window_size, 0, 32)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Minesweeper")
        self.image_folder = "img/"
        pygame.display.set_icon(pygame.image.load(self.image_folder + "ico.png"))

        # IMAGES
        self.undiscovered_tile = self.image_folder + "undiscovered_tile.png"
        self.discovered_tile = self.image_folder + "discovered_tile.png"
        self.flag = self.image_folder + "flag.png"
        self.bomb = self.image_folder + "bomb.png"
        self.flaged_bomb = self.image_folder + "flaged_bomb.png"
        self.exploded_bomb = self.image_folder + "bomb_exploded.png"
        self.question = self.image_folder + "question.png"
        self.background = self.image_folder + "background.png"
        # tile numbers
        self.number_image_folder = self.image_folder + "tiles/"
        self.number = [0 for x in range(11)]
        for x in range(len(self.number)):
            self.number[x] = self.number_image_folder + str(x) + ".png"
        # face images
        self.face_image_folder = self.image_folder + "faces/"
        self.face_happy = self.face_image_folder + "happy.png"
        self.face_death = self.face_image_folder + "death.png"
        self.face_cool = self.face_image_folder + "cool.png"
        # timer/flag counter images
        self.counter_image_folder = self.image_folder + "counter/"
        self.counter = [0 for x in range(11)]
        for x in range(len(self.counter)):
            self.counter[x] = self.counter_image_folder + str(x) + ".png"

        # COLORS
        self.background_color = (180, 180, 180)

    def game_loop(self):
        """
        Game loop with different actions based on user input type
        (right-left click) and click position (top-bar/grid)
        """
        pygame.init()
        self.__init_display()
        while True:
            pygame.display.update()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__mouse_action(event)
            self.__update_timer()

    def __mouse_action(self, event):
        """
        When a click is registered on the window
        """
        pos = pygame.mouse.get_pos()

        # if the click is on the grid
        if (
            self.margin < pos[0] < self.window_width - self.margin
            and self.margin * 2 + self.top_bar
            < pos[1]
            < self.window_height - self.margin
            and self.game_failed is False
            and self.game_won is False
        ):
            self.__grid_click(event.button, pos)

        # if the click is on the face
        elif (
            self.window_width / 2 - self.face_size / 2
            < pos[0]
            < self.window_width / 2 - self.face_size / 2 + self.face_size
            and self.margin + self.top_bar / 2 - self.face_size / 2
            < pos[1]
            < self.margin + self.top_bar / 2 - self.face_size / 2 + self.face_size
        ):
            self.__face_click()

        self.__display_top_bar()

    def __grid_click(self, button, pos):
        """
        When a click is registered on the grid
        """
        x = int((pos[1] - self.margin * 2 - self.top_bar) / self.tile_size)
        y = int((pos[0] - self.margin) / self.tile_size)

        # left click
        if button == 1:
            self.__click_register(x, y)
            if self.game_failed is False:
                self.__display_tiles()

        # right click
        elif button == 3:
            self.__right_click_register(x, y)

        self.__win_test()

    def __face_click(self):
        """
        When a click is registered on the face restart the game
        """
        self.__init__(
            width=self.width, height=self.height, bomb_count=self.bomb_count,
        )
        self.game_loop()

    def __init_display(self):
        """
        Initialize the display by updating background, tiles and top bar
        """
        self.__display_background()
        self.__display_tiles()
        self.__display_top_bar()

    def __display_background(self):
        """
        Update the background image
        """
        self.window.blit(pygame.image.load(self.background), (0, 0))

    def display_face(self):
        """
        Update the face on the top bar
        """
        if self.game_failed:
            face = self.face_death
        elif self.game_won:
            face = self.face_cool
        else:
            face = self.face_happy

        self.window.blit(
            pygame.image.load(face),
            (
                self.window_width / 2 - self.face_size / 2,
                self.margin + self.top_bar / 2 - self.face_size / 2,
            ),
        )

    def __display_bomb_counter(self):
        """
        Update the bomb counter
        """
        count = "000" + str(self.bomb_left)
        for x in range(3):
            number = count[-(3 - x)]
            if number == "-":
                number = 10
            self.__display_counter_digit(
                self.margin + 6 + 13 * x, self.margin + 4, number
            )

    def __display_timer_counter(self):
        """
        Update the timer displayed
        """
        count = "000" + str(self.timer)
        for x in range(3):
            self.__display_counter_digit(
                self.window_width - (self.margin + 6 + 13 * (3 - x)),
                self.margin + 4,
                count[-(3 - x)],
            )

    def __display_counter_digit(self, x, y, digit):
        """
        Update a single digit of either the bomb counter or the timer
        """
        self.window.blit(pygame.image.load(self.counter[int(digit)]), (x, y))

    def __display_top_bar(self):
        """
        Update the top bar, with timer, bomb counter and face
        """
        # reset the top bar
        self.window.fill(
            self.background_color,
            pygame.Rect(
                (
                    (self.margin, self.margin),
                    (self.window_width - self.margin * 2, self.top_bar),
                )
            ),
        )

        self.display_face()
        self.__display_bomb_counter()
        self.__display_timer_counter()

    def __update_timer(self):
        """
        Update the timer displayed to the player
        """
        if (
            self.start_time is not None
            and self.game_failed is False
            and self.game_won is False
        ):
            self.timer = int(
                (datetime.datetime.now() - self.start_time).total_seconds()
            )
        self.__display_timer_counter()

    def __tile_position(self, x, y):
        """
        convert a grid position into gui position of a tile
        """
        gui_x = self.margin + self.tile_size * x
        gui_y = self.margin * 2 + self.tile_size * y + self.top_bar
        return gui_x, gui_y

    def __display_tiles(self):
        """
        Update the display of every tiles on the grid
        """
        for x in range(self.width):
            for y in range(self.height):
                self.__display_one_tile(x, y)

    def __display_one_tile(self, x, y):
        """
        Update the display of a single tile on the grid
        """
        if self.clicked_grid[y][x] is True:
            if isinstance(self.grid[y][x], int):
                # number tile
                self.window.blit(
                    pygame.image.load(self.number[self.grid[y][x]]),
                    self.__tile_position(x, y),
                )

            else:
                # empty tile
                self.window.blit(
                    pygame.image.load(self.discovered_tile), self.__tile_position(x, y)
                )

        elif self.clicked_grid[y][x] == "F":
            # flagged tile
            self.window.blit(pygame.image.load(self.flag), self.__tile_position(x, y))

        elif self.clicked_grid[y][x] == "?":
            # question tile
            self.window.blit(
                pygame.image.load(self.question), self.__tile_position(x, y)
            )

        else:
            # undiscovered tile
            self.window.blit(
                pygame.image.load(self.undiscovered_tile), self.__tile_position(x, y)
            )

    def __show_bombs(self, exploded_x, exploded_y):
        """
        At the end of the game every bombs are shown to the player
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x] == "*":
                    if self.clicked_grid[y][x] == "F" or self.clicked_grid[y][x] == "?":
                        self.window.blit(
                            pygame.image.load(self.flaged_bomb),
                            self.__tile_position(x, y),
                        )
                    else:
                        self.window.blit(
                            pygame.image.load(self.bomb), self.__tile_position(x, y)
                        )

        self.window.blit(
            pygame.image.load(self.exploded_bomb),
            self.__tile_position(exploded_y, exploded_x),
        )

    def __click_register(self, x, y):
        """
        When a user left click on the tile at position x, y
        """
        # Bombs are placed after the first click, preventing the
        # player from clicking on a bomb at first click
        if self.first_click:
            self.first_click = False
            self.__generate_grid()
            while self.grid[x][y] != " ":
                self.__generate_grid()
            self.start_time = datetime.datetime.now()

        if self.clicked_grid[x][y] is False:
            self.clicked_grid[x][y] = True
            if self.grid[x][y] == "*":
                self.game_failed = True
                self.__show_bombs(x, y)
            elif self.grid[x][y] == " ":
                self.__discover_tiles(x, y)

    def __right_click_register(self, x, y):
        """
        When a user right click on the tile at position x, y
        """
        if self.clicked_grid[x][y] == "F":
            self.clicked_grid[x][y] = "?"
            self.bomb_left += 1
        elif self.clicked_grid[x][y] == "?":
            self.clicked_grid[x][y] = False
        elif self.clicked_grid[x][y] is False:
            self.clicked_grid[x][y] = "F"
            self.bomb_left -= 1
        self.__display_one_tile(y, x)

    def __discover_tiles(self, x, y):
        """
        Will pass on all 8 adjacent tiles and
        if they are either number or empty it will be recursive
        """
        for n in range(-1, 2):
            for m in range(-1, 2):
                u = x + n
                v = y + m
                if 0 <= u <= (self.height - 1) and 0 <= v <= (self.width - 1):
                    if self.grid[u][v] == " " or isinstance(self.grid[u][v], int):
                        self.__click_register(u, v)

    def __win_test(self):
        """
        Test if player has won the game or not
        and update self.game_won
        """
        if self.grid is not None:
            for x in range(self.width):
                for y in range(self.height):
                    if (
                        (self.grid[y][x] == "*" and self.clicked_grid[y][x] != "F")
                        or (self.clicked_grid[y][x] == "F" and self.grid[y][x] != "*")
                        or (self.clicked_grid[y][x] is False and self.grid[y][x] != "*")
                    ):
                        return
            self.game_won = True

    def __generate_grid(self):
        """
        Generate a random grid filled with bomb and with numbers
        """
        self.grid = [[" " for x in range(self.width)] for x in range(self.height)]
        self.__place_bombs()
        self.__attribute_value()

    def __place_bombs(self):
        """
        Randomly place bombs on the grid
        """
        bomb_count = 0
        while bomb_count != self.bomb_count:
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if self.grid[x][y] != "*":
                self.grid[x][y] = "*"
                bomb_count += 1

    def __attribute_value(self):
        """
        Place numbers on the grid based on the number of bomb in
        the 8 adjacents tiles
        """
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y] != "*":
                    c = 0
                    for n in range(-1, 2):
                        for m in range(-1, 2):
                            u = x + n
                            v = y + m
                            if (
                                0 <= u
                                and u <= (self.height - 1)
                                and 0 <= v
                                and v <= (self.width - 1)
                            ):
                                if self.grid[u][v] == "*":
                                    c += 1
                    if c > 0:
                        self.grid[x][y] = c
                    else:
                        self.grid[x][y] = " "


if __name__ == "__main__":
    session = MineSweeper()
    session.game_loop()
