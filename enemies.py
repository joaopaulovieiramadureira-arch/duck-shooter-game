import pygame
import math
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    """Base enemy class"""
    def __init__(self, x, y, health=ENEMY_HEALTH_BASE, enemy_type="insect"):
        super().__init__()
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.damage = 1
        self.size = 25
        self.enemy_type = enemy_type
        
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def draw_health_bar(self, screen):
        bar_width = 30
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size // 2 - 10
        
        if bar_y < 0:
            bar_y = self.y + self.size // 2 + 5
        
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

class Insect(Enemy):
    """Phase 1: Walks randomly, doesn't follow"""
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_HEALTH_BASE, "insect")
        self.speed = INSECT_SPEED
        self.direction = random.uniform(0, 2 * math.pi)
        self.change_direction_timer = 0
        self.draw_insect()
    
    def draw_insect(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, (139, 69, 19), (5, 8, 15, 12))
        pygame.draw.circle(self.image, (101, 50, 15), (12, 5), 4)
        for i in range(3):
            pygame.draw.line(self.image, (139, 69, 19), (8 + i * 3, 15), (5 + i * 2, 22), 2)
            pygame.draw.line(self.image, (139, 69, 19), (15 + i * 2, 15), (18 + i * 2, 22), 2)
    
    def update(self):
        self.change_direction_timer += 1
        if self.change_direction_timer > 120:
            self.direction = random.uniform(0, 2 * math.pi)
            self.change_direction_timer = 0
        
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.direction = math.pi - self.direction
        if self.y < 100 or self.y > SCREEN_HEIGHT - 100:
            self.direction = -self.direction
        
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(100, min(SCREEN_HEIGHT - 100, self.y))
        
        self.rect.center = (self.x, self.y)

class FlyingEnemy(Enemy):
    """Phase 1: Flies and follows when close"""
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_HEALTH_BASE, "flying")
        self.speed = FLYING_ENEMY_SPEED
        self.follow_distance = 200
        self.direction = 0
        self.draw_flying()
    
    def draw_flying(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, (255, 0, 0), (8, 10, 9, 10))
        pygame.draw.circle(self.image, (200, 0, 0), (12, 8), 3)
        pygame.draw.circle(self.image, (255, 255, 255), (10, 7), 1)
        pygame.draw.circle(self.image, (255, 255, 255), (14, 7), 1)
        pygame.draw.polygon(self.image, (255, 100, 100), [(5, 12), (2, 8), (4, 14)])
        pygame.draw.polygon(self.image, (255, 100, 100), [(19, 12), (22, 8), (20, 14)])
    
    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance < self.follow_distance:
            self.direction = math.atan2(dy, dx)
        else:
            self.direction += random.uniform(-0.3, 0.3)
        
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        self.x = max(20, min(SCREEN_WIDTH - 20, self.x))
        self.y = max(120, min(SCREEN_HEIGHT - 120, self.y))
        
        self.rect.center = (self.x, self.y)

