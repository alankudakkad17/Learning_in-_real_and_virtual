import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LRVH")
clock = pygame.time.Clock()
FPS = 60

class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-5, 5)
        self.damping = 0.98

    def reactivate(self):
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-5, 5)

    def move(self):
        self.speed_x *= self.damping
        self.speed_y *= self.damping
        if abs(self.speed_x) < 0.1:
            self.speed_x = 0
        if abs(self.speed_y) < 0.1:
            self.speed_y = 0
        self.x = int(self.x + self.speed_x) % WIDTH
        self.y = int(self.y + self.speed_y) % HEIGHT
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        
    
circles = []
for _ in range(10):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    radius = random.randint(20, 50)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    circle = Circle(x, y, radius, color)
    circles.append(circle)
    
# print(len(circles))
x, y = 300, 300
radius = 50

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for circle in circles:
                    circle.reactivate()
    
    screen.fill((255,255,255))
    
    for circle in circles:
        circle.move()
        circle.draw(screen)
        
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()