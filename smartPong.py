# TRAINING DATA START
TRAINING_DATA = [-1, 0, 0, -1, 1, 1, 0, 0, 0, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 0, 0, -1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, -1, 1, 1, -1, 0, -1, -1, -1, 1, -1, -1, 1, 0, -1, -1, 1, -1, -1, 1, 0, 0, 0, 0, -1, 1, 0, 1, 1, -1, 1, 0, -1, 0, -1, 1, 0, 1, -1, 1, -1, 1, -1, 1, 1, -1, 0, -1, 1, 1, 1, -1, -1, 1, 1, 0, -1, 1, 1, 1]
# TRAINING DATA END

import time
import os
import keyboard
import random
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_training_data(training_data):
    # Save the training data in this file between the TRAINING DATA markers.
    filename = __file__
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print("Could not open file for writing training data:", e)
        return
    start_index = None
    end_index = None
    for i, line in enumerate(lines):
        if line.startswith("# TRAINING DATA START"):
            start_index = i
        if line.startswith("# TRAINING DATA END"):
            end_index = i
            break
    if start_index is not None and end_index is not None:
        new_data_str = "TRAINING_DATA = " + repr(training_data) + "\n"
        lines[start_index+1:end_index] = [new_data_str]
        try:
            with open(filename, 'w') as f:
                f.writelines(lines)
        except Exception as e:
            print("Could not write training data:", e)

def create_screen(width, height):
    return [[' ' for _ in range(width)] for _ in range(height)]

def overlay_text(screen, text_lines):
    """
    Overlay text_lines on the screen. Each tuple is (row, text), and the text is centered on that row.
    """
    height = len(screen)
    width = len(screen[0])
    for row, text in text_lines:
        if 0 <= row < height:
            start_col = (width - len(text)) // 2
            for i, ch in enumerate(text):
                if 0 <= start_col + i < width:
                    screen[row][start_col + i] = ch

def draw_screen(screen):
    for row in screen:
        print("".join(row))

def start_screen():
    # Animation grid dimensions for the start screen
    width = 44
    height = 20

    # Initialize ball position within the inner area of the box and choose a random direction
    ball_x = random.randint(2, width - 3)
    ball_y = random.randint(2, height - 3)
    dx, dy = random.choice([-1, 1]), random.choice([-1, 1])

    # Text lines to overlay (includes game mode instructions)
    text_lines = [
        (2, "=" * 44),
        (4, "Welcome to ASCII Pong!"),
        (6, "Player 1 (Left): W (Up) / S (Down)"),
        (7, "Player 2 (Right): AI or Multiplayer"),
        (9, "Press 'S' to Start Game"),
        (10, "Press 'Q' to Quit"),
        (12, "Choose Game Mode:"),
        (13, "Press 1: Classic, 2: Smart, 3: Multiplayer"),
        (15, "=" * 44)
    ]
    
    game_mode = None  # Will be set to "classic", "smart", or "multiplayer"
    
    while True:
        # Update ball position (for the bouncing animation inside the box)
        ball_x += dx
        ball_y += dy

        # Bounce off the box's inner walls
        if ball_x <= 1 or ball_x >= width - 2:
            dx = -dx
            ball_x += dx
        if ball_y <= 1 or ball_y >= height - 2:
            dy = -dy
            ball_y += dy

        # Create a new screen background
        screen = create_screen(width, height)

        # Draw a box border spanning the game area (only for the start menu)
        for i in range(width):
            screen[0][i] = '#'
            screen[height-1][i] = '#'
        for j in range(height):
            screen[j][0] = '#'
            screen[j][width-1] = '#'

        # Draw the bouncing ball
        if 0 <= ball_y < height and 0 <= ball_x < width:
            screen[ball_y][ball_x] = 'O'

        # Overlay the start text on top of the animation
        overlay_text(screen, text_lines)

        clear_screen()
        draw_screen(screen)
        time.sleep(0.05)
        
        # Allow the player to choose game mode with 1, 2, or 3 keys.
        if keyboard.is_pressed('1'):
            game_mode = "classic"
        if keyboard.is_pressed('2'):
            game_mode = "smart"
        if keyboard.is_pressed('3'):
            game_mode = "multiplayer"
        if game_mode:
            # Briefly display the chosen mode.
            clear_screen()
            print("Game Mode Selected:", game_mode.upper())
            time.sleep(0.5)
        if keyboard.is_pressed('s') and game_mode:
            return game_mode
        if keyboard.is_pressed('q'):
            return False

def update_paddle(screen, paddle_y, paddle_x, paddle_len):
    # Clear previous paddle positions
    for y in range(len(screen)):
        if screen[y][paddle_x] == '|':
            screen[y][paddle_x] = ' '
    # Draw paddle at new position
    for y in range(paddle_y, paddle_y + paddle_len):
        if 0 <= y < len(screen):
            screen[y][paddle_x] = '|'

