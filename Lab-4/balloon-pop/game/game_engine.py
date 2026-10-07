import random
import time

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
ROUND_TIME_SECONDS = 30

class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the game state for a new round."""
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.start_time = time.time()
        self.time_left = ROUND_TIME_SECONDS

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)
        self.balloons.append(Balloon(x=x, y=-radius, radius=radius, speed=speed))

    def handle_click(self, pos):
        # Allow restarting the game via a mouse click if the game is over
        if self.game_over:
            self.reset()
            return

        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points
            if self.score < 0:
                self.score = 0

    def update(self):
        if self.game_over:
            return

        # Update the countdown timer
        elapsed_time = time.time() - self.start_time
        self.time_left = max(0, int(ROUND_TIME_SECONDS - elapsed_time))

        # Check timeout condition
        if self.time_left <= 0:
            self.game_over = True
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        active_balloons = []
        for b in self.balloons:
            if b.is_past_bottom(HEIGHT):
                self.lives -= 1
            else:
                active_balloons.append(b)
                
        self.balloons = active_balloons

        # Check lives condition
        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 40))
        renderer.draw_text(surface, font, f"Time: {self.time_left}s", (10, 70))
        
        if self.game_over:
            # Adjust these coordinates depending on your display size and font
            renderer.draw_text(surface, font, "GAME OVER", (WIDTH // 2 - 80, HEIGHT // 2 - 30))
            renderer.draw_text(surface, font, f"Final Score: {self.score}", (WIDTH // 2 - 80, HEIGHT // 2 + 10))
            renderer.draw_text(surface, font, "Click or Press 'R' to Restart", (WIDTH // 2 - 140, HEIGHT // 2 + 50))