import tkinter as tk
import turtle
import random
import time
import math


# Define the boundary limits for the turtles (e.g., within a 700x700 canvas)
BOUNDARY_X = 350
BOUNDARY_Y = 350
BOUNDARY_BUFFER = 50  # Buffer zone where the runner will try to avoid the boundary
ESCAPE_DISTANCE = 100  # Distance at which the runner will start orthogonal escape
COOLDOWN_STEPS = 10  # Number of steps after orthogonal escape before randomness resumes


class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius ** 2
        self.time_left = 15.0  # Set initial time to 15 seconds
        self.timer_running = False  # Flag to indicate if the timer is running
        self.game_over = False  # Flag to stop the game when it's over
        self.distance_moved = 0.0  # Track the distance moved by the player (chaser)

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing on canvas
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    def start_countdown(self):
        """Initiate the countdown before the game starts."""
        self.drawer.clear()
        self.drawer.penup()  # Make sure pen is up before moving
        self.drawer.setpos(0, 0)
        self.drawer.write("3", align='center', font=('Arial', 48, 'bold'))
        self.canvas.ontimer(lambda: self.update_countdown(2), 1000)

    def update_countdown(self, number):
        """Update the countdown on the screen."""
        self.drawer.clear()
        if number > 0:
            self.drawer.write(f"{number}", align='center', font=('Arial', 48, 'bold'))
            self.canvas.ontimer(lambda: self.update_countdown(number - 1), 1000)
        else:
            self.drawer.write("Catch The Runner!", align='center', font=('Arial', 24, 'bold'))
            self.canvas.ontimer(self.start_game, 1000)

    def start_game(self):
        """Start the game after countdown and display message."""
        self.drawer.clear()
        self.start(init_dist=400, ai_timer_msec=100)

    def start(self, init_dist=400, ai_timer_msec=50):
        self.runner.penup()
        self.chaser.penup()

        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # Start the game and the timer
        self.timer_running = True
        self.start_time = time.time()  # Record the start time
        self.update_timer()  # Start updating the timer on the screen
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        if self.game_over:  # Stop the game if it's over
            return

        # Only the runner uses AI to avoid the chaser
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())

        # Check if the runner is caught
        is_catched = self.is_catched()

        if is_catched:
            self.end_game(won=True)  # Player wins
        elif self.time_left <= 0:
            self.end_game(won=False)  # Time runs out, player loses
        else:
            # Keep the game running
            self.canvas.ontimer(self.step, self.ai_timer_msec)

    def end_game(self, won):
        """End the game and display a message based on whether the player won or lost."""
        self.game_over = True  # Set the game over flag
        self.timer_running = False  # Stop the timer

        time_taken = time.time() - self.start_time  # Calculate time taken
        if won:
            # Player won, calculate score based on time and distance moved
            score = self.calculate_score(time_taken)
            self.display_score(score, time_taken)

    def calculate_score(self, time_taken):
        """Calculate the combo score based on time and distance moved."""
        time_score = 1000 - (time_taken * 50)
        distance_score = 1000 - (self.distance_moved * 1.5)
        return max(0, time_score + distance_score)  # Ensure score doesn't go below 0

    def display_score(self, score, time_taken):
        """Display the final score and time taken."""
        self.drawer.clear()
        self.drawer.penup()  # Ensure pen is up before moving the drawer
        self.drawer.setpos(0, 0)
        self.drawer.write(f'You Won!\nTime taken: {time_taken:.3f} seconds\nScore: {score:.2f}',
                          align='center', font=('Arial', 24, 'normal'))

    def update_timer(self):
        """Update the countdown timer and display it at the top of the screen."""
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.time_left = max(0, 15.0 - elapsed_time)  # Calculate remaining time

            # Clear previous timer text and display updated time
            self.drawer.clear()
            self.drawer.penup()  # Ensure pen is up before moving the drawer
            self.drawer.setpos(0, 320)
            self.drawer.write(f'Remaining Time: {self.time_left:.3f}', align='center', font=('Arial', 16, 'normal'))

            # Check if time is up
            if self.time_left > 0:
                # Continue updating the timer every 10ms
                self.canvas.ontimer(self.update_timer, 10)
            else:
                self.end_game(won=False)  # Time ran out, the player lost


