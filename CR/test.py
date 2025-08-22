import pygame
import sys

# --- 1. 初始化 Pygame ---
pygame.init()

# --- 2. 視窗設定 ---
screen_width = 1440
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("圖片載入與滑鼠點擊偵測")

# --- 3. 載入圖片 ---
# 請將 'your_image.png' 換成您自己的圖片檔案名稱
# 確保圖片檔案與此 .py 檔案在同一個資料夾中
try:
    loaded_image = pygame.image.load('assets/images/pier_walkable_mask.png')
    # 調整圖片大小以符合視窗，如果需要的話
    # loaded_image = pygame.transform.scale(loaded_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"無法載入圖片 'your_image.png': {e}")
    print("請確認：")
    print("1. 圖片檔案名稱是否正確？")
    print("2. 圖片檔案是否與 Python 程式在同一個資料夾？")
    sys.exit() # 如果圖片載入失敗，直接結束程式

# --- 4. 遊戲主迴圈 ---
running = True
while running:
    # --- 5. 事件處理 ---
    for event in pygame.event.get():
        # (A) 處理關閉視窗事件
        if event.type == pygame.QUIT:
            running = False

        # (B) 處理滑鼠點擊事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # event.pos 會回傳一個包含 (x, y) 座標的元組 (tuple)
            mouse_x, mouse_y = event.pos
            print(f"滑鼠點擊位置 (x, y): ({mouse_x}, {mouse_y})")

    # --- 6. 畫面繪製 ---
    # (A) 用白色填滿背景 (可選)
    screen.fill((255, 255, 255))

    # (B) 將載入的圖片繪製到視窗的左上角 (0, 0)
    screen.blit(loaded_image, (0, 0))

    # --- 7. 更新畫面 ---
    pygame.display.flip()

# --- 8. 結束 Pygame ---
pygame.quit()
sys.exit()