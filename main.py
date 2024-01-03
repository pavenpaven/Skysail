import pygame
from perlin_noise import PerlinNoise
import random 
import math
import src.animation as animation



pygame.init()
pygame.display.init()
pygame.font.init()

def scaler_vec_mul(k, vec):
    x,y = vec
    return x*k, y*k

def vec_add(v, w):
    x,y = v
    n,m = w
    return x+n,y+m

WIDTH = 600
HIGHT = 600
window = pygame.display.set_mode((WIDTH, HIGHT))
tile = 5
textured_tiles = 4
textu = (tile*textured_tiles, tile*textured_tiles)

textures = [animation.Animation.from_dir("Art/Skysail_sea", textu, 16),
            animation.Animation([pygame.transform.scale(pygame.image.load("Art/sail_plain.png"), textu)], textu, 16),
            animation.Animation([pygame.transform.scale(pygame.image.load("Art/sail_sand.png"), textu)], textu, 16), 
            animation.Animation([pygame.transform.scale(pygame.image.load("Art/Skysail_Moutain.png"), textu)], textu, 16),
            animation.Animation.from_dir("Art/Skysail_forest", textu, 16)]

HOUSE = pygame.transform.scale(pygame.image.load("Art/Skysail_house.png"), textu)
HOUSEDOT = pygame.transform.scale(pygame.image.load("Art/Skysail_dot.png"), (8, 8))

waterlevel = 0.2
sand = 0.05
mountain = 0.75


FONT = pygame.font.Font(None, size=30)

def tiledetermine(hight, montaincond, forest):
    if hight < waterlevel:
        return 0
    if hight + montaincond > mountain:
        return 3
    if waterlevel + sand > hight > waterlevel: 
        return 2
    if forest + 0.5*hight > 0.4:
        return 4
    if hight > waterlevel + sand: 
        return 1


class Map:
    def __init__(self, seedd):
        self.noise_big = PerlinNoise(octaves=3, seed= seedd)
        self.noise_small = PerlinNoise(octaves=7, seed= seedd+1) 
        self.noise_very_small = PerlinNoise(octaves=12, seed= seedd+2) 

        self.montaincond_big = PerlinNoise(octaves = 3, seed = seedd+5)
        self.montaincond_small = PerlinNoise(octaves = 8, seed = seedd+6)
        self.forest_noise_big = PerlinNoise(octaves = 7, seed= seedd + 3)
        self.forest_noise_small = PerlinNoise(octaves = 13, seed= seedd + 4)
        self.forest_noise_very_big = PerlinNoise(octaves = 4, seed = seedd + 7)

        self.seedd = seedd
        self.tileMap = self.get_tilemap((0,0), 1, 240)
        self.villages = []
        for i in range(6):
            for j in range(1000):
                pos = math.floor(random.random()*240), math.floor(random.random()*240)
                if self.tileMap[pos[1]][pos[0]] == 1:
                    self.villages.append(scaler_vec_mul(1/240, pos))
                    break
        print("villages:", self.villages)
        self.map_surface = pygame.Surface((WIDTH, HIGHT))
        self.render(self.map_surface, (0,0), 1, self.get_tilemap((0,0), 1, 120), False)
       
                

    def noise_func(self, pos):
        return (self.noise_big(pos) + 0.8*self.noise_small(pos) + 0.6*self.noise_very_small(pos), 
                 0.7*self.montaincond_big(pos) + self.montaincond_small(pos),
                 self.forest_noise_big(pos) + self.forest_noise_small(pos) + 0.5*self.forest_noise_small(pos))
        
        
    def get_tilemap(self, pos, size, num_tiles):
        self.pic = [[self.noise_func((j/num_tiles + pos[0], i/num_tiles + pos[1])) for j in range(num_tiles)] for i in range(num_tiles)]

        return [[tiledetermine(*j) for j in i] for i in self.pic]

    def connect(tileMap):
        pass
    
    def render(self, window, pos, size , tileMap, textured = False, framecount = 0):
        pos = scaler_vec_mul(1/8, pos)
        for n,i in enumerate(tileMap): 
            for m,j in enumerate(i): 
                if not textured:
                    if j == 1: 
                        pygame.draw.rect(window, (0, 200, 0), pygame.Rect((tile*n, tile*m), (tile, tile)))  
                    if j == 0: 
                        pygame.draw.rect(window, (0x2f, 0x36, 0x99), pygame.Rect((tile*n, tile*m), (tile, tile))) 
                    if j == 2: 
                        pygame.draw.rect(window, (0xf5, 0xb7, 0x77), pygame.Rect((tile*n, tile*m), (tile, tile)))
                    if j == 3:
                        pygame.draw.rect(window, (100,100,100), pygame.Rect((tile*n, tile*m), (tile, tile)))
                    if j == 4:
                        pygame.draw.rect(window, (0, 100, 0), pygame.Rect((tile*n, tile*m), (tile, tile)))
                else:
                    textures[j].update(framecount)
                    window.blit(textures[j].texture, (tile*textured_tiles*n, tile*textured_tiles*m))
        if not textured:
            for i in range(0, 8):
                pygame.draw.line(window, (0,0,0) ,(0, round(600/8)*i), (600, round(600/8)*i))
                pygame.draw.line(window, (0,0,0),(round(600/8)*i, 0), (round(600/8)*i, 600))
        for i in self.villages:
            i = (i[1], i[0])
            if not textured:
                window.blit(HOUSEDOT, vec_add(scaler_vec_mul(600, i), (-4, -4)))
            else:
                if pos[0] <= i[0] <= pos[0]+ 1/size and pos[1] <= i[1] <= pos[1] + 1/size:
                    window.blit(HOUSE, scaler_vec_mul(600*8, vec_add((-pos[0], -pos[1]), i)))
        window.blit(FONT.render(str(self.seedd), False, (0,0,0), None), (1,1))
        

