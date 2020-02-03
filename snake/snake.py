import numpy as np
import time
import random
from IPython.display import clear_output


class Snake:
    """ Snake Game

    :property ticks: the current ticks
    :property player: the player that determines the next move
    :property dimx: x size of field
    :property dimy: y size of field
    :property direction: the direction can have 4 values:
        1 -> left
        2 -> up
        3 -> right
        4 -> down
    :property snake: the coordinates of the snake parts
    :property snake_max: max length of the snake
    :property food: the coordinates of the food
    :property x_map: maps a move/direction to the changes made to the x coordinate
                     (2 = up -> x does not change)
    :property y_map: maps a move/direction to the changes made to the y coordinate
                     (2 = up -> y decreases by 1)
    """

    def __init__(self, player, dim=(20, 10), move_at_ticks=30, verbose=True):
        """ Initializes the game state.
        """
        self.ticks = 0
        self.move_at_ticks = move_at_ticks
        self.player = player
        self.dimx, self.dimy = dim
        self.direction = 2
        self.snake = [(self.dimy // 2, self.dimx // 2)]
        self.snake_max = 1
        self.food = (5, 5)
        self.x_map = {1: -1, 2: 0, 3: 1, 4: 0}
        self.y_map = {1: 0, 2: -1, 3: 0, 4: 1}
        self.symbol_map = {0: " ", 5: "5", 9: "9"}
        self.verbose = verbose

    def start(self):
        """ The function which runs the game. Contains all the game logic.
        """

        # necessary to make the start of the game less awkward
        self._wait_for_player()

        # game loop
        while True:
            # advance game state by 1 ticks
            self.ticks += 1

            # get next move
            next_move = self.player.get_next_move(self)

            # only move every 10 ticks
            if self.ticks == self.move_at_ticks:
                # process next move
                if not self._process_move(next_move):
                    break

                # display updated state and reset ticks
                self._display_state()
                self.ticks = 0

            # sleep
            if self.verbose:
                time.sleep(0.005)

        # game is finished
        self._end_game()

    def _wait_for_player(self):
        """ Countdown before the game starts.
        """
        if not self.verbose:
            return

        self._display_state()
        time_to_wait = 2.5
        while time_to_wait > 0:
            print("Game starts in " + str(time_to_wait) + "s!", end="\r")
            time_to_wait -= 0.5
            time.sleep(0.5)

    def _process_move(self, move):
        """ Checks the validity of the given move and proceeds accordingly.

        :parameter move: next direction (if valid)

        :return game_not_finished: determines whether the game is finished or not
        """

        # check if move is valid
        if move == 1 or move == 2 or move == 3 or move == 4:
            self.direction = move

        # determine new position of snake head
        y, x = self.snake[-1]
        x += self.x_map[self.direction]
        y += self.y_map[self.direction]

        # check for colision with border
        if x < 1 or x == self.dimx - 1 or y < 1 or y == self.dimy - 1:
            return False

        # check for collision with food
        if (y, x) == self.food:
            self.snake_max += 1
            # determine possible positions for new food
            possible_food = []
            for i in [(y_, x_) for x_ in range(1, self.dimx - 1) for y_ in range(1, self.dimy - 1)]:
                if i not in self.snake:
                    possible_food.append(i)

            self.food = possible_food[random.randrange(len(possible_food))]

        # check for collision with snake body
        for i in self.snake:
            if i == (y, x):
                return False

        # set new position of head
        self.snake.append((y, x))
        if self.snake_max < len(self.snake):
            del self.snake[0]

        return True

    def _display_state(self):
        """ Clears the output and prints the current state of the game.
        """
        if not self.verbose:
            return

        # clear output and prepare an empty board
        clear_output(wait=True)
        field_to_draw = np.zeros((self.dimy, self.dimx), dtype=np.int8)

        # set snake in field
        for i in self.snake:
            field_to_draw[i] = 9

        # set food in field
        field_to_draw[self.food] = 5

        # draw field (including snake, food)
        game = ""
        for i in range(field_to_draw.shape[0]):
            for j in range(field_to_draw.shape[1]):

                # border
                if j == 0 or j == self.dimx - 1:
                    game = game + "|"
                    continue
                elif i == 0 or i == self.dimy - 1:
                    game = game + "-"
                    continue

                # snake, food and empty cells
                game = game + self.symbol_map[field_to_draw[i, j]]

            game = game + "\n"

        # only a single print to display the whole field
        print(game)

    def _end_game(self):
        if self.verbose:
            print("You got " + str(self.snake_max - 1) + " points!")
