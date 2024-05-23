import arcade
from game_app import GameWindow


def main():
    GameWindow(1280, 720, "Breakout Game")
    arcade.run()


if __name__ == "__main__":
    main()
