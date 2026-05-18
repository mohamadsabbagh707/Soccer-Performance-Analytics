"""
Course: CST2213 – Business Intelligence Programming 2 (Advanced Concepts)
Project Title: Performance Analytics and Predictive Modeling in a Soccer Simulation Environment
Author: Mohamad Al Sabbagh

Description:
This game simulates soccer shooting and generates structured match data
for Business Intelligence analysis and predictive modeling.
"""

import pygame
import random
import csv
import os
import matplotlib.pyplot as plt

pygame.init()

# --------------------------------------------------------
# Window Setup
# --------------------------------------------------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Soccer Game")

clock = pygame.time.Clock()

# --------------------------------------------------------
# Colors
# --------------------------------------------------------
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FONT = pygame.font.SysFont(None, 28)

# --------------------------------------------------------
# Goal Setup
# --------------------------------------------------------
GOAL_WIDTH = 90
GOAL_HEIGHT = 180

GOAL_X = WIDTH - 140
GOAL_TOP = HEIGHT // 2 - GOAL_HEIGHT // 2

GOAL_RECT = pygame.Rect(GOAL_X, GOAL_TOP, GOAL_WIDTH, GOAL_HEIGHT)

# --------------------------------------------------------
# Match Settings
# --------------------------------------------------------
MAX_SHOTS = 10
CSV_FILE = "soccer_match_data.csv"


# --------------------------------------------------------
# Player Class
# --------------------------------------------------------
class Player:
    """Represents the player controlled by the user."""

    def __init__(self, x, y):
        # Initial position
        self.x = x
        self.y = y

        # Player properties
        self.radius = 20
        self.speed = 5

    def move(self, keys):
        """Handles player movement using arrow keys"""

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if keys[pygame.K_UP]:
            self.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Keep player inside screen boundaries
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self):
        """Draw player on screen"""
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)


# --------------------------------------------------------
# Goalkeeper Class
# --------------------------------------------------------
class Goalkeeper:
    """Represents AI goalkeeper with difficulty-based behavior."""

    def __init__(self, difficulty):
        # Difficulty affects speed and reaction probability
        settings = {
            "Easy": (3, 0.2),
            "Normal": (4, 0.35),
            "Hard": (6, 0.55)
        }

        self.speed, self.reaction = settings[difficulty]

        # Goalkeeper rectangle
        self.rect = pygame.Rect(GOAL_X - 30, GOAL_TOP + 60, 18, 60)

    def move(self, ball_y):
        """Moves goalkeeper towards ball based on reaction probability"""

        if random.random() < self.reaction:
            if self.rect.centery < ball_y:
                self.rect.y += self.speed
            elif self.rect.centery > ball_y:
                self.rect.y -= self.speed

        # Keep goalkeeper inside goal area
        if self.rect.top < GOAL_TOP:
            self.rect.top = GOAL_TOP

        if self.rect.bottom > GOAL_TOP + GOAL_HEIGHT:
            self.rect.bottom = GOAL_TOP + GOAL_HEIGHT

    def draw(self):
        """Draw goalkeeper"""
        pygame.draw.rect(screen, RED, self.rect)


# --------------------------------------------------------
# Ball Class
# --------------------------------------------------------
class Ball:
    """Handles ball movement, shooting, and collision detection."""

    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y

        self.x = x
        self.y = y

        self.radius = 10

        # Speeds
        self.normal_speed = 10
        self.power_speed = 30
        self.speed = self.normal_speed

        # Velocity
        self.vx = 0
        self.vy = 0

        # State
        self.in_play = False
        self.power_shot = False

    def reset(self, x, y):
        """Reset ball after shot"""
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

        self.in_play = False
        self.power_shot = False

        self.speed = self.normal_speed

    def shoot(self, target_x, target_y, power=False):
        """Launch ball towards target"""

        self.power_shot = power
        self.speed = self.power_speed if power else self.normal_speed

        dx = target_x - self.x
        dy = target_y - self.y

        # Normalize direction vector
        mag = max((dx**2 + dy**2) ** 0.5, 1e-6)

        self.vx = self.speed * dx / mag
        self.vy = self.speed * dy / mag

        self.in_play = True

    def update(self):
        """Update ball position"""
        if self.in_play:
            self.x += self.vx
            self.y += self.vy

    def rect(self):
        """Return rectangle for collision detection"""
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):
        """Draw ball"""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)


