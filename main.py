import arcade

PADDLE_SPEED = 6
BALL_SPEED = 2
BTN_WIDTH = 200
BTN_HEIGHT = 50


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.all_sprites = None
        self.background = None
        self.ball = None
        self.bricks = None
        self.paddle = None
        self.game_over = False
        self.start_button = None

        self.setup()

    def setup(self):
        self.background = arcade.load_texture("./assets/background.png")
        self.all_sprites = arcade.SpriteList()

        self.paddle = arcade.Sprite(
            "./assets/paddle.png", center_x=self.width // 2, center_y=50
        )
        self.paddle.change_x = 0
        self.all_sprites.append(self.paddle)

        self.ball = arcade.Sprite(
            "./assets/ball.png", center_x=self.width // 2, center_y=self.height // 2
        )
        self.ball.change_x = BALL_SPEED
        self.ball.change_y = -BALL_SPEED
        self.all_sprites.append(self.ball)

        self.bricks = arcade.SpriteList()
        brick_width = 60
        brick_height = 20
        for row in range(8):
            for column in range(18):
                brick = arcade.Sprite("./assets/brick.png")
                brick.left = column * (brick_width + 10) + 15
                brick.top = self.height - row * (brick_height + 5) - 45
                self.all_sprites.append(brick)
                self.bricks.append(brick)

        self.game_over = False

    def draw_start_btn(self):
        if self.game_over:
            arcade.draw_rectangle_filled(
                self.width // 2,
                self.height // 2,
                BTN_WIDTH,
                BTN_HEIGHT,
                arcade.color.AZURE,
            )
            arcade.draw_text(
                "Start New Game",
                self.width // 2,
                self.height // 2,
                arcade.color.BLACK,
                18,
                anchor_x="center",
                anchor_y="center",
            )

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.width, self.height, self.background
        )
        self.all_sprites.draw()

        if self.game_over:
            arcade.draw_text(
                "Game Over",
                self.width / 2,
                self.height / 2 + 60,
                arcade.color.WHITE,
                54,
                anchor_x="center",
            )
            self.draw_start_btn()

    def on_update(self, delta_time: float):
        if self.game_over:
            return

        self.all_sprites.update()

        self.paddle.center_x += self.paddle.change_x
        if self.paddle.left < 0:
            self.paddle.left = 0
        if self.paddle.right > self.width:
            self.paddle.right = self.width

        self.ball.center_x += self.ball.change_x
        self.ball.center_y += self.ball.change_y

        if self.ball.left < 0 or self.ball.right > self.width:
            self.ball.change_x *= -1
        if self.ball.top > self.height:
            self.ball.change_y *= -1
        if self.ball.bottom < 0:
            self.game_over = True

        if self.ball.collides_with_sprite(self.paddle):
            self.ball.change_y *= -1
            offset = self.ball.center_x - self.paddle.center_x
            self.ball.change_x = offset * 0.1

        brick_hit_list = arcade.check_for_collision_with_list(self.ball, self.bricks)
        if brick_hit_list:
            self.ball.change_y *= -1
            for brick in brick_hit_list:
                brick.remove_from_sprite_lists()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.paddle.change_x = -PADDLE_SPEED
        if key == arcade.key.RIGHT:
            self.paddle.change_x = PADDLE_SPEED

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.paddle.change_x = 0

    def on_mouse_press(self, x: float, y: float, btn: int, modifiers: int):
        if self.game_over:
            btn_x_start = self.width // 2 - BTN_WIDTH // 2
            btn_x_end = self.width // 2 + BTN_WIDTH // 2
            btn_y_start = self.height // 2 - BTN_HEIGHT // 2
            btn_y_end = self.height // 2 + BTN_HEIGHT // 2
            if btn_x_start < x < btn_x_end and btn_y_start < y < btn_y_end:
                self.setup()


def main():
    GameWindow(1280, 720, "Breakout Game")
    arcade.run()


if __name__ == "__main__":
    main()
