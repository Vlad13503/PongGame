import pygame as pg
pg.init()

WIDTH, HEIGHT = 700, 500
pg.display.set_icon(pg.image.load("PongLogo.jpg"))
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("PONG")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

class Paddle:
    COLOR = WHITE
    VELOCITY = 4 

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def drawPaddle(self, win):
        pg.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def movePaddle(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

def draw(win, paddles):
    win.fill(BLACK)

    for paddle in paddles:
        paddle.drawPaddle(WIN)

    pg.display.update()

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pg.K_w]:
        left_paddle.movePaddle(up=True)
    if keys[pg.K_s]:
        left_paddle.movePaddle(up=False)

    if keys[pg.K_UP]:
        right_paddle.movePaddle(up=True)
    if keys[pg.K_DOWN]:
        right_paddle.movePaddle(up=False)

def main():
    running = True
    clock = pg.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while running:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle])

        for crtEvent in pg.event.get():
            if crtEvent.type == pg.QUIT:
                running = False
                break

        keys = pg.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

    pg.quit()

if __name__ == '__main__':
    main()