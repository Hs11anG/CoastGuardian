# scenes/main_menu_scene.py
import pygame
from settings import *
from scene_manager import Scene
from asset_manager import assets

class MainMenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        
        # 菜單選項
        self.menu_options = ['開始新遊戲', '讀取存檔', '離開遊戲']
        self.menu_rects = []
        self.hovered_option = -1
        
        # 建立每個選項的 rect (用於偵測滑鼠碰撞)
        for i, option in enumerate(self.menu_options):
            # 這裡的 rect 尺寸需要根據您的字體和文字長度來調整
            rect = pygame.Rect(0, 0, 450, 80) 
            rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5 + i * 90)
            self.menu_rects.append(rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEMOTION:
                self.hovered_option = -1
                for i, rect in enumerate(self.menu_rects):
                    if rect.collidepoint(event.pos):
                        self.hovered_option = i
                        break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hovered_option != -1:
                    self.select_option(self.hovered_option)

    def select_option(self, index):
        if index == 0: # 開始新遊戲
            gameplay_scene = self.manager.scenes['gameplay']
            # 載入數字為 1 的關卡
            gameplay_scene.load_level(1) 
            self.manager.switch_to_scene('gameplay')
        elif index == 1: # 讀取存檔
            print("[INFO] '讀取存檔' 功能尚未實作。")
        elif index == 2: # 離開遊戲
            pygame.quit()
            exit()
            
    def update(self):
        """
        【【【補上這個空的 update 方法】】】
        主選單是靜態的，所以 update 方法目前不需要做任何事。
        但這個方法必須存在，否則就會觸發 NotImplementedError。
        """
        pass

    def draw(self, screen):
        # 繪製背景圖
        background_image = assets.get_image('main_menu_bg')
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)
        
        # 取得字體
        title_font = assets.get_font('title')
        menu_font = assets.get_font('menu')

        # 繪製標題
        title_surf = title_font.render("Coast Guardian", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2))
        screen.blit(title_surf, title_rect)

        # 繪製菜單選項
        for i, option_text in enumerate(self.menu_options):
            color = WHITE
            if i == self.hovered_option:
                color = HOVER_COLOR
            
            option_surf = menu_font.render(option_text, True, color)
            option_rect = option_surf.get_rect(center=self.menu_rects[i].center)
            screen.blit(option_surf, option_rect)