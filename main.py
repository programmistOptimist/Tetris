import pygame

import random


def main():
    pygame.init()

    WINDOW_WIDTH = 400

    WINDOW_HEIGHT = 800

    BLOCK_DIMENSION = 20

    COLUMNS = WINDOW_WIDTH // BLOCK_DIMENSION

    ROWS = WINDOW_HEIGHT // BLOCK_DIMENSION

    BLACK = (0, 0, 0)  # Черный цвет

    WHITE = (255, 255, 255)  # Белый цвет

    GRAY = (128, 128, 128)  # Серый цвет

    RED = (255, 0, 0)  # Красный цвет

    GREEN = (0, 255, 0)  # Зеленый цвет

    BLUE = (0, 0, 255)  # Синий цвет

    CYAN = (0, 255, 255)  # Cyan (голубой)

    MAGENTA = (255, 0, 255)  # Пурпурный

    YELLOW = (255, 255, 0)  # Желтый цвет

    BEIGE = (245, 245, 220)  # Бежевый цвет

    COLOR_PALETTE = [RED, GREEN, CYAN, YELLOW, MAGENTA]

    SHAPE_TEMPLATES = [

        [[1, 1, 1, 1]],  # Фигура "I"

        [[1, 1, 1], [0, 1, 0]],  # Фигура "T"

        [[1, 1, 1], [1, 0, 0]],  # Фигура "L"

        [[1, 1, 1], [0, 0, 1]],  # Фигура "J"

        [[1, 1], [1, 1]],  # Фигура "O"

        [[0, 1, 1], [1, 1, 0]],  # Фигура "S"

        [[1, 1, 0], [0, 1, 1]]  # Фигура "Z"

    ]

    class Tetromino:

        def __init__(self, pos_x, pos_y, shape_matrix):
            self.x = pos_x

            self.y = pos_y

            self.shape = [

                shape_matrix,

                self.rotate_matrix(shape_matrix),

                self.rotate_matrix(self.rotate_matrix(shape_matrix)),

                self.rotate_matrix(self.rotate_matrix(self.rotate_matrix(shape_matrix)))

            ]

            self.color = random.choice(COLOR_PALETTE)

            self.rotation_state = 0

        def rotate(self):
            self.rotation_state = (self.rotation_state + 1) % len(self.shape)

        def get_imagine(self):
            return self.shape[self.rotation_state]

        def rotate_matrix(self, matrix):
            return [list(row) for row in zip(*matrix[::-1])]

    class TetrisGame:

        def __init__(self, screen):

            self.screen = screen

            self.grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]

            self.current_piece = self.generate_new_piece()

            self.next_piece = self.generate_new_piece()

            self.score = 0

            self.is_game_over = False

        def generate_new_piece(self):

            return Tetromino(COLUMNS // 2 - 2, 0, random.choice(SHAPE_TEMPLATES))

        def check_collision(self, offset_x=0, offset_y=0):

            for y, row in enumerate(self.current_piece.get_imagine()):

                for x, cell in enumerate(row):

                    if cell:

                        new_x = x + self.current_piece.x + offset_x

                        new_y = y + self.current_piece.y + offset_y

                        if (new_x < 0 or new_x >= COLUMNS or

                                new_y >= ROWS or

                                (new_y >= 0 and self.grid[new_y][new_x] != BLACK)):
                            return True

            return False

        def lock_piece(self):

            for y, row in enumerate(self.current_piece.get_imagine()):

                for x, cell in enumerate(row):

                    if cell:

                        grid_y = y + self.current_piece.y

                        grid_x = x + self.current_piece.x

                        if 0 <= grid_y < ROWS and 0 <= grid_x < COLUMNS:
                            self.grid[grid_y][grid_x] = self.current_piece.color

            self.clear_filled_lines()

            self.current_piece = self.next_piece

            self.next_piece = self.generate_new_piece()

            if self.check_collision():
                self.is_game_over = True

        def clear_filled_lines(self):

            lines_to_clear = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]

            for i in lines_to_clear:
                del self.grid[i]

                self.grid.insert(0, [BLACK for _ in range(COLUMNS)])

            self.score += len(lines_to_clear) * 100

        def move_piece(self, delta_x):

            if not self.check_collision(delta_x, 0):
                self.current_piece.x += delta_x

        def drop_piece(self):

            if not self.check_collision(0, 1):

                self.current_piece.y += 1

                return True

            else:

                self.lock_piece()

                return False

        def rotate_piece(self):

            self.current_piece.rotate()

            if self.check_collision():
                # Откат вращения при коллизии

                self.current_piece.rotate()

                self.current_piece.rotate()

                self.current_piece.rotate()

        def draw_grid(self):

            for y in range(ROWS):

                for x in range(COLUMNS):

                    pygame.draw.rect(self.screen, GRAY,

                                     (x * BLOCK_DIMENSION, y * BLOCK_DIMENSION,

                                      BLOCK_DIMENSION, BLOCK_DIMENSION), 1)

                    if self.grid[y][x] != BLACK:
                        pygame.draw.rect(self.screen, self.grid[y][x],

                                         (x * BLOCK_DIMENSION, y * BLOCK_DIMENSION,

                                          BLOCK_DIMENSION, BLOCK_DIMENSION))

        def draw_current_piece(self):

            for y, row in enumerate(self.current_piece.get_imagine()):

                for x, cell in enumerate(row):

                    if cell:
                        pygame.draw.rect(

                            self.screen,

                            self.current_piece.color,

                            (

                                (x + self.current_piece.x) * BLOCK_DIMENSION,

                                (y + self.current_piece.y) * BLOCK_DIMENSION,

                                BLOCK_DIMENSION,

                                BLOCK_DIMENSION

                            )

                        )

        def draw_next_piece(self):

            for y, row in enumerate(self.next_piece.get_imagine()):

                for x, cell in enumerate(row):

                    if cell:
                        pygame.draw.rect(

                            self.screen,

                            self.next_piece.color,

                            (

                                (x + COLUMNS + 1) * BLOCK_DIMENSION,

                                (y + 1) * BLOCK_DIMENSION,

                                BLOCK_DIMENSION,

                                BLOCK_DIMENSION

                            )

                        )

        def render(self):

            self.screen.fill(BLACK)

            self.draw_grid()

            self.draw_current_piece()

            self.draw_next_piece()

            font = pygame.font.SysFont("Arial", 25)

            score_text = font.render(f"Счёт 🔢: {self.score}", True, WHITE)

            self.screen.blit(score_text, (10, 10))

            pygame.display.update()

        def update_game_state(self):

            if not self.is_game_over:

                self.drop_piece()

            else:

                font = pygame.font.SysFont("Helvetica", 50)

                game_over_text = font.render("Игра окончена! ⛔", True, BEIGE)

                self.screen.blit(

                    game_over_text,

                    (

                        WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,

                        WINDOW_HEIGHT // 2 - game_over_text.get_height() // 2

                    )

                )

                pygame.display.update()

                pygame.time.wait(3000)

                pygame.quit()

                exit()

    screen = pygame.display.set_mode((WINDOW_WIDTH + 6 * BLOCK_DIMENSION, WINDOW_HEIGHT))

    pygame.display.set_caption("Тетрис! 🕹️")

    clock = pygame.time.Clock()

    game = TetrisGame(screen)

    running = True

    keys_pressed = set()

    fall_speed = 500

    last_fall_time = pygame.time.get_ticks()

    while running:

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    game.move_piece(-1)

                elif event.key == pygame.K_RIGHT:

                    game.move_piece(1)

                elif event.key == pygame.K_DOWN:

                    game.drop_piece()

                elif event.key == pygame.K_UP:

                    game.rotate_piece()

                elif event.key == pygame.K_SPACE:

                    # Быстрое падение

                    while game.drop_piece():
                        pass

        if current_time - last_fall_time > fall_speed:
            game.drop_piece()

            last_fall_time = current_time

        game.render()

        game.update_game_state()

        clock.tick(10)


if __name__ == "__main__":
    main()