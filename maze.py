import pygame
import random

GRID_SIZE = 8
TILE_SIZE = 60
WIDTH, HEIGHT = GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE + 90
MAZE = [
    [0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 2],
]

ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
FPS = 30

agent_pos = [0, 0]
score = 0
episode = 1

steps_per_frame = 50
fast_mode = False
status_message = ""

q_table = {}
alpha = 0.1
gamma = 0.9

epsilon = 1.0
epsilon_min = 0.1
epsilon_decay = 0.99

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if MAZE[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif MAZE[y][x] == 2:
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect, 2)

    agent_rect = pygame.Rect(
        agent_pos[0] * TILE_SIZE + 10,
        agent_pos[1] * TILE_SIZE + 10,
        TILE_SIZE - 20,
        TILE_SIZE - 20,
    )

    pygame.draw.rect(screen, BLUE, agent_rect)

    text = font.render(f"Score: {score:.2f}  Episode: {episode}  Mode: {'NORMAL' if not fast_mode else 'FAST'}", True, BLACK)
    screen.blit(text, (10, HEIGHT - 40))

def reset_agent():
    global agent_pos, score, episode, epsilon, epsilon_min, epsilon_decay
    agent_pos = [0, 0]
    episode += 1
    score = 0
    epsilon = max(epsilon * epsilon_decay, epsilon_min)


def choose_action(state):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    q_vals = [q_table.get((state, a), 0) for a in ACTIONS]
    max_q = max(q_vals)
    best_actions = [a for a, q in zip(ACTIONS, q_vals) if q == max_q]
    return random.choice(best_actions)

def update_q(state, action, reward, new_state):
    old_q = q_table.get((state, action), 0)
    next_max = max([q_table.get((new_state, a), 0) for a in ACTIONS])
    new_q = old_q + alpha * (reward + gamma * next_max - old_q)
    q_table[(state, action)] = new_q

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fast_mode = not fast_mode
            # dx, dy = 0, 0
            # if event.key == pygame.K_UP:
            #     dy = -1
            # elif event.key == pygame.K_DOWN:
            #     dy = 1
            # elif event.key == pygame.K_LEFT:
            #     dx = -1
            # elif event.key == pygame.K_RIGHT:
            #     dx = 1

    for _ in range(steps_per_frame if fast_mode else 1):
        state = tuple(agent_pos)
        action = choose_action(state)

        dx, dy = action
        new_x = agent_pos[0] + dx
        new_y = agent_pos[1] + dy

        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            tile = MAZE[new_y][new_x]
            new_state = (new_x, new_y)
            if tile == 1:
                reward = -1
                score += reward
                update_q(state, action, reward, state)
            else:
                reward = -0.01
                score += reward
                agent_pos = [new_x, new_y]
                if tile == 2:
                    reward = 10
                    score += reward
                    reset_agent()
                update_q(state, action, reward, new_state)

    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
