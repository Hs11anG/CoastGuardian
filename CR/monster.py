# monster.py
import pygame
import random
from settings import *
from asset_manager import assets

class Monster(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, monster_type, walkable_mask, monster_manager):
        super().__init__()
        
        self.data = MONSTER_DATA[monster_type]
        self.walkable_mask = walkable_mask
        self.max_health = self.data['health']
        # 【新增】儲存對 MonsterManager 的引用，以便回報事件
        self.manager = monster_manager

        original_image = assets.get_image(monster_type)
        size = (self.data['sizex'], self.data['sizey'])
        self.image_right = pygame.transform.scale(original_image, size)
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.facing_right = self.direction.x > 0
        self.image = self.image_right if self.facing_right else self.image_left
        
        self.rect = self.image.get_rect(midbottom=spawn_pos)
        
        self.state = 'roaming'
        self.health = self.data['health']
        self.speed = self.data['speed']

        self.spawn_time = pygame.time.get_ticks()
        self.last_damage_time = self.spawn_time
        self.last_direction_change = self.spawn_time

        self.exclamation_image = pygame.transform.scale(assets.get_image('exclamation'), (20, 20))
        self.exclamation_rect = self.exclamation_image.get_rect()
        self.show_exclamation = False

    def avoid_walkable_area(self):
        # ... (此方法不變)
        look_ahead_point = self.rect.center + self.direction * 30
        try:
            if self.walkable_mask.get_at(look_ahead_point):
                self.direction.rotate_ip(random.randint(90, 270))
        except IndexError:
            pass

    def roam(self):
        # ... (此方法不變)
        now = pygame.time.get_ticks()
        if now - self.last_direction_change > random.randint(2000, 4000):
            self.last_direction_change = now
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.avoid_walkable_area()
        self.rect.center += self.direction * self.speed

    def escape(self):
        # ... (此方法不變)
        self.avoid_walkable_area()
        self.rect.center += self.direction * self.speed

    def auto_damage(self):
        # ... (此方法不變)
        now = pygame.time.get_ticks()
        if now - self.last_damage_time > 1000:
            self.last_damage_time = now
            self.health -= random.randint(1, 3)
            if self.health <= 0:
                self.kill()

    def update(self):
        now = pygame.time.get_ticks()
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        if self.state == 'roaming' and now - self.spawn_time > self.data['escape_time']:
            self.state = 'escaping'
            self.speed *= self.data['escape_speed_multiplier']
            self.show_exclamation = True
        
        if self.state == 'roaming':
            self.roam()
        elif self.state == 'escaping':
            self.escape()
        
        if self.state == 'roaming':
            if (self.rect.left <= 0 and self.direction.x < 0) or \
               (self.rect.right >= SCREEN_WIDTH and self.direction.x > 0):
                self.direction.x *= -1
            if (self.rect.top <= 0 and self.direction.y < 0) or \
               (self.rect.bottom >= SCREEN_HEIGHT and self.direction.y > 0):
                self.direction.y *= -1
            self.rect.clamp_ip(screen_rect)
        
        elif self.state == 'escaping':
            if not self.rect.colliderect(screen_rect):
                # 【修改】在 kill 之前，先通知管理者
                self.manager.report_escape()
                self.kill()
        
        if self.direction.x > 0 and not self.facing_right:
            self.image = self.image_right
            self.facing_right = True
        elif self.direction.x < 0 and self.facing_right:
            self.image = self.image_left
            self.facing_right = False
        
        self.auto_damage()

    def draw_health_bar(self, surface):
        # ... (此方法不變)
        if self.health < self.max_health:
            WHITE = (255, 255, 255)
            RED = (255, 0, 0)
            health_percent = self.health / self.max_health
            bar_width = self.rect.width * 0.8
            bar_height = 7
            bar_x = self.rect.centerx - bar_width / 2
            bar_y = self.rect.bottom + 5
            background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            health_rect = pygame.Rect(bar_x, bar_y, bar_width * health_percent, bar_height)
            pygame.draw.rect(surface, WHITE, background_rect)
            pygame.draw.rect(surface, RED, health_rect)