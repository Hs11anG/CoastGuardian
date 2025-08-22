# player.py
import pygame
from asset_manager import assets
from settings import *
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, level_number):
        super().__init__()
        
        # 修正您指出的筆誤
        original_image = assets.get_image('player') 
        player_size = LEVELS[level_number]['playersize']
        self.image = pygame.transform.scale(original_image, player_size)
        
        self.offsetx = LEVELS[level_number]['offsetx']
        self.offsety = LEVELS[level_number]['offsety']
        
        self.rect = self.image.get_rect(midbottom=start_pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5

        self.equipped_weapon_type = None
        self.equipped_weapon_icon = None
        self.can_interact = True
        self.last_shot_time = 0

        self.interaction_text = ""
        self.text_target_weapon = None

    def check_interaction(self, weapon_group):
        self.interaction_text = ""
        self.text_target_weapon = None

        if self.equipped_weapon_type:
            self.interaction_text = "按E以脫下"
            return

        interaction_rect = self.rect.inflate(30, 30)
        nearby_weapons = [w for w in weapon_group if interaction_rect.colliderect(w.rect)]

        if nearby_weapons:
            closest_weapon = min(nearby_weapons, key=lambda w: pygame.Vector2(self.rect.center).distance_to(w.rect.center))
            self.text_target_weapon = closest_weapon
            self.interaction_text = "按E以裝備"

    def move(self, keys, walkable_mask):
        if self.equipped_weapon_type:
            return

        old_rect = self.rect.copy()
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.rect.y += self.speed
            
        is_valid_move = False
        bottom_left_vec = pygame.Vector2(self.rect.bottomleft)
        bottom_right_vec = pygame.Vector2(self.rect.bottomright)
        point1 = bottom_left_vec + pygame.Vector2(self.offsetx, 0)
        point2 = bottom_right_vec - pygame.Vector2(self.offsetx, 0)
        corners = [point1, point2]
        
        for pos in corners:
            try:
                if walkable_mask.get_at(pos):
                    is_valid_move = True
                    break
            except IndexError:
                continue
        if not is_valid_move:
            self.rect = old_rect

    def interact_with_weapon(self, weapon_group):
        if self.equipped_weapon_type:
            self.equipped_weapon_type = None
            self.equipped_weapon_icon = None
            return
        if self.text_target_weapon:
            weapon_to_equip = self.text_target_weapon
            self.equipped_weapon_type = weapon_to_equip.weapon_type
            self.equipped_weapon_icon = weapon_to_equip.image.copy()
            
    def shoot(self, target_pos, projectile_group):
        if not self.equipped_weapon_type: return
        now = pygame.time.get_ticks()
        cooldown = WEAPON_DATA[self.equipped_weapon_type]['cooldown'] * 1000
        if now - self.last_shot_time > cooldown:
            self.last_shot_time = now
            new_projectile = Projectile(self.rect.center, target_pos, self.equipped_weapon_type)
            projectile_group.add(new_projectile)

    def update(self, keys, events, walkable_mask, weapon_group, projectile_group):
        self.check_interaction(weapon_group)
        self.move(keys, walkable_mask)
        if keys[pygame.K_e]:
            if self.can_interact:
                self.interact_with_weapon(weapon_group)
                self.can_interact = False
        else:
            self.can_interact = True
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.shoot(event.pos, projectile_group)

    def draw_ui(self, screen):
        """【【【新的獨立方法】】】負責繪製所有附加在玩家身上的 UI 元素"""
        # 繪製裝備相關的 UI
        if self.equipped_weapon_type:
            # 畫頭頂圖標
            icon_rect = self.equipped_weapon_icon.get_rect(center=(self.rect.centerx, self.rect.top - 30))
            screen.blit(self.equipped_weapon_icon, icon_rect)
            
            # 畫冷卻計時器
            cooldown = WEAPON_DATA[self.equipped_weapon_type]['cooldown']
            now = pygame.time.get_ticks()
            elapsed = (now - self.last_shot_time) / 1000
            if elapsed < cooldown:
                remaining_cd = cooldown - elapsed
                font = assets.get_font('ui')
                cd_text = f"{remaining_cd:.1f}s"
                text_surf = font.render(cd_text, True, WHITE)
                text_rect = text_surf.get_rect(midtop=self.rect.midbottom)
                screen.blit(text_surf, text_rect)

        # 繪製互動提示文字
        if self.interaction_text:
            font = assets.get_font('ui')
            text_surf = font.render(self.interaction_text, True, WHITE)
            pos = (0,0)
            if self.equipped_weapon_type:
                pos = (self.rect.centerx, self.rect.top - 60)
            elif self.text_target_weapon:
                pos = self.text_target_weapon.rect.midtop
            
            text_rect = text_surf.get_rect(midbottom=pos)
            screen.blit(text_surf, text_rect)