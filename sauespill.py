import pygame
import random

# FARVER
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)#forskjellige grønnfarger
GREENNT = (0, 150, 0)
GREENNTBORING = (0, 100, 0)

# Størrelse og andre konstanter
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
GHOST_SIZE = 30
OBSTACLE_SIZE = 50
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

    def update(self, dx, dy):#Oppdateringsfunksjon for spilleren variabler
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
        
        if not self.SheepCarry:#oppdaterer om spilleren bærer sau
            self.image.fill(WHITE)
        else:
            self.image.fill(GREEN)

        obstacles_hit = pygame.sprite.spritecollide(self, obstacles, False)
        for _ in obstacles_hit:#Litt rar veggkollisjon
            if dx > 0:
                self.rect.right -= dx
            elif dx < 0:
                self.rect.left -= dx
            if dy > 0:
                self.rect.bottom -= dy
            elif dy < 0:
                self.rect.top -= dy

class Ghost(pygame.sprite.Sprite):#spøkelsesklasse
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([GHOST_SIZE, GHOST_SIZE])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(200, SCREEN_WIDTH - GHOST_SIZE-200)
        self.rect.y = random.randint(200, SCREEN_HEIGHT - GHOST_SIZE-200)
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
        print(self.dx, self.dy)
        for obs in obstacles_hit:#det er en feil her som gjør at spøkelset spretter feil i vertikalen
            if self.rect.x <= obs.rect.x + OBSTACLE_SIZE and self.rect.x >= obs.rect.x - GHOST_SIZE:
                self.dx *= -1
                break
            elif self.rect.y <= obs.rect.y + OBSTACLE_SIZE and self.rect.y >= obs.rect.y - GHOST_SIZE:
                self.dy *= -1
        safezones_hit = pygame.sprite.spritecollide(self, safezones, False)
        for sf in safezones_hit:
            if self.rect.x <= sf.rect.x or self.rect.x >= sf.rect.x - GHOST_SIZE:
                self.dx *= -1
                break
            if self.rect.y <= sf.rect.y or self.rect.y >= sf.rect.y - GHOST_SIZE:
                self.dy *= -1

class Obstacle(pygame.sprite.Sprite):#for veggobjektene i spillet, de er bare statiske
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([OBSTACLE_SIZE, OBSTACLE_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
class Safe_Zone(pygame.sprite.Sprite):#Safezones
    def __init__(self, x, y, collecterplace, scalex, scaley):
        super().__init__()
        self.image = pygame.Surface([scalex, scaley])
        self.collecterplace = collecterplace
        if(collecterplace):#kan sonen la spilleren sanke inn sauer - en boolean
            self.image.fill(GREENNT)
        else:
            self.image.fill(GREENNTBORING)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Sheep(pygame.sprite.Sprite):
    def __init__(self, x, y, pickupable):
        super().__init__()
        self.image = pygame.Surface([SHEEP_SIZE, SHEEP_SIZE])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pickupable = pickupable #kan den plukkes opp? dette brukes for sauene du får over til andre siden

# Initialiser Pygame
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Manic Mansion")

# Oppretter Objektgruppene for kollisjonsfunksjonen i pygame, veldig nyttig!
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
sheep = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
safezones = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

#Funksjoner for å legge til objekter tilrettelagt spillerkartet
def Safe_zones():#to safezones, en for sauesanking og en annen som spillerbase
    safezone = Safe_Zone(0,0,True,200,800)
    safezone2 = Safe_Zone(600,0,False,200,800)
    safezones.add(safezone)
    safezones.add(safezone2)

def add_obstacles(amt):
    for _ in range(amt):
        obstacle = Obstacle(random.randint(200, SCREEN_WIDTH - OBSTACLE_SIZE-200), random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE))
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

def add_sheep(amt):
    for _ in range(amt):
        sheep_obj = Sheep(random.randint(600, SCREEN_WIDTH - SHEEP_SIZE), random.randint(0, SCREEN_HEIGHT - SHEEP_SIZE),True)
        all_sprites.add(sheep_obj)
        sheep.add(sheep_obj)

def add_ghosts(amt):
    for _ in range(amt):
        ghost = Ghost()
        all_sprites.add(ghost)
        ghosts.add(ghost)

#Første objekter legges til her
Safe_zones()
add_obstacles(3)
add_sheep(3)
add_ghosts(1)

clock = pygame.time.Clock()

running = True#running variabel for å tape spiller
dx = dy = 0

while running:
    # Holder spillet på riktig oppdateringshastighet
    clock.tick(30)

    # hendelser
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

    # Oppdaterer spilleren, med tidligere definert funksjon
    player.update(dx, dy)
    
    for big_g in ghosts:
        big_g.update()

    # Sjekker for kollisjoner mellom spiller og sau
    sheeps_hit = pygame.sprite.spritecollide(player, sheep, False)
    for one in sheeps_hit:
        if not player.SheepCarry and one.pickupable:
            one.kill()
            player.SheepCarry = True
        elif player.SheepCarry and one.pickupable:#hvorfor ville spilleren dødd når dette skjer (man dør hvis man rører en sau for mye)
            running = False
    safehits = pygame.sprite.spritecollide(player, safezones, False)
    for sf in safehits:
        if player.SheepCarry and sf.collecterplace:
            player.SheepCarry = False
            sheep_obj = Sheep(player.rect.x-50, player.rect.y, False)
            all_sprites.add(sheep_obj)
            sheep.add(sheep_obj)
            add_obstacles(3)#gjorde det litt mer vanskelig  
            add_sheep(1)
            add_ghosts(3)


    # Sjekker for kollisjon mellom spiller og spøkelser
    ghosts_hit = pygame.sprite.spritecollide(player, ghosts, False)
    if ghosts_hit:
        running = False  # Spillet slutter hvis spilleren treffer et spøkelse


    # Tegner alt
    screen.fill(BLACK)
    safezones.draw(screen)#tegner denne spesifikt før alt det andre (layering)
    all_sprites.draw(screen)
    pygame.display.flip()

# Avslutter Pygame
pygame.quit()

'''brukte Chat-GPT for å jobbe med den uvandte kollisjonstypen
og det grunnleggende rammeverket, men endret veldig mye etter 
det så koden ser ikke veldig lik ut'''