# --------------------------------------------------------
# Game Controller Class
# --------------------------------------------------------
class Game:
    """Controls game loop, events, updates, and data collection."""

    def __init__(self):
        self.running = True

        # Random difficulty
        self.difficulty = random.choice(["Easy", "Normal", "Hard"])

        # Match stats
        self.shots = 0
        self.goals = 0
        self.saves = 0
        self.power_shots = 0

        # Objects
        self.player = Player(200, HEIGHT // 2)
        self.ball = Ball(240, HEIGHT // 2)
        self.goalkeeper = Goalkeeper(self.difficulty)

        self.match_id = self.get_match_id()

    def get_match_id(self):
        """Generate match ID based on CSV file"""

        if not os.path.exists(CSV_FILE):
            return 1

        with open(CSV_FILE) as f:
            rows = list(csv.reader(f))

        if len(rows) <= 1:
            return 1

        return len(rows)

    def save_data(self):
        """Save match results to CSV"""

        file_exists = os.path.exists(CSV_FILE)

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)

            # Write header if file is new
            if not file_exists:
                writer.writerow([
                    "match_id",
                    "difficulty_level",
                    "shots",
                    "goals",
                    "saves",
                    "power_shot_count"
                ])

            # Write match data
            writer.writerow([
                self.match_id,
                self.difficulty,
                self.shots,
                self.goals,
                self.saves,
                self.power_shots
            ])

    def events(self):
        """Handle user input"""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if not self.ball.in_play:

                    # Normal shot
                    if event.key == pygame.K_SPACE:
                        self.shoot(False)

                    # Power shot
                    if event.key == pygame.K_p:
                        self.shoot(True)

    def shoot(self, power):
        """Handle shooting logic"""

        if self.shots >= MAX_SHOTS:
            return

        self.shots += 1

        if power:
            self.power_shots += 1

        target_x = GOAL_X + GOAL_WIDTH + 5
        target_y = random.randint(GOAL_TOP - 20, GOAL_TOP + GOAL_HEIGHT + 20)

        self.ball.shoot(target_x, target_y, power)

    def update(self):
        """Update game state"""

        keys = pygame.key.get_pressed()
        self.player.move(keys)

        # Keep ball with player if not shot
        if not self.ball.in_play:
            self.ball.x = self.player.x + 30
            self.ball.y = self.player.y

        self.goalkeeper.move(self.ball.y)
        self.ball.update()

        # Collision (save)
        if self.ball.in_play and self.ball.rect().colliderect(self.goalkeeper.rect):
            self.saves += 1
            self.ball.reset(self.player.x + 30, self.player.y)

        # Goal detection
        if self.ball.in_play and self.ball.x >= GOAL_X + GOAL_WIDTH:
            if GOAL_TOP <= self.ball.y <= GOAL_TOP + GOAL_HEIGHT:
                self.goals += 1

            self.ball.reset(self.player.x + 30, self.player.y)

        # End match
        if self.shots >= MAX_SHOTS and not self.ball.in_play:
            self.running = False

    def draw(self):
        """Render everything"""

        screen.fill(GREEN)

        pygame.draw.rect(screen, WHITE, GOAL_RECT, 4)

        self.player.draw()
        self.goalkeeper.draw()
        self.ball.draw()

        accuracy = (self.goals / self.shots * 100) if self.shots > 0 else 0

        hud = FONT.render(
            f"Difficulty:{self.difficulty} Shots:{self.shots}/10 Goals:{self.goals} Saves:{self.saves} Power:{self.power_shots} Accuracy:{accuracy:.1f}%",
            True, WHITE
        )

        screen.blit(hud, (20, 20))

        pygame.display.flip()

    def run(self):
        """Main game loop"""

        while self.running:
            clock.tick(60)

            self.events()
            self.update()
            self.draw()

        pygame.quit()
        self.save_data()

        # Show performance chart
        if self.shots > 0:
            labels = ["Goals", "Saves", "Power Shots"]
            values = [self.goals, self.saves, self.power_shots]

            plt.bar(labels, values)
            plt.title("Match Performance")
            plt.show()


# --------------------------------------------------------
# Start Game
# --------------------------------------------------------
if __name__ == "__main__":
    Game().run()
