import pygame
import math
import random
from config import *
from player import Player
from enemies import Insect, FlyingEnemy, Roller, BigRoller, FlyingBomber, Boss
from projectiles import Projectile, SoundBomb

class GameState:
    def __init__(self):
        self.phase = 1
        self.loop_counter = 0
        self.player_alive = True
        self.phase_complete = False
        self.victory = False
        self.game_over = False

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Duck Shooter - 5 Phases")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.state = GameState()
        self.setup_phase()
    
    def setup_phase(self):
        """Setup current phase"""
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.boss = None
        
        # Apply difficulty multiplier
        diff_mult = DIFFICULTY_MULTIPLIER.get(self.state.loop_counter, 2.0)
        dmg_mult = DAMAGE_MULTIPLIER.get(self.state.loop_counter, 1.4)
        
        self.player.health = PLAYER_HEALTH * diff_mult
        self.player.max_health = self.player.health
        
        # Setup enemies based on phase
        if self.state.phase == 1:
            # 2 insects + 1 flying enemy
            self.enemies.add(Insect(200, 150))
            self.enemies.add(Insect(1000, 150))
            self.enemies.add(FlyingEnemy(SCREEN_WIDTH // 2, 200))
        
        elif self.state.phase == 2:
            # 2 flying bombers + 1 roller
            bomber1 = FlyingBomber(300, 150, ENEMY_HEALTH_BASE * diff_mult)
            bomber2 = FlyingBomber(900, 150, ENEMY_HEALTH_BASE * diff_mult)
            roller = Roller(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200, ENEMY_HEALTH_ROLLER * diff_mult)
            self.enemies.add(bomber1, bomber2, roller)
        
        elif self.state.phase == 3:
            # 2 rollers (opposite sides) + 1 flying bomber
            roller1 = Roller(150, SCREEN_HEIGHT - 150, ENEMY_HEALTH_ROLLER * diff_mult)
            roller2 = Roller(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, ENEMY_HEALTH_ROLLER * diff_mult)
            bomber = FlyingBomber(SCREEN_WIDTH // 2, 150, ENEMY_HEALTH_BASE * diff_mult)
            self.enemies.add(roller1, roller2, bomber)
            roller1.direction = 1
            roller2.direction = -1
        
        elif self.state.phase == 4:
            # 1 flying bomber + 1 big roller
            bomber = FlyingBomber(SCREEN_WIDTH // 2, 150, ENEMY_HEALTH_BASE * diff_mult)
            big_roller = BigRoller(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            big_roller.health = ENEMY_HEALTH_BIG_ROLLER * diff_mult
            big_roller.max_health = big_roller.health
            self.enemies.add(bomber, big_roller)
        
        elif self.state.phase == 5:
            # Boss battle
            self.boss = Boss(SCREEN_WIDTH // 2, 150)
            self.boss.health = BOSS_HEALTH * diff_mult
            self.boss.max_health = self.boss.health
            self.boss.damage = BOSS_DAMAGE * dmg_mult
        
        self.state.phase_complete = False
        self.shoot_cooldown = 0
        self.door_timer = 0
        self.transition_timer = 0
        self.show_transition = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to shoot
                    if self.shoot_cooldown <= 0:
                        self.shoot()
                        self.shoot_cooldown = 10
        return True
    
    def shoot(self):
        """Player shoots"""
        proj_x, proj_y, angle = self.player.shoot()
        projectile = Projectile(proj_x, proj_y, angle, self.player.damage)
        self.projectiles.add(projectile)
    
    def update(self):
        if self.state.phase_complete or self.state.game_over or self.state.victory:
            return
        
        self.shoot_cooldown -= 1
        
        # Update player
        mouse_pos = pygame.mouse.get_pos()
        self.player.update(mouse_pos)
        
        # Update projectiles
        self.projectiles.update()
        self.bombs.update()
        
        # Update enemies
        if self.state.phase == 5:
            if self.boss:
                self.boss.update(self.player)
                
                # Boss shoots
                if self.boss.should_shoot():
                    boss_proj_x, boss_proj_y, boss_angle = self.boss.shoot()
                    projectile = Projectile(boss_proj_x, boss_proj_y, boss_angle, self.boss.damage)
                    self.projectiles.add(projectile)
        else:
            for enemy in self.enemies:
                if isinstance(enemy, FlyingEnemy):
                    enemy.update(self.player)
                elif isinstance(enemy, FlyingBomber):
                    enemy.update()
                    if enemy.should_drop_bomb():
                        bomb = SoundBomb(enemy.x, enemy.y)
                        self.bombs.add(bomb)
                else:
                    enemy.update()
        
        # Check collisions: Player projectiles vs Enemies
        for projectile in self.projectiles:
            if self.state.phase == 5 and self.boss:
                if pygame.sprite.spritecollide(projectile, pygame.sprite.Group(self.boss), False):
                    if self.boss.take_damage(projectile.damage):
                        self.boss = None
                        self.state.phase_complete = True
                    projectile.kill()
            else:
                hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies, False)
                for enemy in hit_enemies:
                    if enemy.take_damage(projectile.damage):
                        enemy.kill()
                    projectile.kill()
                    break
        
        # Check collisions: Bombs vs Player
        for bomb in self.bombs:
            if pygame.sprite.spritecollide(bomb, pygame.sprite.Group(self.player), False):
                if self.player.take_damage(bomb.damage):
                    self.state.player_alive = False
                    self.state.game_over = True
                bomb.kill()
        
        # Check collisions: Enemies vs Player (take damage)
        if self.state.phase != 5:
            for enemy in self.enemies:
                if pygame.sprite.spritecollide(enemy, pygame.sprite.Group(self.player), False):
                    if not isinstance(enemy, Roller) or (isinstance(enemy, Roller) and enemy.is_rolling) or (isinstance(enemy, BigRoller) and enemy.is_rolling):
                        if self.player.take_damage(enemy.damage):
                            self.state.game_over = True
        else:
            if self.boss and pygame.sprite.spritecollide(self.boss, pygame.sprite.Group(self.player), False):
                if self.player.take_damage(self.boss.damage):
                    self.state.game_over = True
        
        # Check boss projectiles vs player
        boss_projectiles = [p for p in self.projectiles if hasattr(p, 'angle')]
        for projectile in boss_projectiles:
            if pygame.sprite.spritecollide(projectile, pygame.sprite.Group(self.player), False):
                if self.player.take_damage(projectile.damage):
                    self.state.game_over = True
                projectile.kill()
        
        # Check if phase complete
        if not self.state.phase_complete:
            if self.state.phase == 5:
                if not self.boss:
                    self.state.phase_complete = True
            else:
                if len(self.enemies) == 0:
                    self.state.phase_complete = True
    
    def draw(self):
        # Draw background
        colors = PHASE_COLORS[self.state.phase]
        bg_color = colors["background"]
        ground_color = colors["ground"]
        
        self.screen.fill(bg_color)
        
        # Draw ground
        pygame.draw.rect(self.screen, ground_color, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Draw player
        self.screen.blit(self.player.image, self.player.rect)
        self.player.draw_health_bar(self.screen)
        
        # Draw aim line
        end_x = self.player.x + math.cos(self.player.aim_angle) * 100
        end_y = self.player.y + math.sin(self.player.aim_angle) * 100
        pygame.draw.line(self.screen, (255, 255, 0), (self.player.x, self.player.y), (end_x, end_y), 2)
        
        # Draw enemies
        for enemy in self.enemies:
            self.screen.blit(enemy.image, enemy.rect)
            enemy.draw_health_bar(self.screen)
        
        # Draw boss
        if self.state.phase == 5 and self.boss:
            self.screen.blit(self.boss.image, self.boss.rect)
            self.boss.draw_health_bar(self.screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            self.screen.blit(projectile.image, projectile.rect)
        
        # Draw bombs
        for bomb in self.bombs:
            self.screen.blit(bomb.image, bomb.rect)
        
        # Draw phase info
        phase_text = f"Phase: {self.state.phase}/5  Loop: {self.state.loop_counter + 1}"
        text = self.small_font.render(phase_text, True, (255, 255, 255))
        self.screen.blit(text, (SCREEN_WIDTH - 300, 10))
        
        # Draw phase complete message
        if self.state.phase_complete and self.state.phase < 5:
            msg_text = self.font.render("Phase Complete! Click Door to Continue", True, (0, 255, 0))
            self.screen.blit(msg_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2))
            
            # Draw door
            door_x = SCREEN_WIDTH // 2
            door_y = SCREEN_HEIGHT // 2 + 80
            pygame.draw.rect(self.screen, (139, 69, 19), (door_x - 40, door_y - 60, 80, 120))
            pygame.draw.circle(self.screen, (255, 215, 0), (door_x + 25, door_y), 8)
        
        # Draw victory message
        if self.state.phase == 5 and self.state.phase_complete:
            if self.state.loop_counter == 0:
                msg_text = self.font.render("Victory! Click to Continue for Loop 2", True, (255, 215, 0))
            else:
                msg_text = self.font.render("Final Victory! You Win!", True, (255, 215, 0))
            self.screen.blit(msg_text, (SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2))
        
        # Draw game over message
        if self.state.game_over:
            msg_text = self.font.render("GAME OVER! Press ESC to Quit", True, (255, 0, 0))
            self.screen.blit(msg_text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    def handle_phase_complete(self):
        """Handle phase completion and transitions"""
        if not self.state.phase_complete:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        if self.state.phase < 5:
            # Check if clicked on door
            door_x = SCREEN_WIDTH // 2
            door_y = SCREEN_HEIGHT // 2 + 80
            door_rect = pygame.Rect(door_x - 40, door_y - 60, 80, 120)
            
            if door_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
                self.state.phase += 1
                self.setup_phase()
        else:
            # Phase 5 complete
            if self.state.loop_counter == 0:
                # Go to loop 2
                if mouse_pressed[0]:
                    self.state.loop_counter += 1
                    self.state.phase = 1
                    self.setup_phase()
            else:
                self.state.victory = True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if not self.state.game_over and not self.state.victory:
                self.update()
                self.handle_phase_complete()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
