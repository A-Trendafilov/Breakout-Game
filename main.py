import arcade


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.all_sprites = None
        self.background = None
        self.ball = None
        self.bricks = None
        self.brick = None
        self.paddle = None

        self.setup()

    def setup(self):
        self.background = arcade.load_texture("./assets/background.png")
        self.all_sprites = arcade.SpriteList()

        self.paddle = arcade.Sprite(
            "./assets/paddle.png", center_x=self.width // 2, center_y=50
        )
        self.all_sprites.append(self.paddle)

        self.ball = arcade.Sprite(
            "./assets/ball.png", center_x=self.width // 2, center_y=self.height // 2
        )
        self.ball.change_x = 3
        self.ball.change_y = -3
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

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.width, self.height, self.background
        )
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        self.all_sprites.update()

    def on_key_press(self, key: int, modifiers: int):
        pass

    def on_key_release(self, key: int, modifiers: int):
        pass


def main():
    GameWindow(1280, 720, "Breakout Game")
    arcade.run()


if __name__ == "__main__":
    main()
