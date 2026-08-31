import pygame
import math
from config import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage=PROJECTILE_DAMAGE):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = PROJECTILE_SPEED
        self.size = PROJECTILE_SIZE
        self.damage = damage
        
        # Create sprite (orange/red fire ball)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 100, 0), (self.size // 2, self.size // 2), self.size // 2)
        pygame.draw.circle(self.image, (255, 200, 0), (self.size // 2, self.size // 2), self.size // 3)
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.rect.center = (self.x, self.y)
        
        # Remove if off screen
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.kill()

class SoundBomb(pygame.sprite.Sprite):
    """Mini sound bomb dropped by flying enemies in phase 3+"""
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = 12
        self.damage = 5
        self.speed_y = 3
        
        # Create sprite (purple/blue bomb)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (100, 50, 200), (self.size // 2, self.size // 2), self.size // 2)
        pygame.draw.circle(self.image, (150, 100, 255), (self.size // 2 - 2, self.size // 2 - 2), self.size // 3)
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self):
        self.y += self.speed_y
        self.rect.center = (self.x, self.y)
        
        # Remove if off screen
        if self.y > SCREEN_HEIGHT:
            self.kill()