class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, game, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.game = game  # Reference to the game to check the game_over flag
        self.previous_position = self.pos()  # Track the player's previous position

        # Register event handlers
        canvas.onkeypress(self.move_up, 'Up')
        canvas.onkeypress(self.move_down, 'Down')
        canvas.onkeypress(self.move_left, 'Left')
        canvas.onkeypress(self.move_right, 'Right')
        canvas.listen()

    def move_up(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.forward(self.step_move)
            self.update_distance()
            self.check_boundary()

    def move_down(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.backward(self.step_move)
            self.update_distance()
            self.check_boundary()

    def move_left(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.left(self.step_turn)

    def move_right(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.right(self.step_turn)

    def update_distance(self):
        """Update the total distance moved by the player (chaser)."""
        current_position = self.pos()
        distance_moved = math.sqrt((current_position[0] - self.previous_position[0]) ** 2 +
                                   (current_position[1] - self.previous_position[1]) ** 2)
        self.game.distance_moved += distance_moved  # Add to the total distance
        self.previous_position = current_position  # Update the previous position

    def check_boundary(self):
        """Ensure the chaser stays within the screen boundaries."""
        x, y = self.pos()
        if x < -BOUNDARY_X:
            self.setx(-BOUNDARY_X)
        if x > BOUNDARY_X:
            self.setx(BOUNDARY_X)
        if y < -BOUNDARY_Y:
            self.sety(-BOUNDARY_Y)
        if y > BOUNDARY_Y:
            self.sety(BOUNDARY_Y)


class IntelligentMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.cooldown = 0  # Cooldown counter to prevent immediate reversal after orthogonal escape

    def run_ai(self, chaser_pos, chaser_heading):
        """Move intelligently to avoid the chaser and boundaries."""
        runner_pos = self.pos()
        dx = runner_pos[0] - chaser_pos[0]
        dy = runner_pos[1] - chaser_pos[1]
        distance_to_chaser = math.sqrt(dx**2 + dy**2)

        if self.cooldown > 0:
            # Continue moving in the same direction during cooldown
            self.forward(self.step_move)
            self.cooldown -= 1
        elif distance_to_chaser < ESCAPE_DISTANCE:
            # If the player is too close, move orthogonally and set cooldown
            self.orthogonal_escape(chaser_heading)
            self.cooldown = COOLDOWN_STEPS  # Prevent direction changes for a few steps
        elif self.near_boundary():
            # Avoid boundary by moving away
            self.avoid_boundary()
        else:
            # Randomize the movement to make it less predictable
            self.random_movement()

        # Ensure the runner stays within boundaries
        self.check_boundary()

    def random_movement(self):
        """Performs continuous random movement."""
        random_angle = random.uniform(-45, 45)  # Random small angle changes
        self.setheading(self.heading() + random_angle)  # Adjust current heading
        self.forward(self.step_move)

    def orthogonal_escape(self, chaser_heading):
        """Move orthogonally to the player's direction to gain more distance."""
        # Move left or right depending on a random choice
        orthogonal_angle = chaser_heading + (90 if random.choice([True, False]) else -90)
        self.setheading(orthogonal_angle)
        self.forward(self.step_move)

    def near_boundary(self):
        """Check if the runner is near the boundary."""
        x, y = self.pos()
        return (x < -BOUNDARY_X + BOUNDARY_BUFFER or
                x > BOUNDARY_X - BOUNDARY_BUFFER or
                y < -BOUNDARY_Y + BOUNDARY_BUFFER or
                y > BOUNDARY_Y - BOUNDARY_BUFFER)

    def avoid_boundary(self):
        """Move away from the boundary when too close."""
        x, y = self.pos()
        if x < -BOUNDARY_X + BOUNDARY_BUFFER:
            self.setheading(0)  # Move right
        elif x > BOUNDARY_X - BOUNDARY_BUFFER:
            self.setheading(180)  # Move left
        if y < -BOUNDARY_Y + BOUNDARY_BUFFER:
            self.setheading(90)  # Move up
        elif y > BOUNDARY_Y - BOUNDARY_BUFFER:
            self.setheading(270)  # Move down
        self.forward(self.step_move)

    def check_boundary(self):
        """Ensure the runner stays within the screen boundaries."""
        x, y = self.pos()
        if x < -BOUNDARY_X:
            self.setx(-BOUNDARY_X)
        if x > BOUNDARY_X:
            self.setx(BOUNDARY_X)
        if y < -BOUNDARY_Y:
            self.sety(-BOUNDARY_Y)
        if y > BOUNDARY_Y:
            self.sety(BOUNDARY_Y)


if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    runner = IntelligentMover(screen)  # Initialize intelligent runner turtle
    chaser = ManualMover(screen, None)  # Initialize chaser turtle

    # Create the game and pass both runner and chaser turtles
    game = RunawayGame(screen, runner, chaser)
    chaser.game = game  # Set the game reference in the chaser turtle
    game.start_countdown()
    screen.mainloop()
