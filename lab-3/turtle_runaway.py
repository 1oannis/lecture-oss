import tkinter as tk
import turtle
import random
import time  # Import time for managing timer


class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius ** 2
        self.time_left = 15.0  # Set initial time to 15 seconds
        self.timer_running = False  # Flag to indicate if the timer is running
        self.game_over = False  # Flag to stop the game when it's over

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

    def start(self, init_dist=400, ai_timer_msec=100):
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

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

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

        # Display the appropriate message
        self.drawer.clear()
        self.drawer.penup()  # Ensure pen is up before moving the drawer
        self.drawer.setpos(0, 0)

        if won:
            # Player won, display win message and time taken
            time_taken = 15.0 - self.time_left
            self.drawer.write(f'You Won!\nTime taken: {time_taken:.3f} seconds',
                              align='center', font=('Arial', 24, 'normal'))
        else:
            # Player lost, display lose message
            self.drawer.write('You Lost!', align='center', font=('Arial', 24, 'normal'))

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

        # Register event handlers
        canvas.onkeypress(self.move_up, 'Up')
        canvas.onkeypress(self.move_down, 'Down')
        canvas.onkeypress(self.move_left, 'Left')
        canvas.onkeypress(self.move_right, 'Right')
        canvas.listen()

    def move_up(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.forward(self.step_move)

    def move_down(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.backward(self.step_move)

    def move_left(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.left(self.step_turn)

    def move_right(self):
        if not self.game.game_over:  # Only move if the game is not over
            self.right(self.step_turn)

    def run_ai(self, opp_pos, opp_heading):
        pass


class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)


if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    runner = RandomMover(screen)
    chaser = ManualMover(screen, None)

    # Create the game and pass both runner and chaser turtles
    game = RunawayGame(screen, runner, chaser)
    chaser.game = game  # Set the game reference in the chaser turtle
    game.start_countdown()
    screen.mainloop()
