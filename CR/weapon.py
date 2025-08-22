# weapon.py
import pygame
from settings import WEAPON_DATA
from asset_manager import assets

class Weapon(pygame.sprite.Sprite):
    def __init__(self, position, weapon_type):
        super().__init__()
        
        self.data = WEAPON_DATA.get(weapon_type)
        if not self.data:
            print(f"錯誤：找不到武器類型 {weapon_type} 的資料！")
            self.kill()
            return
            
        self.weapon_type = weapon_type
        
        # 圖像設定
        original_image = assets.get_image(self.data['id'])
        self.image = pygame.transform.scale(original_image, self.data['size'])
        self.rect = self.image.get_rect(center=position)