import arcade


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.paddle = None
        self.ball = None
        self.bricks = None

        arcade.set_background_color(arcade.csscolor.DIM_GRAY)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        pass


def main():
    GameWindow(1280, 720, "Breakout Game")
    arcade.run()


if __name__ == "__main__":
    main()
