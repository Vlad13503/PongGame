import pygame as pg
pg.init()

width, height = 700, 500

pg.display.set_icon(pg.image.load("PongLogo.jpg"))
WIN = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption("PONG")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 10

SCORE_FONT = pg.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

class Paddle:
    COLOR = WHITE
    VELOCITY = 4 

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def drawPaddle(self, win):
        pg.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def movePaddle(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def resetPaddle(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VELOCITY = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def drawBall(self, win):
        pg.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def moveBall(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def resetBall(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity *= -1
        self.y_velocity = 0


def draw(win, paddles, ball, left_player_score, right_player_score):
    win.fill(BLACK)

    left_player_score_text = SCORE_FONT.render(f"{left_player_score}", 1, WHITE)
    right_player_score_text = SCORE_FONT.render(f"{right_player_score}", 1, WHITE)
    win.blit(left_player_score_text, (width // 4 - left_player_score_text.get_width() // 2, 20))
    win.blit(right_player_score_text, (3 * width // 4 - right_player_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.drawPaddle(WIN)

    ball.drawBall(win)

    pg.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= height or ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = difference_y / reduction_factor
                ball.y_velocity = -1 * y_velocity
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_velocity = difference_y / reduction_factor
                ball.y_velocity = -1 * y_velocity

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pg.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.movePaddle(up=True)
    if keys[pg.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= height:
        left_paddle.movePaddle(up=False)

    if keys[pg.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.movePaddle(up=True)
    if keys[pg.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= height:
        right_paddle.movePaddle(up=False)

def main():
    global width, height
    
    running = True
    clock = pg.time.Clock()

    left_paddle = Paddle(10, height // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(width - 10 - PADDLE_WIDTH, height // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(width // 2, height // 2, BALL_RADIUS)

    left_player_score = 0
    right_player_score = 0

    while running:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_player_score, right_player_score)

        for crtEvent in pg.event.get():
            if crtEvent.type == pg.QUIT:
                running = False
                break
            elif crtEvent.type == pg.VIDEORESIZE:
                width, height = crtEvent.size
                left_paddle = Paddle(10, height // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
                right_paddle = Paddle(width - 10 - PADDLE_WIDTH, height // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
                ball = Ball(width // 2, height // 2, BALL_RADIUS)

        keys = pg.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.moveBall()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_player_score += 1
            ball.resetBall()
        elif ball.x > width:
            left_player_score += 1
            ball.resetBall()

        game_won = False

        if left_player_score >= WINNING_SCORE:
            game_won = True
            win_text = "Left Player Won!"
        elif right_player_score >= WINNING_SCORE:
            game_won = True
            win_text = "Right Player Won!"

        if game_won:
            game_over_text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
            pg.display.update()
            pg.time.delay(3000)
            ball.resetBall()
            left_paddle.resetPaddle()
            right_paddle.resetPaddle()
            left_player_score = right_player_score = 0

    pg.quit()

if __name__ == '__main__':
    main()