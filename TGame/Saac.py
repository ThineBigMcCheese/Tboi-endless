import pygame
pygame.init()

win = pygame.display.set_mode((693, 465))

pygame.display.set_caption("The saacening")
x = 200
y = 300
width = 80
height = 120
vel = 5
left = False
right = False
up = False
down = False
walkCount = 0

#animation steps
walkRight = [pygame.image.load('I_walk1_right.png'), pygame.image.load('I_walk2_right.png'), pygame.image.load('I_walk3_right.png')]
walkLeft = [pygame.image.load('I_walk1_left.png'), pygame.image.load('I_walk2_left.png'), pygame.image.load('I_walk3_left.png')]
walkUp = [pygame.image.load('I_walk1_up.png'), pygame.image.load('I_walk2_up.png'), pygame.image.load('I_walk3_up.png')]
walkDown = [pygame.image.load('I_walk1.png'), pygame.image.load('I_idle.png'), pygame.image.load('I_walk2.png')]
bg = pygame.image.load('Room.png')
char = pygame.image.load('I_idle.png')

clock = pygame.time.Clock()

class tear(object):
    def__init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
        
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawGameWindow():
    global walkCount
    
    win.blit(bg, (0,0))
    
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
        
    pygame.display.update() 

run = True

while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    dx = 0
    dy = 0    

    # get movement direction
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

    redrawGameWindow() 

pygame.quit()