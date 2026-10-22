from settings import * 
from sprites import *
from groups import AllSprites
from support import *
from timer import Timer
from  random import randint



class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #load game
        self.load_assets()
        self.setup()

        #timer
        self.bee_timer = Timer(500, func = self.create_bee, autostart = True, repeat = True)

    #create 

    def create_bee(self):
        Bee(pos = ((self.level_width + WINDOW_WIDTH), randint(0,self.level_height)), 
            frames = self.bee_frames, 
            groups = (self.all_sprites, self.enemy_sprites),
            speed = randint(300,500))

    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos, self.all_sprites, self.player)
        self.audio['shoot'].play().set_volume(0.3)

    def load_assets(self):
        #graphics 
        self.player_frames = import_folder('images', 'player')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')

        #sounds
        self.audio = audio_importer('audio')

    def setup(self):
        #get the layer and tiles in map file
        tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))
        
        self.level_width = tmx_map.width * TILE_SIZE        
        self.level_height = tmx_map.height * TILE_SIZE
        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            #set up sprite to hold x and y coords and your groups 
            #x and y are coordinates as in the map file so need to multiply by tile size to get as pixels 
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))
        #do the same to call in the decorations for the map, removing the collision sprite as you should collide with background
        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))
        #now i need objects on map so call them from the file
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            if obj.name == 'Worm':
                Worm(pygame.FRect(obj.x, obj.y, obj.width, obj.height), self.worm_frames, (self.all_sprites, self.enemy_sprites))  

        self.audio['music'].play(loops= -1).set_volume(0.3)

    def collision(self):
        #bu9llet and enemy
        for bullet in self.bullet_sprites:
            sprite_collisions = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collisions:
                self.audio['impact'].play().set_volume(0.3)
                bullet.kill()
                for sprite in sprite_collisions:
                    sprite.destroy()

        # enemies collide with player
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)#passes player coords to draw function in groups.py
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 