def update_balls(screen, balls, ball_event_type=None):
    # Clear old ball positions
    for y in range(len(screen)):
        for x in range(len(screen[0])):
            if screen[y][x] == 'O':
                screen[y][x] = ' '
    # If the ball is supposed to be bigger, draw a 2x2 block
    if ball_event_type == "big_ball":
        for ball in balls:
            x = ball['x']
            y = ball['y']
            if 0 <= y < len(screen):
                if 0 <= x < len(screen[0]):
                    screen[y][x] = 'O'
                if 0 <= x+1 < len(screen[0]):
                    screen[y][x+1] = 'O'
            if 0 <= y+1 < len(screen):
                if 0 <= x < len(screen[0]):
                    screen[y+1][x] = 'O'
                if 0 <= x+1 < len(screen[0]):
                    screen[y+1][x+1] = 'O'
    else:
        for ball in balls:
            if 0 <= ball['y'] < len(screen) and 0 <= ball['x'] < len(screen[0]):
                screen[ball['y']][ball['x']] = 'O'

def draw_game_screen(screen, score_p1, score_p2, event_message=""):
    clear_screen()
    print("-" * (len(screen[0]) + 2))
    print(f"Player 1: {score_p1}      Player 2: {score_p2}")
    print("-" * (len(screen[0]) + 2))
    for row in screen:
        print("|" + "".join(row) + "|")
    print("-" * (len(screen[0]) + 2))
    if event_message:
        print(event_message)

def get_input_player1():
    if keyboard.is_pressed('w'):
        return 'W'
    elif keyboard.is_pressed('s'):
        return 'S'
    return None

def end_screen(winner):
    clear_screen()
    print("=" * 44)
    print("              GAME OVER")
    print("           " + winner)
    print("=" * 44)
    print("Press R to restart or Q to quit.")
    while True:
        if keyboard.is_pressed('q'):
            return False
        elif keyboard.is_pressed('r'):
            return True
        time.sleep(0.1)

