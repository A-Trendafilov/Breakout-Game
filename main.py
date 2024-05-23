import arcade
import arcade.gui
from arcade.gui import UIOnClickEvent

PADDLE_SPEED = 6
BALL_SPEED = 2
BTN_WIDTH = 200


class QuitBtn(arcade.gui.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window

    def on_click(self, event: UIOnClickEvent):
        arcade.exit()


class StartBtn(arcade.gui.UIFlatButton):
    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window

    def on_click(self, event: UIOnClickEvent):
        self.window.start_game()


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.all_sprites = None
        self.background = None
        self.ball = None
        self.bricks = None
        self.paddle = None
        self.game_over = False
        self.game_started = False
        self.score = 0

        self.btn_manager = arcade.gui.UIManager()
        self.btn_manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        start_btn = StartBtn(window=self, text="Start Game", width=BTN_WIDTH)
        self.v_box.add(start_btn)
        quit_btn = QuitBtn(window=self, text="Quit Game", width=BTN_WIDTH)
        self.v_box.add(quit_btn)

        self.btn_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
            )
        )

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
        self.game_started = False
        self.score = 0

    def start_game(self):
        self.setup()
        self.game_started = True

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.width, self.height, self.background
        )
        if self.game_started:
            self.all_sprites.draw()
            arcade.draw_text(
                f"Score: {self.score}", 10, self.height - 30, arcade.color.RED
            )
        else:
            self.btn_manager.draw()

        if self.game_over:
            arcade.draw_text(
                "Game Over",
                self.width / 2,
                self.height / 2 + 60,
                arcade.color.WHITE,
                54,
                anchor_x="center",
            )
            self.btn_manager.draw()

    def on_update(self, delta_time: float):
        if not self.game_started or self.game_over:
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
                self.score += 10

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.paddle.change_x = -PADDLE_SPEED
        if key == arcade.key.RIGHT:
            self.paddle.change_x = PADDLE_SPEED

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.paddle.change_x = 0


def main():
    GameWindow(1280, 720, "Breakout Game")
    arcade.run()


if __name__ == "__main__":
    main()
