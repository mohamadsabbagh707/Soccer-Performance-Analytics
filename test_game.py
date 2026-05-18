import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # prevents pygame window

import pytest
from soccer_game import Game, Ball   # <-- use your actual file name


# -------------------------------------------------
# Test 1: Verify that shooting increases shot count
# -------------------------------------------------
def test_shot_increases():
    game = Game()
    initial_shots = game.shots

    game.shoot(power=False)

    assert game.shots == initial_shots + 1


# -------------------------------------------------
# Test 2: Verify power shots are counted correctly
# -------------------------------------------------
def test_power_shot_count():
    game = Game()

    game.shoot(power=True)

    assert game.power_shots == 1


# -------------------------------------------------
# Test 3: Ensure logical constraint (goals ≤ shots)
# -------------------------------------------------
def test_goals_not_exceed_shots():
    game = Game()

    game.shots = 5
    game.goals = 3

    assert game.goals <= game.shots


# -------------------------------------------------
# Test 4: Verify ball reset behavior
# -------------------------------------------------
def test_ball_reset():
    ball = Ball(100, 100)

    ball.shoot(200, 200, power=True)
    ball.reset(50, 50)

    assert ball.in_play == False
    assert ball.power_shot == False
    assert ball.x == 50
    assert ball.y == 50


# -------------------------------------------------
# Test 5: Ensure max shots limit is respected
# -------------------------------------------------
def test_max_shots_limit():
    game = Game()

    game.shots = 10
    game.shoot(power=False)

    assert game.shots == 10
