import tkinter as tk
import random

# Constants
GAME_WIDTH = 500
GAME_HEIGHT = 500
SNAKE_SIZE = 20
FOOD_SIZE = 20
SPEED = 100  # Lower values make the game faster
BG_COLOR = "white"
SNAKE_COLOR = "blue"
FOOD_COLOR = "red"

# Directions
DIRECTIONS = {
    "Up": (0, -SNAKE_SIZE),
    "Down": (0, SNAKE_SIZE),
    "Left": (-SNAKE_SIZE, 0),
    "Right": (SNAKE_SIZE, 0)
}

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Maneesh's Snake Game")
        self.canvas = tk.Canvas(self.window, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        # Initial state
        self.snake = [(100, 100), (80, 100), (60, 100)] 
        self.food = None
        self.direction = "Right"
        self.score = 0
        self.running = True

        # Bind keypresses
        self.window.bind("<KeyPress>", self.change_direction)

        # Create initial food and start the game loop
        self.create_food()
        self.update()
        self.window.mainloop()

    def create_food(self):
        """Create a food item at a random location."""
        x = random.randint(0, (GAME_WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE
        y = random.randint(0, (GAME_HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE
        self.food = (x, y)
        self.canvas.create_rectangle(x, y, x + FOOD_SIZE, y + FOOD_SIZE, fill=FOOD_COLOR, tag="food")

    def move_snake(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.snake[0]
        move_x, move_y = DIRECTIONS[self.direction]
        new_head = (head_x + move_x, head_y + move_y)

        # Check for collisions
        if (
            new_head in self.snake  # Collides with itself
            or new_head[0] < 0  # Collides with the left wall
            or new_head[1] < 0  # Collides with the top wall
            or new_head[0] >= GAME_WIDTH  # Collides with the right wall
            or new_head[1] >= GAME_HEIGHT  # Collides with the bottom wall
        ):
            self.running = False
            return

        # Move the snake
        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.canvas.delete("food")
            self.create_food()
        else:
            self.snake.pop()

    def draw_snake(self):
        """Draw the snake on the canvas."""
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )

    def change_direction(self, event):
        """Change the snake's direction based on user input."""
        new_direction = event.keysym
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction in DIRECTIONS and new_direction != opposites[self.direction]:
            self.direction = new_direction

    def update(self):
        """Update the game state."""
        if self.running:
            self.move_snake()
            self.draw_snake()
            self.window.after(SPEED, self.update)
        else:
            self.canvas.create_text(
                GAME_WIDTH // 2,
                GAME_HEIGHT // 2,
                fill="black",
                font="Arial 20 bold",
                text=f"Game Over! Score: {self.score}",
            )

# Main block
if __name__ == "__main__":
    SnakeGame()
