# asset_manager.py
import pygame

class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.fonts = {}
        self.images = {}
        self.sounds = {}
        print("AssetManager initialized.")

    def load_font(self, name, path, size):
        try:
            self.fonts[name] = pygame.font.Font(path, size)
            print(f"Font '{name}' loaded from {path}")
        except pygame.error as e:
            print(f"Error loading font '{name}' from {path}: {e}")
            self.fonts[name] = pygame.font.Font(None, size)

    def get_font(self, name):
        font = self.fonts.get(name)
        if font is None:
            print(f"Warning: Font '{name}' not found!")
        return font

    # --- ↓↓↓ 以下是這次新增/修改的程式碼 ↓↓↓ ---

    def load_image(self, name, path):
        """載入一個圖片並用名稱儲存起來"""
        try:
            # pygame.image.load() 會回傳一個 Surface 物件
            image = pygame.image.load(path)
            # .convert_alpha() 會轉換圖片的像素格式，包含處理透明度
            # 這一步驟對效能至關重要，能讓後續繪製速度大幅提升！
            self.images[name] = image.convert_alpha()
            print(f"Image '{name}' loaded from {path}")
        except pygame.error as e:
            print(f"Error loading image '{name}' from {path}: {e}")

    def get_image(self, name):
        """根據名稱取得一個已載入的圖片"""
        image = self.images.get(name)
        if image is None:
            print(f"Warning: Image '{name}' not found!")
        return image

# --- ↑↑↑ 以上是這次新增/修改的程式碼 ↑↑↑ ---


# 全局唯一的實例
assets = AssetManager()