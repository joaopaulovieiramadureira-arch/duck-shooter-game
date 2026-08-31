import pygame
import math
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.damage = PLAYER_DAMAGE
        self.speed = PLAYER_SPEED
        self.size = PLAYER_SIZE
        
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw_duck()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        self.aim_angle = 0
        
    def draw_duck(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 0), (self.size // 2, self.size // 2), self.size // 2 - 2)
        pygame.draw.circle(self.image, (0, 0, 0), (self.size // 2 + 5, self.size // 2 - 3), 3)
        pygame.draw.polygon(self.image, (255, 165, 0), [
            (self.size - 5, self.size // 2 - 2),
            (self.size - 5, self.size // 2 + 2),
            (self.size, self.size // 2)
        ])
    
    def update(self, mouse_pos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y > self.size // 2:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < SCREEN_HEIGHT - self.size // 2:
            self.y += self.speed
        if keys[pygame.K_a] and self.x > self.size // 2:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < SCREEN_WIDTH - self.size // 2:
            self.x += self.speed
        
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.aim_angle = math.atan2(dy, dx)
        
        self.rect.center = (self.x, self.y)
    
    def shoot(self):
        proj_x = self.x + math.cos(self.aim_angle) * (self.size // 2)
        proj_y = self.y + math.sin(self.aim_angle) * (self.size // 2)
        return proj_x, proj_y, self.aim_angle
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
    
    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10
        
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        font = pygame.font.Font(None, 16)
        text = font.render(f"HP: {int(self.health)}/{int(self.max_health)}", True, (255, 255, 255))
        screen.blit(text, (bar_x + 5, bar_y + 2))
