import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LRVH")
clock = pygame.time.Clock()
FPS = 60
pygame.font.init()
font=pygame.font.SysFont("Arial",20)

class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 0
        self.speed_y = 0
        self.damping = 0.98
        self.last_stimulus_time=0
        self.sensitivity=1.0

    def reactivate(self,current_time):
        
        
        time_since_last_stimulus=current_time-self.last_stimulus_time
        if time_since_last_stimulus < 2000:
            self.sensitivity *=0.9
        else:
            self.sensitivity=min(1,self.sensitivity+0.01*(time_since_last_stimulus//1000))

        self.last_stimulus_time=current_time
        self.speed_x = random.uniform(-5, 5)*self.sensitivity
        self.speed_y = random.uniform(-5, 5)*self.sensitivity

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
start_time=pygame.time.get_ticks()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for circle in circles:
                    current_time=pygame.time.get_ticks()
                    circle.reactivate(current_time)
                    
    
    screen.fill((255,255,255))
    current_tick=pygame.time.get_ticks()
    elasped_time=current_tick-start_time
    elasped_time_sec= elasped_time//1000
    avg_sensitivity=sum(c.sensitivity for c in circles)/len(circles)
    text=f"Current ticks:{elasped_time_sec}"
    text+=f"\naverage_sensitivity={avg_sensitivity}"
    text_surface=font.render(text,True,(0,0,255))
    screen.blit(text_surface,(10,10))
    for circle in circles:
        circle.move()
        circle.draw(screen)
        
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()