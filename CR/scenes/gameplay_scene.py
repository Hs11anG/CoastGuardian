# scenes/gameplay_scene.py
import pygame
from settings import *
from scene_manager import Scene
from asset_manager import assets
from player import Player
from monster_manager import MonsterManager
from weapon import Weapon

class GameplayScene(Scene):
    # __init__, load_level, handle_events, check_collisions, check_game_over, draw_hud, update
    # 這些方法都和您上傳的版本一樣，無需變更
    def __init__(self, manager):
        super().__init__(manager)
        self.game_state = 'inactive'
        self.player = None
        self.monster_manager = None
        self.all_sprites = pygame.sprite.Group()
        self.weapon_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.background_image = None
        self.walkable_mask = None
        self.level_duration = 0
        self.level_start_time = 0
        self.victory_monster_limit = 0
        self.escaped_monsters_count = 0
        self.events = []

    def load_level(self, level_number):
        level_data = LEVELS.get(level_number)
        if not level_data: return
        level_id = level_data['id']
        self.background_image = assets.get_image(f'{level_id}_bg')
        walkable_area_image = assets.get_image(f'{level_id}_walkable_mask')
        if walkable_area_image:
            self.walkable_mask = pygame.mask.from_surface(walkable_area_image)
            self.monster_manager = MonsterManager(self.walkable_mask, level_data, self)
        spawn_point = level_data['spawn_point']
        self.player = Player(start_pos=spawn_point, level_number=level_number)
        self.all_sprites.add(self.player)
        self.weapon_group.empty()
        weapon_spawns = level_data.get('weapon_spawns', [])
        for weapon_type, position in weapon_spawns:
            self.weapon_group.add(Weapon(position, weapon_type))
        self.level_duration = level_data.get('duration', 60) * 1000
        self.victory_monster_limit = level_data.get('victory_monster_limit', 20)
        self.level_start_time = pygame.time.get_ticks()
        self.escaped_monsters_count = 0
        self.game_state = 'playing'

    def handle_events(self, events):
        self.events = events
        for event in self.events:
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.switch_to_scene('main_menu')
                
    def check_collisions(self):
        if not self.monster_manager: return
        possible_hits = pygame.sprite.groupcollide(self.projectile_group, self.monster_manager.monsters, False, False)
        for projectile, monsters_hit in possible_hits.items():
            for monster in monsters_hit:
                if pygame.sprite.collide_mask(projectile, monster):
                    monster.health -= projectile.damage
                    projectile.kill()
                    if monster.health <= 0: monster.kill()
                    break

    def check_game_over(self):
        elapsed_time = pygame.time.get_ticks() - self.level_start_time
        if elapsed_time > self.level_duration:
            remaining_monsters = len(self.monster_manager.monsters)
            total_failed_monsters = self.escaped_monsters_count + remaining_monsters
            self.game_state = 'victory' if total_failed_monsters < self.victory_monster_limit else 'defeat'

    def draw_hud(self, screen):
        font = assets.get_font('ui')
        elapsed_time = pygame.time.get_ticks() - self.level_start_time
        remaining_time = max(0, self.level_duration - elapsed_time) / 1000
        time_text = f"Time: {remaining_time:.1f}"
        time_surf = font.render(time_text, True, WHITE)
        screen.blit(time_surf, (SCREEN_WIDTH - time_surf.get_width() - 20, 20))
        remaining_monsters = len(self.monster_manager.monsters) if self.monster_manager else 0
        monsters_text = f"Remaining: {remaining_monsters}"
        monsters_surf = font.render(monsters_text, True, WHITE)
        screen.blit(monsters_surf, (SCREEN_WIDTH - monsters_surf.get_width() - 20, 60))
        escaped_text = f"Escaped: {self.escaped_monsters_count}"
        escaped_surf = font.render(escaped_text, True, WHITE)
        screen.blit(escaped_surf, (SCREEN_WIDTH - escaped_surf.get_width() - 20, 100))

    def update(self):
        if self.game_state == 'playing':
            keys = pygame.key.get_pressed()
            if self.player:
                self.player.update(keys, self.events, self.walkable_mask, self.weapon_group, self.projectile_group)
            if self.monster_manager:
                self.monster_manager.update()
            self.projectile_group.update()
            self.check_collisions()
            self.check_game_over()

    def draw(self, screen):
        """將所有遊戲物件繪製到螢幕上"""
        # 1. 繪製遊戲世界
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((10, 20, 50))
        
        self.weapon_group.draw(screen)
        self.all_sprites.draw(screen) # 這裡會畫出 player.image
        if self.monster_manager:
            self.monster_manager.draw(screen)
        self.projectile_group.draw(screen)

        # 2. 【【【核心修改：在所有東西都畫完後，再畫玩家的 UI】】】
        if self.player:
            self.player.draw_ui(screen)

        # 3. 繪製遊戲整體的 UI
        if self.game_state == 'playing':
            self.draw_hud(screen)

        # 4. 繪製結束畫面
        if self.game_state == 'victory' or self.game_state == 'defeat':
            font = assets.get_font('title')
            text = "勝利" if self.game_state == 'victory' else "失敗"
            color = WHITE if self.game_state == 'victory' else HOVER_COLOR
            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text_surf, text_rect)