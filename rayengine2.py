import pygame
import sys
import numpy as np
import math as m

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200 

SCREEN_HEIGHT = 900

PLAYER_COLOR = (0, 128, 255)
BACKGROUND_COLOR = (80, 80, 80)
FPS = 200
WALL_COLOUR = (200,200,200)
FLOOR_COLOUR = (30,0,0)
TILE_SIZE = 60
PLAYER_RADIUS = TILE_SIZE/4
VIEWPRES = 1
FOV = 60
mapa = [
    [1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,1],
    [1,0,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1]
]
def draw_map(screen, map_layout):
    for row_index, row in enumerate(map_layout):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == 0:
                color = FLOOR_COLOUR
            elif tile == 1:
                color = WALL_COLOUR
            
            pygame.draw.rect(screen, color, pygame.Rect(x, y, TILE_SIZE-1, TILE_SIZE-1))

class floatySprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.floatPosition = (x, y) # or the "true" position

    def updateRect(self, rect):
        self.rect.x = self.floatPosition[0]
        self.rect.y = self.floatPosition[1]

    def setPosition(self, newPosition):
        self.floatPosition = newPosition

    def setX(self, newX):
        self.floatPosition = (newX, self.floatPosition[1])

    def setY(self, newY):
        self.floatPosition = (self.floatPosition[0], newY)

    def getX(self):
        return self.floatPosition[0]
    
    def getY(self):
        return self.floatPosition[1]
    
class Player(floatySprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_COLOR, (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.angle = 0

    def draw_direction_line(self, screen):
        radian_angle = m.radians(self.angle)
        start_pos = self.rect.center
        end_pos = (
            start_pos[0] + TILE_SIZE * m.cos(radian_angle),
            start_pos[1] + TILE_SIZE * m.sin(radian_angle)
        )
        pygame.draw.line(screen, (0,250,0), start_pos, end_pos, 2)
    
    def draw_rays(self, screen):
        raylist = []
        fov = FOV
        xpos, ypos = self.rect.center
        for i in range(fov + 1):
            rot_d = m.radians(self.angle) + m.radians(i - fov / 2)
            x, y = xpos, ypos
            sin, cos = VIEWPRES * m.sin(rot_d), VIEWPRES * m.cos(rot_d)
            j = 0
            while True:
                x, y = x + cos, y + sin
                j += 1
                if mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)] != 0:
                    tile = mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)]
                    d = j
                    j = j * m.cos(m.radians(i - fov / 2))
                    height = (10 / j * 2500)
                    break
            if d / 2 > 255:
                d = 510
            pygame.draw.line(screen,
                             (255 - d / 2, 255 - d / 2, 255 - d / 2),  # color
                             (i * (SCREEN_WIDTH / fov), (SCREEN_HEIGHT / 2) + height),  # pos 1
                             (i * (SCREEN_WIDTH / fov), (SCREEN_HEIGHT / 2) - height),  # pos 2
                             width=int(SCREEN_WIDTH / fov))
            
    def can_move(self, new_x, new_y):
        # Check if new position collides with a wall
        if mapa[int(new_y // TILE_SIZE)][int(new_x // TILE_SIZE)] == 1:
            return False
        return True
    
    def draw_map_rays(self,screen):
        fov = FOV
        xpos, ypos = self.rect.center
        for i in range(fov + 1):
            rot_d = m.radians(self.angle) + m.radians(i - fov / 2)
            x, y = xpos, ypos
            sin, cos = VIEWPRES * m.sin(rot_d), VIEWPRES * m.cos(rot_d)
            j = 0
            while True:
                x, y = x + cos, y + sin
                j += 1
                if mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)] != 0:
                    tile = mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)]
                    d = j
                    j = j * m.cos(m.radians(i - fov / 2))
                    height = (10 / j * 2500)
                    break
            if d / 2 > 255:
                d = 510
            pygame.draw.line(screen,(250,0,0),(xpos,ypos),(x,y),2)

    def update(self, keys):
        # Change angle based on left and right key presses or A and D
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle -= VIEWPRES
            
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += VIEWPRES

        update_speed = 0

        # Go forward or backward based on W and S key presses, in direction player is facing
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            update_speed = self.speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            update_speed = -self.speed

        radian_angle = m.radians(self.angle)
        dx = update_speed * m.cos(radian_angle)
        dy = update_speed * m.sin(radian_angle)

        new_x = self.getX() + dx
        new_y = self.getY() + dy    

        print(new_x, new_y, self.can_move(new_x, new_y))

        if self.can_move(new_x, new_y):
            self.setX(new_x)
            self.setY(new_y)
            self.updateRect(self.rect)

# Main Game Function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    

    player = Player(TILE_SIZE*1.5, TILE_SIZE*1.5)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        all_sprites.update(keys)

        screen.fill(BACKGROUND_COLOR)
        
        
        
        
        
        
        player.draw_rays(screen)
        draw_map(screen,mapa)
        all_sprites.draw(screen)
        #pygame.draw.line(screen,(250,0,0),(a,b),(c,d),2)
        
        player.draw_map_rays(screen)
        player.draw_direction_line(screen)
        pygame.display.flip()

        clock.tick(FPS)
        pygame.display.set_caption(f'Pygame Player Object. FPS: {int(clock.get_fps())} ')

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
