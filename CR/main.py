import pygame
from settings import *
from scene_manager import SceneManager
from scenes.main_menu_scene import MainMenuScene
from scenes.gameplay_scene import GameplayScene
from asset_manager import assets # <--- 引入全局資源管理器實例

class Game:
# main.py (只顯示 Game 類別的 __init__ 方法)

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Coast Guardian")

        print("--- Loading Assets ---")
        
        assets.load_font('title', "NotoSerifTC-Medium.ttf", TITLE_FONT_SIZE)
        assets.load_font('menu', "NotoSerifTC-Medium.ttf", MENU_FONT_SIZE)
        assets.load_font('ui',  "NotoSerifTC-Medium.ttf", 36)
        
        assets.load_image('main_menu_bg', 'assets/images/GameStart.png')
        
        for level_num, level_data in LEVELS.items():
            level_id = level_data['id']
            assets.load_image(f'{level_id}_bg', level_data['background_image'])
            assets.load_image(f'{level_id}_walkable_mask', level_data['walkable_mask_image'])
        
        assets.load_image('player', 'assets/images/player.png')
        
        # 載入所有怪物的圖片
        assets.load_image('gbird_alpha', MONSTER_DATA['gbird_alpha']['image_path'])
        # ↓↓↓ 新增這一行 ↓↓↓
        assets.load_image('gbird_beta', MONSTER_DATA['gbird_beta']['image_path'])
        assets.load_image('exclamation', 'assets/images/exclamation.png')
        for weapon_id, weapon_data in WEAPON_DATA.items():
            assets.load_image(weapon_data['id'], weapon_data['image_path'])
        print("--- Asset Loading Complete ---")

        self.clock = pygame.time.Clock()
        self.running = True

        scenes = {
            'main_menu': MainMenuScene,
            'gameplay': GameplayScene
        }
        
        self.scene_manager = SceneManager(scenes, 'main_menu')
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            events = pygame.event.get()

            self.scene_manager.handle_events(events)
            self.scene_manager.update()
            self.scene_manager.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()