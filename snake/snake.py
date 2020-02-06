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
    :property symbol_map: maps numbers in numpy array field to strings for displaying
    :property verbose: determines whether output's printed on console
    :property max_steps_without_eating: determines how many steps can be made without eating food before the game ends
    :property current_steps: the number of current steps without eating food
    """

    def __init__(self, player, dim=(20, 10), move_at_ticks=30, verbose=True):
        """ Initializes the game state.
        """
        self.ticks = 0
        self.move_at_ticks = move_at_ticks
        self.player = player
        self.dim_x, self.dim_y = dim
        self.direction = 2
        self.snake = [(self.dim_y - 2, self.dim_x // 2)]
        self.snake_max = 1
        self.food = (5, 5)
        self.x_map = {1: -1, 2: 0, 3: 1, 4: 0}
        self.y_map = {1: 0, 2: -1, 3: 0, 4: 1}
        self.symbol_map = {0: " ", 5: "5", 9: "9"}
        self.verbose = verbose
        self.max_steps_without_eating = int(self.dim_x * self.dim_y)
        self.current_steps = 0

    def start(self):
        """ Main loop of the game.
        """
        self._wait_for_player()

        while True:
            self.ticks += 1

            next_move = self.player.get_next_move(self)
            if self.ticks == self.move_at_ticks:
                if not self._process_move(next_move):
                    break

                self._display_state()
                self.ticks = 0

            if self.verbose:
                time.sleep(0.005)

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
        self.current_steps += 1

        if move == 1 or move == 2 or move == 3 or move == 4:
            self.direction = move

        y, x = self.snake[-1]
        x += self.x_map[self.direction]
        y += self.y_map[self.direction]

        if not self._check_collisions((y, x)):
            return False

        self.snake.append((y, x))
        if self.snake_max < len(self.snake):
            del self.snake[0]

        if self.current_steps > self.max_steps_without_eating:
            return False

        return True

    def _check_collisions(self, next_position):
        """ Checks collisions and spawns new food if necessary.
        """
        y, x = next_position

        if x < 1 or x == self.dim_x - 1 or y < 1 or y == self.dim_y - 1:
            return False

        for i in self.snake:
            if i == (y, x):
                return False

        if (y, x) == self.food:
            self.snake_max += 1
            self.current_steps = 0
            possible_food = []
            for i in [(y_, x_) for x_ in range(1, self.dim_x - 1) for y_ in range(1, self.dim_y - 1)]:
                if i not in self.snake:
                    possible_food.append(i)

            self.food = possible_food[random.randrange(len(possible_food))]

        return True

    def _display_state(self):
        """ Clears the output and prints the current state of the game.
        """
        if not self.verbose:
            return

        clear_output(wait=True)
        field_to_draw = np.zeros((self.dim_y, self.dim_x), dtype=np.int8)

        for i in self.snake:
            field_to_draw[i] = 9

        field_to_draw[self.food] = 5

        game = "Points: {} ({}/{} steps)\n".format(self.snake_max-1, self.current_steps, self.max_steps_without_eating)
        for i in range(field_to_draw.shape[0]):
            for j in range(field_to_draw.shape[1]):

                if j == 0 or j == self.dim_x - 1:
                    game += "|"
                    continue
                elif i == 0 or i == self.dim_y - 1:
                    game += "-"
                    continue

                game += self.symbol_map[field_to_draw[i, j]]

            game += "\n"

        print(game)

    def _end_game(self):
        """ Finishes the game.
        """
        if self.verbose:
            print("You got " + str(self.snake_max - 1) + " points!")
