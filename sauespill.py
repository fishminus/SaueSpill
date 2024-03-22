import pygame
import random

# FARVER
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Størrelse og andre konstanter
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
GHOST_SIZE = 30
OBSTACLE_SIZE = 30
SHEEP_SIZE = 20
SPEED = 5
GHOST_SPEED = 3

class gameObject():
    pass

class Player(pygame.sprite.Sprite):#spillerklasse
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT // 2
        self.SheepCarry = False

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        # Sjekker kantkollisjon
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= SCREEN_WIDTH - PLAYER_SIZE:
            self.rect.x = SCREEN_WIDTH - PLAYER_SIZE
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= SCREEN_HEIGHT - PLAYER_SIZE:
            self.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
        
        if not self.SheepCarry:
            self.image.fill(WHITE)
        else:
            self.image.fill(GREEN)

        obstacles_hit = pygame.sprite.spritecollide(self, obstacles, False)
        for obstacle in obstacles_hit:
            # If moving right, adjust player position to the left side of the obstacle
            if dx > 0:
                self.rect.right = obstacle.rect.left
            # If moving left, adjust player position to the right side of the obstacle
            elif dx < 0:
                self.rect.left = obstacle.rect.right
            # If moving down, adjust player position to the top side of the obstacle
            if dy > 0:
                self.rect.bottom = obstacle.rect.top
            # If moving up, adjust player position to the bottom side of the obstacle
            elif dy < 0:
                self.rect.top = obstacle.rect.bottom

class Ghost(pygame.sprite.Sprite):#spøkelsesklasse
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([GHOST_SIZE, GHOST_SIZE])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - GHOST_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - GHOST_SIZE)
        self.dx = random.choice([-1, 1]) * GHOST_SPEED
        self.dy = random.choice([-1, 1]) * GHOST_SPEED

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Sjekker kantkollisjon
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - GHOST_SIZE:
            self.dx *= -1
        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT - GHOST_SIZE:
            self.dy *= -1
        
        obstacles_hit = pygame.sprite.spritecollide(self, obstacles, False)
        for obs in obstacles_hit:
            if self.rect.x <= 0 or self.rect.x >= OBSTACLE_SIZE - GHOST_SIZE:
                self.dx *= -1
            if self.rect.y <= 0 or self.rect.y >= OBSTACLE_SIZE - GHOST_SIZE:
                self.dy *= -1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([OBSTACLE_SIZE, OBSTACLE_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y#posisjonsvariabler

class Sheep(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([SHEEP_SIZE, SHEEP_SIZE])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Initialiser Pygame
pygame.init()

# Setter opp skjerm
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Manic Mansion")

# Oppretter spilleobjekter
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
sheep = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Legger til hindringer
def add_obstacles(amt):
    for _ in range(amt):
        obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE), random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE))
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

# Legger til sauene
def add_sheep(amt):
    for _ in range(amt):
        sheep_obj = Sheep(random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - SHEEP_SIZE), random.randint(0, SCREEN_HEIGHT - SHEEP_SIZE))
        all_sprites.add(sheep_obj)
        sheep.add(sheep_obj)

# Legger til spøkelser
def add_ghosts(amt):
    for _ in range(amt):
        ghost = Ghost()
        all_sprites.add(ghost)
        ghosts.add(ghost)

add_obstacles(3)
add_sheep(3)
add_ghosts(1)

# Lager en klokke for å styre oppdateringshastigheten
clock = pygame.time.Clock()

running = True
dx = dy = 0

while running:
    # Holder spillet på riktig oppdateringshastighet
    clock.tick(30)

    # Håndterer hendelser
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx = -SPEED
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx = SPEED
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                dy = -SPEED
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                dy = SPEED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                dy = 0

    # Oppdaterer spillerens posisjon
    player.update(dx, dy)
    
    for big_g in ghosts:
        big_g.update()

    # Sjekker for kollisjoner mellom spiller og sau
    sheeps_hit = pygame.sprite.spritecollide(player, sheep, False)
    for one in sheeps_hit:
        if not player.SheepCarry:
            one.kill()
            player.SheepCarry = True

    # Sjekker for kollisjon mellom spiller og spøkelser
    ghosts_hit = pygame.sprite.spritecollide(player, ghosts, False)
    if ghosts_hit:
        running = False  # Spillet slutter hvis spilleren treffer et spøkelse


    # Tegner alt
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Sjekker om spilleren har kommet til startsonen
    if player.rect.x <= 0 and player.SheepCarry:
        player.SheepCarry = False
        # Legger til poeng
        print("Poeng!")
        # Øker spillerens fart
        SPEED += 1
        # Legger til ny sau
        add_sheep(1)
        # Legger til nye hindringer
        add_obstacles(3)
        # Legger til nye spøkelser
        add_ghosts(1)

# Avslutter Pygame
pygame.quit()