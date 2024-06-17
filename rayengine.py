import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200 

SCREEN_HEIGHT = 900

PLAYER_COLOR = (0, 128, 255)
BACKGROUND_COLOR = (80, 80, 80)
FPS = 60
WALL_COLOUR = (200,200,200)
FLOOR_COLOUR = (0,0,0)
TILE_SIZE = 60
PLAYER_RADIUS = TILE_SIZE/4
VIEWPRES = 0.4
FOV = 60
mapa = [
    [1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,1],
    [1,1,1,1,0,1,0,1],
    [1,0,0,1,0,1,0,1],
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
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_COLOR, (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.angle = 0

    def draw_direction_line(self, screen):
        radian_angle = np.radians(self.angle)
        start_pos = self.rect.center
        end_pos = (
            start_pos[0] + TILE_SIZE * np.cos(radian_angle),
            start_pos[1] + TILE_SIZE * np.sin(radian_angle)
        )
        pygame.draw.line(screen, (0,250,0), start_pos, end_pos, 2)
    
    def draw_rays(self, screen):
        raylist = []
        fov = FOV
        xpos, ypos = self.rect.center
        for i in range(fov + 1):
            rot_d = np.radians(self.angle) + np.radians(i - fov / 2)
            x, y = xpos, ypos
            sin, cos = VIEWPRES * np.sin(rot_d), VIEWPRES * np.cos(rot_d)
            j = 0
            while True:
                x, y = x + cos, y + sin
                j += 1
                if mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)] != 0:
                    tile = mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)]
                    d = j
                    j = j * np.cos(np.radians(i - fov / 2))
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
            rot_d = np.radians(self.angle) + np.radians(i - fov / 2)
            x, y = xpos, ypos
            sin, cos = VIEWPRES * np.sin(rot_d), VIEWPRES * np.cos(rot_d)
            j = 0
            while True:
                x, y = x + cos, y + sin
                j += 1
                if mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)] != 0:
                    tile = mapa[int(y // TILE_SIZE)][int(x // TILE_SIZE)]
                    d = j
                    j = j * np.cos(np.radians(i - fov / 2))
                    height = (10 / j * 2500)
                    break
            if d / 2 > 255:
                d = 510
            pygame.draw.line(screen,(250,0,0),(xpos,ypos),(x,y),2)
    '''def draw_rays(self,screen):
        rayAngle = self.angle
        for r in range(1):
            #check horizontals
            dof = 0
            aTan = -1/np.tan(rayAngle)
            if rayAngle >np.pi:
                ry = (int(self.rect.y/TILE_SIZE)*TILE_SIZE) - 0.0001
                rx = ((self.rect.y-ry) * aTan) + self.rect.x
                yoff = -TILE_SIZE
                xoff = - yoff * aTan
            elif rayAngle < np.pi:
                ry = (int(self.rect.y/TILE_SIZE)*TILE_SIZE) +TILE_SIZE
                rx = ((self.rect.y-ry) * aTan) + self.rect.x
                yoff = TILE_SIZE
                xoff = - yoff * aTan
            if rayAngle == 0 or rayAngle == np.pi:
                
                rx = self.rect.x
                ry = self.rect.y
                dof = 8
            while dof<8:
                mx = int(int(rx) // TILE_SIZE) % 8
                my = int(int(ry) // TILE_SIZE) % 8

                mp = my*8*TILE_SIZE + mx
                if mp < 8*8*TILE_SIZE*TILE_SIZE and mapa[mx][my] ==1 and mp > 0:
                    dof = 8
                else:
                    rx += xoff
                    ry += yoff
                    dof += 1
        pygame.draw.line(screen, (250,0,0), self.rect.center, (rx,ry), 2)'''
            


    

        

    def update(self, keys):
        if keys[pygame.K_a]:
            self.angle -= VIEWPRES
        if keys[pygame.K_d]:
            self.angle += VIEWPRES

        radian_angle = np.radians(self.angle)

        if keys[pygame.K_w]:
            new_x = self.rect.x + (self.speed * np.cos(radian_angle))
            new_y = self.rect.y + (self.speed * np.sin(radian_angle))
            if self.can_move(new_x, new_y):
                self.rect.x = new_x
                self.rect.y = new_y

        if keys[pygame.K_s]:
            new_x = self.rect.x - (self.speed * np.cos(radian_angle))
            new_y = self.rect.y - (self.speed * np.sin(radian_angle))
            if self.can_move(new_x, new_y):
                self.rect.x = new_x
                self.rect.y = new_y

        if keys[pygame.K_LEFT]:
            new_x = self.rect.x - self.speed
            if self.can_move(new_x, self.rect.y):
                self.rect.x = new_x
        if keys[pygame.K_RIGHT]:
            new_x = self.rect.x + self.speed
            if self.can_move(new_x, self.rect.y):
                self.rect.x = new_x
        if keys[pygame.K_UP]:
            new_y = self.rect.y - self.speed
            if self.can_move(self.rect.x, new_y):
                self.rect.y = new_y
        if keys[pygame.K_DOWN]:
            new_y = self.rect.y + self.speed
            if self.can_move(self.rect.x, new_y):
                self.rect.y = new_y


# Main Game Function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pygame Player Object')
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

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
