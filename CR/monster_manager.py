# monster_manager.py
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MONSTER_DATA
from monster import Monster

class MonsterManager:
    def __init__(self, walkable_mask, level_data, gameplay_scene):
        self.monsters = pygame.sprite.Group()
        self.walkable_mask = walkable_mask
        # 【新增】儲存對 GameplayScene 的引用
        self.scene = gameplay_scene
        
        self.spawn_list = []
        spawns = level_data.get('spawns', {})
        for monster_type, count in spawns.items():
            self.spawn_list.extend([monster_type] * count)
        
        random.shuffle(self.spawn_list)
        
        self.total_monsters_to_spawn = len(self.spawn_list)
        level_duration_ms = level_data.get('duration', 60) * 1000
        
        if self.total_monsters_to_spawn > 0:
            self.spawn_interval = level_duration_ms / self.total_monsters_to_spawn
        else:
            self.spawn_interval = float('inf')

        self.last_spawn_time = pygame.time.get_ticks()

    def choose_spawn_pos(self):
        # ... (此方法不變)
        while True:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            try:
                if not self.walkable_mask.get_at((x, y)):
                    return (x, y)
            except IndexError:
                return (x, y)

    def update(self):
        now = pygame.time.get_ticks()
        
        if now - self.last_spawn_time > self.spawn_interval and self.spawn_list:
            self.last_spawn_time = now
            monster_to_spawn = self.spawn_list.pop()
            spawn_pos = self.choose_spawn_pos()
            # 【修改】在建立怪物時，把 self (也就是 MonsterManager 自己) 傳進去
            new_monster = Monster(spawn_pos, monster_to_spawn, self.walkable_mask, self)
            self.monsters.add(new_monster)

        self.monsters.update()

    def draw(self, screen):
        # ... (此方法不變)
        self.monsters.draw(screen)
        for monster in self.monsters:
            monster.draw_health_bar(screen)
            if monster.show_exclamation:
                monster.exclamation_rect.center = (monster.rect.centerx, monster.rect.top - 10)
                screen.blit(monster.exclamation_image, monster.exclamation_rect)
                
    # ↓↓↓ 【【【新增接收回報的方法】】】 ↓↓↓
    def report_escape(self):
        """當有怪物成功逃跑時，由此方法通知 GameplayScene"""
        self.scene.escaped_monsters_count += 1
        print(f"An escape reported! Total escaped: {self.scene.escaped_monsters_count}")