def main():
    scene = Map(random.randint(1,10000))
    window.blit(scene.map_surface, (0,0))
    running = True
    textured = False
    size = 1
    pos = (0,0)
    clock = pygame.time.Clock()
    tileMap = []
    framecount = 0
    tick = 0
    while running:
        framecount+= 1
        if not framecount%10:
            tick+=1
        clock.tick(30)
        events = pygame.event.get()
        window.blit(FONT.render(f"tick: {tick}", False, (0,0,0), None), (100, 0)) 
        pygame.display.update()
        if not textured:
            window.blit(scene.map_surface, (0,0))
        if textured:
            scene.render(window, scaler_vec_mul(1/30, pos), size, tileMap, True, framecount)
        for i in events:
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    print("mouse_pos:", i.pos)
                    x,y = vec_add(pos, scaler_vec_mul(1/(size*600), i.pos))
                    pos =math.floor(x*8), math.floor(y*8)
                    pos = scaler_vec_mul(30, pos)
                    tileMap = list(map(lambda x: x[pos[1]:pos[1]+ 30], scene.tileMap[pos[0]:pos[0]+30]))
                    size *= 8
                    textured = True
                    #pos = vec_add((-1/(size*2), -1/(size*2)), pos)
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_z:
                    size = 1
                    pos = (0,0)
                    textured = False
                    window.blit(scene.map_surface, (0,0))
                if i.key == pygame.K_w:
                    pos = vec_add(pos, (0,-1))
                    tileMap = list(map(lambda x: x[pos[1]:pos[1]+30], scene.tileMap[pos[0]:pos[0]+30]))
                if i.key == pygame.K_s:
                    pos = vec_add(pos, (0,1))
                    tileMap = list(map(lambda x: x[pos[1]:pos[1]+30], scene.tileMap[pos[0]:pos[0]+30]))
                if i.key == pygame.K_d:
                    pos = vec_add(pos, (1,0))
                    tileMap = list(map(lambda x: x[pos[1]:pos[1]+30], scene.tileMap[pos[0]:pos[0]+30]))
                if i.key == pygame.K_a:
                    pos = vec_add(pos, (-1,0))
                    tileMap = list(map(lambda x: x[pos[1]:pos[1]+30], scene.tileMap[pos[0]:pos[0]+30]))
                                       
                if i.key == pygame.K_t:
                    size = 1
                    pos = (0,0)
                    scene = Map(random.randint(1,10000))
                    textured = False
                    window.blit(scene.map_surface, (0,0))

                    
                
            if i.type == pygame.QUIT:
                pygame.quit()
                running = False 
            
main()
