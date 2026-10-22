from settings import *

#set up our moving camera
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        #this controls math behind camera movement
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH/2)#calculates the middle of the screen horizontally
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT/2)#does the same vertically to get the central coords
        #target_pos tells pygame how far i have walked off center
        #since we calculate how far off centre the character has moved to match that we need the inverse hence '-'

        for sprite in self:
            #this goes through every sprite in the game (literally everything from player and enemies to background objects)
            #and reblits the shifted by the above calculated offset to keep character in middle of screen
            #moving the world round the chtracter insted of the character round the world
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
                                  
        
    