def pong_game():
    game_mode = start_screen()
    if not game_mode:
        print("Quitting game.")
        return None

    # Game settings
    width = 40
    height = 15
    normal_paddle_len = 3
    shrunk_paddle_len = 2  # Paddle length during shrink event
    paddle1_x = 2
    paddle2_x = width - 3

    # Initial paddle positions
    paddle1_y = height // 2 - normal_paddle_len // 2
    enemy_paddle_y = float(height // 2 - normal_paddle_len // 2)

    # Ball settings: using a list to allow for multiple balls
    def create_ball():
        return {
            'x': width // 2,
            'y': height // 2,
            'dx': random.choice([-1, 1]),
            'dy': random.choice([-1, 1])
        }
    balls = [create_ball()]  # Start with one ball

    # Scores start at 0
    score_p1 = 0
    score_p2 = 0

    # Movement settings
    paddle_speed = 1           # Player paddle moves 1 unit per frame
    ball_interval = 0.1        # Ball movement interval (unchanged by events)
    fps = 30
    frame_delay = 1 / fps

    # Enemy paddle speed range (units per second) for AI modes
    min_enemy_speed = 10
    max_enemy_speed = 30

    # Special event variables
    active_event = None  # No event active initially
    event_cooldown = 60  # One special event every 60 seconds

    screen = create_screen(width, height)
    current_paddle_len = normal_paddle_len
    update_paddle(screen, paddle1_y, paddle1_x, current_paddle_len)
    update_paddle(screen, int(enemy_paddle_y), paddle2_x, current_paddle_len)
    update_balls(screen, balls)
    draw_game_screen(screen, score_p1, score_p2)

    last_frame_time = time.time()
    last_ball_move_time = time.time()

    # Main game loop
    while True:
        current_time = time.time()
        dt = current_time - last_frame_time

        if dt >= frame_delay:
            # Process player 1 input
            action_p1 = get_input_player1()
            if action_p1 == 'W':
                paddle1_y -= paddle_speed
            elif action_p1 == 'S':
                paddle1_y += paddle_speed
            paddle1_y = max(0, min(paddle1_y, height - normal_paddle_len))

            # --- Opponent Movement ---
            if game_mode == "multiplayer":
                # Player 2 controls using I (up) and K (down)
                if keyboard.is_pressed('i'):
                    enemy_paddle_y -= paddle_speed
                elif keyboard.is_pressed('k'):
                    enemy_paddle_y += paddle_speed
            else:
                enemy_speed = random.uniform(min_enemy_speed, max_enemy_speed)
                if game_mode == "classic" or (game_mode == "smart" and not TRAINING_DATA):
                    enemy_center = enemy_paddle_y + normal_paddle_len / 2
                    if balls:
                        if balls[0]['y'] < enemy_center:
                            enemy_paddle_y -= enemy_speed * dt
                        elif balls[0]['y'] > enemy_center:
                            enemy_paddle_y += enemy_speed * dt
                else:
                    ball = balls[0]
                    if ball['dx'] > 0:
                        time_to_reach = (paddle2_x - ball['x']) / abs(ball['dx'])
                        avg_offset = sum(TRAINING_DATA) / len(TRAINING_DATA) if TRAINING_DATA else 0
                        predicted_y = ball['y'] + ball['dy'] * time_to_reach + avg_offset
                    else:
                        predicted_y = ball['y']
                    enemy_center = enemy_paddle_y + normal_paddle_len / 2
                    if predicted_y < enemy_center:
                        enemy_paddle_y -= enemy_speed * dt
                    elif predicted_y > enemy_center:
                        enemy_paddle_y += enemy_speed * dt
            enemy_paddle_y = max(0, min(enemy_paddle_y, height - normal_paddle_len))

            # Special event logic: trigger one event every 60 seconds
            if active_event is None:
                event_cooldown -= dt
                if event_cooldown <= 0:
                    event_choice = random.choice(["shrink", "double_balls", "big_ball"])
                    if event_choice == "shrink":
                        active_event = {
                            "type": "shrink",
                            "end_time": current_time + 5,
                            "message": "Special Event: Both paddles shrink for 5 seconds!"
                        }
                    elif event_choice == "double_balls":
                        active_event = {
                            "type": "double_balls",
                            "end_time": current_time + 10,
                            "message": "Special Event: Double Balls for 10 seconds!"
                        }
                    elif event_choice == "big_ball":
                        active_event = {
                            "type": "big_ball",
                            "end_time": current_time + 15,
                            "message": "Special Event: Ball is bigger for 15 seconds!"
                        }
            else:
                if current_time >= active_event["end_time"]:
                    active_event = None
                    event_cooldown = 60  # Reset cooldown after an event ends
                    if len(balls) > 1:
                        balls = balls[:1]

            # Adjust paddle length based on shrink event
            if active_event and active_event["type"] == "shrink":
                current_paddle_len = shrunk_paddle_len
            else:
                current_paddle_len = normal_paddle_len

            # Handle double balls event: if active, ensure two balls are in play
            if active_event and active_event["type"] == "double_balls":
                if len(balls) < 2:
                    balls.append(create_ball())

            # Update ball positions (collision detection based on the ball's top-left coordinate)
            if current_time - last_ball_move_time >= ball_interval:
                for ball in balls:
                    ball['x'] += ball['dx']
                    ball['y'] += ball['dy']

                    # Bounce off top and bottom walls
                    if ball['y'] <= 0 or ball['y'] >= height - 1:
                        ball['dy'] *= -1

                    # Collision with player's paddle:
                    if ball['x'] == paddle1_x + 1 and paddle1_y <= ball['y'] < paddle1_y + current_paddle_len:
                        if game_mode == "smart":
                            offset = ball['y'] - (paddle1_y + current_paddle_len // 2)
                            TRAINING_DATA.append(offset)
                            save_training_data(TRAINING_DATA)
                        ball['dx'] *= -1
                    # Collision with enemy paddle
                    elif ball['x'] == paddle2_x - 1 and int(enemy_paddle_y) <= ball['y'] < int(enemy_paddle_y) + current_paddle_len:
                        ball['dx'] *= -1

                    # Check for scoring and reset the ball if needed
                    if ball['x'] < 0:
                        score_p2 += 1
                        ball.update(create_ball())
                    elif ball['x'] >= width:
                        score_p1 += 1
                        ball.update(create_ball())
                last_ball_move_time = current_time

            # Redraw the game screen
            screen = create_screen(width, height)
            update_paddle(screen, paddle1_y, paddle1_x, current_paddle_len)
            update_paddle(screen, int(enemy_paddle_y), paddle2_x, current_paddle_len)
            ball_draw_type = active_event["type"] if active_event and active_event["type"] == "big_ball" else None
            update_balls(screen, balls, ball_draw_type)
            event_message = active_event["message"] if active_event else ""
            draw_game_screen(screen, score_p1, score_p2, event_message)

            last_frame_time = current_time

            if score_p1 >= 10 or score_p2 >= 10:
                break
        else:
            time.sleep(frame_delay - dt)
        if keyboard.is_pressed('q'):
            print("Game ended by player.")
            return None

    if game_mode == "multiplayer":
        winner = "Player 1 wins!" if score_p1 >= 10 else "Player 2 wins!"
    else:
        winner = "Player 1 wins!" if score_p1 >= 10 else "AI wins!"
    return winner

if __name__ == "__main__":
    while True:
        result = pong_game()
        if result is None:
            break
        if not end_screen(result):
            break
