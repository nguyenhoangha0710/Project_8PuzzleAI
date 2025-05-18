import pygame
import random
import pickle
import time
import os

# --- Cấu hình ---
GRID_SIZE = 15
CELL_SIZE = 40
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 15
MAX_STEPS = 200  # để tránh rắn chạy mãi nếu không gặp thức ăn

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)

# Hành động
actions = ["U", "D", "L", "R"]

# Khởi tạo Q-table
q_table = {}

# --- Q-learning ---
alpha = 0.1       # learning rate
gamma = 0.9       # discount factor
epsilon = 1.0     # exploration
epsilon_decay = 0.995
epsilon_min = 0.1


def state_to_tuple(snake, food):
    head = snake[0]
    danger = [
        (head[0] - 1, head[1]) in snake or head[0] == 0,  # up
        (head[0] + 1, head[1]) in snake or head[0] == GRID_SIZE - 1,  # down
        (head[0], head[1] - 1) in snake or head[1] == 0,  # left
        (head[0], head[1] + 1) in snake or head[1] == GRID_SIZE - 1,  # right
    ]
    food_dir = [
        food[0] < head[0],  # food is up
        food[0] > head[0],  # food is down
        food[1] < head[1],  # food is left
        food[1] > head[1],  # food is right
    ]
    return tuple(danger + food_dir)

def get_q(state, action):
    if (state, action) not in q_table:
        q_table[(state, action)] = 0
    return q_table[(state, action)]

def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions)
    q_values = [get_q(state, a) for a in actions]
    max_q = max(q_values)
    best = [a for a, q in zip(actions, q_values) if q == max_q]
    return random.choice(best)

def update_q(state, action, reward, next_state):
    current_q = get_q(state, action)
    max_future_q = max([get_q(next_state, a) for a in actions])
    q_table[(state, action)] = current_q + alpha * (reward + gamma * max_future_q - current_q)

def move(snake, action):
    head = snake[0]
    if action == "U":
        new_head = (head[0] - 1, head[1])
    elif action == "D":
        new_head = (head[0] + 1, head[1])
    elif action == "L":
        new_head = (head[0], head[1] - 1)
    elif action == "R":
        new_head = (head[0], head[1] + 1)
    return [new_head] + snake[:-1]

def is_collision(pos, snake):
    x, y = pos
    return (
        x <= 0 or x >= GRID_SIZE - 1 or
        y <= 0 or y >= GRID_SIZE - 1 or
        pos in snake
    )

def draw(screen, snake, food):
    screen.fill(BLACK)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if i == 0 or i == GRID_SIZE - 1 or j == 0 or j == GRID_SIZE - 1:
                pygame.draw.rect(screen, GRAY, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food[1] * CELL_SIZE, food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def generate_food(snake):
    while True:
        pos = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
        if pos not in snake:
            return pos

def main():
    global epsilon
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake AI Training")
    clock = pygame.time.Clock()

    episodes = 0
    best_score = 0

    while True:
        snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        food = generate_food(snake)
        score = 0
        steps = 0
        alive = True

        while alive:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("q_table_snake.pkl", "wb") as f:
                        pickle.dump(q_table, f)
                    pygame.quit()
                    return

            state = state_to_tuple(snake, food)
            action = choose_action(state)
            new_snake = move(snake, action)
            head = new_snake[0]

            steps += 1
            if is_collision(head, snake):
                reward = -10
                alive = False
            elif head == food:
                new_snake.append(snake[-1])
                food = generate_food(new_snake)
                reward = 10
                score += 1
                steps = 0
            else:
                reward = -0.1

            next_state = state_to_tuple(new_snake, food)
            update_q(state, action, reward, next_state)
            snake = new_snake

            draw(screen, snake, food)
            pygame.display.flip()

            if steps > MAX_STEPS:
                alive = False

        episodes += 1
        epsilon = max(epsilon * epsilon_decay, epsilon_min)
        if score > best_score:
            best_score = score
        print(f"Episode {episodes} | Score: {score} | Best: {best_score} | Epsilon: {epsilon:.3f}")

if __name__ == "__main__":
    main()
