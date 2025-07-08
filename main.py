import math
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
clock = pygame.time.Clock() #keeps whole simulation running

G = 6.67430e-11
SCALE = 6e-11       # shows everything
ZOOM_SCALE = 1e-9   # shows a part of the system simulation 
DT = 86400

zoomed = False

class Body:
    def __init__(self, x, y, vx, vy, mass, radius , color): 
        #vi is velocity along i-axis
        self.x = x 
        self.y = y 
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius 
        self.color = color
        self.trail = []

    def update_position(self, bodies):
        fx = fy = 0

        for other in bodies:
            if other != self:
                dx = other.x - self.x 
                dy = other.y - self.y 

                r = math.sqrt(dx ** 2 + dy **2)
                if r > 0:
                    # F = (G*m1*m2) / r*r
                    f = G * self.mass * other.mass / (r ** 2)
                    fx += f * dx / r 
                    fy += f * dy / r 

        # F = ma -> a = F / m
        ax = fx / self.mass
        ay = fy / self.mass

        self.vx += ax * DT
        self.vy += ay * DT

        self.x += self.vx * DT
        self.y += self.vy * DT

        current_scale = ZOOM_SCALE if zoomed else SCALE

        self.trail.append((int(self.x * current_scale + WIDTH // 2),int(self.y * current_scale + HEIGHT // 2)))

        if len(self.trail) > 200:
            self.trail.pop(0)


    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (50,50,50), False, self.trail, 1)

            current_scale = ZOOM_SCALE if zoomed else SCALE

            screen_x = int(self.x * current_scale + WIDTH // 2)
            screen_y = int(self.y * current_scale + HEIGHT // 2)

            pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


bodies = [
    # 🌞 Sun
    Body(0, 0, 0, 0, 1.989e30, 8, (255, 255, 0)),  # Sun

    # 🌍 Mercury
    Body(5.79e10, 0, 0, 47870, 3.30e23, 2, (169, 169, 169)),  # Mercury: gray

    # 🌍 Venus
    Body(1.082e11, 0, 0, 35020, 4.87e24, 3, (218, 165, 32)),  # Venus: golden

    # 🌍 Earth
    Body(1.496e11, 0, 0, 29780, 5.972e24, 4, (100, 149, 237)),  # Earth: blue

    # 🌍 Mars
    Body(2.279e11, 0, 0, 24070, 6.417e23, 3, (255, 69, 0)),  # Mars: red

    # 🌍 Jupiter
    Body(7.785e11, 0, 0, 13070, 1.898e27, 6, (218, 165, 32)),  # Jupiter: orange-brown

    # 🌍 Saturn
    Body(1.433e12, 0, 0, 9680, 5.683e26, 5, (210, 180, 140)),  # Saturn: pale golden

    # 🌍 Uranus
    Body(2.877e12, 0, 0, 6800, 8.681e25, 4, (173, 216, 230)),  # Uranus: light blue

    # 🌍 Neptune
    Body(4.503e12, 0, 0, 5430, 1.024e26, 4, (72, 61, 139)),  # Neptune: deep blue
]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z: # press z for scale
                zoomed = not zoomed

            for body in bodies:
                body.trail = []

    screen.fill((0,0,0))

    for body in bodies:
        body.update_position(bodies)
        body.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()