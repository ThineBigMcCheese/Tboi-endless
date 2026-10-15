import pygame
pygame.init()
font = pygame.font.Font(None, 36)

win = pygame.display.set_mode((693, 465))

pygame.display.set_caption("The saacening")
x = 200
y = 300
width = 80
height = 120
color = (46, 189, 209)
vel = 5
left = False
right = False
up = False
down = False
walkCount = 0
tearCooldown = 0
playerHealth = 10
damageCooldown = 0


#animation steps
walkRight = [pygame.image.load('I_walk1_right.png'), pygame.image.load('I_walk2_right.png'), pygame.image.load('I_walk3_right.png')]
walkLeft = [pygame.image.load('I_walk1_left.png'), pygame.image.load('I_walk2_left.png'), pygame.image.load('I_walk3_left.png')]
walkUp = [pygame.image.load('I_walk1_up.png'), pygame.image.load('I_walk2_up.png'), pygame.image.load('I_walk3_up.png')]
walkDown = [pygame.image.load('I_walk1.png'), pygame.image.load('I_idle.png'), pygame.image.load('I_walk2.png')]
bg = pygame.image.load('Room.png')
char = pygame.image.load('I_idle.png')

clock = pygame.time.Clock()

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.walkCount = 0
        self.hitbox = pygame.Rect(self.x, self.y + 2, 28, 33)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        self.hitbox = pygame.Rect(self.x, self.y + 11, 29, 52)

tears = []

class enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.health = 3
        self.alive = True

        # enemy hitbox
        self.hitbox = pygame.Rect(self.x, self.y + 2, 28, 33)

    def update(self):
        if self.alive:
            self.move()

            # keep hitbox attached to enemy
            self.hitbox.topleft = (self.x, self.y + 2)

    def draw(self, win):
        if self.alive:
            # draw enemy
            win.blit(Enemy, (self.x, self.y))

    def move(self):

        # move to player
        dx = x - self.x
        dy = y - self.y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance != 0:
            dx /= distance
            dy /= distance

        # prevent enemy stacking
        separation_x = 0
        separation_y = 0

        for other in enemies:
            if other is self or not other.alive:
                continue

            enemy_dx = self.x - other.x
            enemy_dy = self.y - other.y

            enemy_distance = (enemy_dx ** 2 + enemy_dy ** 2) ** 0.5

            # how close enemies can get
            separation_distance = 25

            if 0 < enemy_distance < separation_distance:
                enemy_dx /= enemy_distance
                enemy_dy /= enemy_distance

                separation_x += enemy_dx
                separation_y += enemy_dy

        # combine chasing and separation
        dx += separation_x * 1.1
        dy += separation_y * 1.1

        # normalise final movement
        movement_distance = (dx ** 2 + dy ** 2) ** 0.5

        if movement_distance != 0:
            dx /= movement_distance
            dy /= movement_distance

            self.x += dx * self.vel
            self.y += dy * self.vel

    def hit(self):
        print("hit")
        self.health -= 1
        print("Enemy health:", self.health)

        if self.health <= 0:
            self.alive = False
            print("Enemy killed!")

Enemy = pygame.image.load('enemy.png')
enemies = []
for i in range(20):
    enemies.append(enemy(320, 100, 64, 64))

class Tear:
    def __init__(self, x, y, radius, color, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, win):
        pygame.draw.circle(win,self.color,(int(self.x), int(self.y)),self.radius)
        
def redrawGameWindow():
    global walkCount

    win.blit(bg, (0,0))
    for enemy in enemies:
        enemy.draw(win)
    for tear in tears:
        tear.draw(win)
    if walkCount + 1 >= 9:
        walkCount = 0
        
    if left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    elif up:
        win.blit(walkUp[walkCount//3], (x,y))
        walkCount += 1
    elif down:
        win.blit(walkDown[walkCount//3], (x,y))
        walkCount += 1        
    else:
        win.blit(char, (x, y))

    healthText = font.render(
    "Health: " + str(playerHealth),True,(255, 255, 255))

    win.blit(healthText, (20, 20))
        
    pygame.display.update() 

run = True

while run:
    clock.tick(30)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # check which keys are currently held
    keys = pygame.key.get_pressed()

    if tearCooldown > 0:
        tearCooldown -= 1
    if damageCooldown > 0:
        damageCooldown -= 1

    if keys[pygame.K_UP] and tearCooldown == 0:
        tears.append(Tear(x + 14,y + 10,6,(46, 189, 209),0,-8))

        tearCooldown = 10

    if keys[pygame.K_DOWN] and tearCooldown == 0:
        tears.append(Tear(x + 14,y + 10,6,(46, 189, 209),0,+8))
    
        tearCooldown = 10

    if keys[pygame.K_LEFT] and tearCooldown == 0:
        tears.append(Tear(x + 14,y + 10,6,(46, 189, 209),-8,0))
    
        tearCooldown = 10

    if keys[pygame.K_RIGHT] and tearCooldown == 0:
        tears.append(Tear(x + 14,y + 10,6,(46, 189, 209),+8,0))
    
        tearCooldown = 10

    dx = 0
    dy = 0

    if keys[pygame.K_a] and x > 65:
        dx -= 1

    if keys[pygame.K_d] and x < 600:
        dx += 1

    if keys[pygame.K_w] and y > 50:
        dy -= 1

    if keys[pygame.K_s] and y < 355:
        dy += 1

    # normalise diagonal movement
    if dx != 0 or dy != 0:
        length = (dx ** 2 + dy ** 2) ** 0.5

        dx = dx / length
        dy = dy / length

        x += dx * vel
        y += dy * vel

    if dx < 0:
        left = True
        right = False
        up = False
        down = False

    elif dx > 0:
        left = False
        right = True
        up = False
        down = False

    elif dy < 0:
        left = False
        right = False
        up = True
        down = False

    elif dy > 0:
        left = False
        right = False
        up = False
        down = True

    else:
        left = False
        right = False
        up = False
        down = False
        walkCount = 0

    # update enemy position and hitbox
    player_hitbox = pygame.Rect(x, y + 11, 29, 52)

    for enemy in enemies:
        enemy.update()

    # check enemy collision with player
    for enemy in enemies:
        if enemy.alive and enemy.hitbox.colliderect(player_hitbox):
            if damageCooldown == 0:
                playerHealth -= 1
                damageCooldown = 30
                print("Player health:", playerHealth)
                if playerHealth <= 0:
                    print("Player died!")
                    run = False

    # check tears for collision with enemy
    for tear in tears[:]:
        tear.update()

        tear_rect = pygame.Rect(
            tear.x - tear.radius,
            tear.y - tear.radius,
            tear.radius * 2,
            tear.radius * 2
        )

        for enemy in enemies:
            if enemy.alive and tear_rect.colliderect(enemy.hitbox):
                enemy.hit()
                tears.remove(tear)
                break
    enemies = [enemy for enemy in enemies if enemy.alive]

    redrawGameWindow()

pygame.quit()