class Roller(Enemy):
    """Phase 2/3: Rolls back and forth, shield active while rolling"""
    def __init__(self, x, y, health=ENEMY_HEALTH_ROLLER):
        super().__init__(x, y, health, "roller")
        self.speed = ROLLER_SPEED
        self.size = 30
        self.direction = 1
        self.is_rolling = False
        self.rolling_timer = 0
        self.pause_timer = 0
        self.pause_duration = 102
        self.is_paused = True
        self.start_x = x
        self.start_y = y
        self.draw_roller()
    
    def draw_roller(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (0, 100, 255), (self.size // 2, self.size // 2), self.size // 2)
        pygame.draw.circle(self.image, (100, 150, 255), (self.size // 2 - 5, self.size // 2 - 5), self.size // 4)
        pygame.draw.line(self.image, (50, 150, 255), (self.size // 2 - 8, self.size // 2), (self.size // 2 + 8, self.size // 2), 2)
    
    def update(self):
        if self.is_paused:
            self.pause_timer += 1
            if self.pause_timer >= self.pause_duration:
                self.is_paused = False
                self.pause_timer = 0
                self.is_rolling = True
        else:
            if self.is_rolling:
                self.x += self.direction * self.speed
                
                if self.x <= 30 or self.x >= SCREEN_WIDTH - 30:
                    self.x = max(30, min(SCREEN_WIDTH - 30, self.x))
                    self.is_rolling = False
                    self.is_paused = True
        
        self.rect.center = (self.x, self.y)

class BigRoller(Enemy):
    """Phase 4: Bigger roller with smart wall bounce"""
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_HEALTH_BIG_ROLLER, "big_roller")
        self.speed = BIG_ROLLER_SPEED
        self.size = 60
        self.direction = 1
        self.is_rolling = False
        self.rolling_timer = 0
        self.pause_timer = 0
        self.pause_duration = 114
        self.is_paused = True
        self.bounce_chance = 0.58
        self.bounce_used = False
        self.draw_big_roller()
    
    def draw_big_roller(self):
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 50, 150), (self.size // 2, self.size // 2), self.size // 2)
        pygame.draw.circle(self.image, (50, 100, 200), (self.size // 2 - 10, self.size // 2 - 10), self.size // 4)
        pygame.draw.line(self.image, (100, 150, 255), (self.size // 2 - 15, self.size // 2), (self.size // 2 + 15, self.size // 2), 3)
        pygame.draw.line(self.image, (100, 150, 255), (self.size // 2, self.size // 2 - 15), (self.size // 2, self.size // 2 + 15), 3)
    
    def update(self):
        if self.is_paused:
            self.pause_timer += 1
            if self.pause_timer >= self.pause_duration:
                self.is_paused = False
                self.pause_timer = 0
                self.is_rolling = True
                self.bounce_used = False
        else:
            if self.is_rolling:
                self.x += self.direction * self.speed
                
                if self.x <= self.size // 2 or self.x >= SCREEN_WIDTH - self.size // 2:
                    self.x = max(self.size // 2, min(SCREEN_WIDTH - self.size // 2, self.x))
                    
                    if not self.bounce_used and random.random() < self.bounce_chance:
                        self.direction *= -1
                        self.bounce_used = True
                    else:
                        self.is_rolling = False
                        self.is_paused = True
        
        self.rect.center = (self.x, self.y)

class FlyingBomber(Enemy):
    """Phase 3+: Flies back and forth, drops sound bombs"""
    def __init__(self, x, y, health=ENEMY_HEALTH_BASE):
        super().__init__(x, y, health, "flying_bomber")
        self.speed = 2
        self.direction = 1
        self.bomb_timer = 0
        self.bomb_interval = 240
        self.draw_bomber()
    
    def draw_bomber(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, (200, 0, 200), (7, 8, 11, 10))
        pygame.draw.circle(self.image, (150, 0, 150), (12, 6), 3)
        pygame.draw.circle(self.image, (255, 255, 0), (10, 5), 1)
        pygame.draw.circle(self.image, (255, 255, 0), (14, 5), 1)
        pygame.draw.polygon(self.image, (200, 100, 200), [(4, 11), (1, 5), (3, 13)])
        pygame.draw.polygon(self.image, (200, 100, 200), [(20, 11), (23, 5), (21, 13)])
    
    def update(self):
        self.x += self.direction * self.speed
        
        if self.x <= 50 or self.x >= SCREEN_WIDTH - 50:
            self.direction *= -1
            self.x = max(50, min(SCREEN_WIDTH - 50, self.x))
        
        self.bomb_timer += 1
        
        self.rect.center = (self.x, self.y)
    
    def should_drop_bomb(self):
        if self.bomb_timer >= self.bomb_interval:
            self.bomb_timer = 0
            return True
        return False

class Boss(pygame.sprite.Sprite):
    """Phase 5: Intelligent boss that mirrors player behavior"""
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.damage = BOSS_DAMAGE
        self.speed = PLAYER_SPEED
        self.size = PLAYER_SIZE
        self.aim_angle = 0
        self.shoot_timer = 0
        self.shoot_interval = 30
        
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw_boss()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw_boss(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (184, 134, 11), (self.size // 2, self.size // 2), self.size // 2 - 2)
        pygame.draw.circle(self.image, (255, 0, 0), (self.size // 2 + 5, self.size // 2 - 3), 3)
        pygame.draw.polygon(self.image, (200, 0, 0), [
            (self.size - 5, self.size // 2 - 2),
            (self.size - 5, self.size // 2 + 2),
            (self.size, self.size // 2)
        ])
        for i in range(4):
            angle = (i * math.pi / 2)
            spike_x = self.size // 2 + math.cos(angle) * (self.size // 2 + 5)
            spike_y = self.size // 2 + math.sin(angle) * (self.size // 2 + 5)
            pygame.draw.line(self.image, (255, 0, 0), 
                           (self.size // 2, self.size // 2), 
                           (spike_x, spike_y), 2)
    
    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance > 150:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        elif distance < 100:
            self.x -= (dx / distance) * self.speed
            self.y -= (dy / distance) * self.speed
        
        self.x = max(self.size // 2, min(SCREEN_WIDTH - self.size // 2, self.x))
        self.y = max(120, min(SCREEN_HEIGHT - 120, self.y))
        
        dx = player.x - self.x
        dy = player.y - self.y
        self.aim_angle = math.atan2(dy, dx)
        
        self.shoot_timer += 1
        
        self.rect.center = (self.x, self.y)
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def shoot(self):
        proj_x = self.x + math.cos(self.aim_angle) * (self.size // 2)
        proj_y = self.y + math.sin(self.aim_angle) * (self.size // 2)
        return proj_x, proj_y, self.aim_angle
    
    def should_shoot(self):
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            return True
        return False
    
    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 10
        
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        font = pygame.font.Font(None, 16)
        text = font.render(f"BOSS HP: {int(self.health)}/{int(self.max_health)}", True, (255, 255, 255))
        screen.blit(text, (bar_x + 10, bar_y + 2))
