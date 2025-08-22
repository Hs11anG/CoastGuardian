# projectile.py
import pygame
import math # 【新增】引入數學函式庫
from settings import WEAPON_DATA, SCREEN_WIDTH, SCREEN_HEIGHT
from asset_manager import assets

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, weapon_type):
        super().__init__()

        self.data = WEAPON_DATA.get(weapon_type)
        if not self.data:
            self.kill()
            return
            
        self.damage = self.data['damage']
        
        # --- 【【【這是修正後、更穩定的旋轉與圖像邏輯】】】 ---
        # 1. 取得最原始的、未經旋轉的圖片
        original_image = assets.get_image(self.data['id'])
        
        # 2. 計算方向向量
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        
        # 3. 使用 math.atan2 計算精準角度 (弧度)，並轉換為 Pygame 使用的角度
        # math.atan2(dy, dx) 的結果是弧度，pygame.math.rad_to_deg 將其轉為角度
        # Pygame 的角度是逆時針為正，所以我們需要加負號
        angle = math.degrees(math.atan2(-dy, dx))

        # 4. 只旋轉這一次最原始的圖片
        rotated_image = pygame.transform.rotate(original_image, angle)

        # 5. 縮放旋轉後的圖片
        size_multiplier = self.data['projectile_size_multiplier']
        new_size = (int(self.data['size'][0] * size_multiplier), int(self.data['size'][1] * size_multiplier))
        self.image = pygame.transform.scale(rotated_image, new_size)
        
        self.rect = self.image.get_rect(center=start_pos)
        self.mask = pygame.mask.from_surface(self.image)
        
        # --- 移動邏輯 ---
        # 計算一次性的、標準化的方向向量
        self.direction = pygame.Vector2(dx, dy)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.speed = 15 # 稍微提高飛行速度

    def update(self):
        # 沿著固定的方向向量移動
        self.rect.center += self.direction * self.speed
        
        # 檢查是否超出螢幕範圍
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
            self.kill()