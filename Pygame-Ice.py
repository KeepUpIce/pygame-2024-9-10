from PIL import Image
import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 200, 200)
INITIAL_COUNTDOWN_TIME = 120  # 初始倒计时时间（秒）
PINK = (255, 192, 203)  # 定义粉色
RED = (255, 0, 0)  # 红色
YELLOW = (255, 255, 0)  # 黄色

# 定义字体大小
FONT_SIZE_MAIN = 55
FONT_SIZE_SCORE = 40
FONT_SIZE_TIME = 40
FONT_SIZE_CONTINUE = 30



# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("消除类小游戏——陈尚冰")

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 使用 Pillow 加载 GIF 动画帧
def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.copy().convert("RGBA")
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames


# 加载 background.gif
gif_frames = load_gif_frames("background.gif")
gif_frame_count = len(gif_frames)
gif_frame_index = 0
gif_frame_delay = 30  # 延迟30ms切换帧
last_frame_time = pygame.time.get_ticks()

# 创建游戏板
def create_board():
    tiles = patterns * (ROWS * COLS // len(patterns))
    random.shuffle(tiles)
    return [tiles[i * COLS:(i + 1) * COLS] for i in range(ROWS)]

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def check_match():
    global score  # 使用全局变量更新分数
    if len(selected) == 3:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        r3, c3 = selected[2]
        if board[r1][c1] == board[r2][c2] == board[r3][c3]:
            board[r1][c1] = None
            board[r2][c2] = None
            board[r3][c3] = None
            score += 10  # 每次消除成功加 10 分
        selected.clear()

def load_font(size):
    return pygame.font.Font(font_path, size)

def main_menu():
    font = load_font(font_size)
    while True:
        # 绘制背景动图
        global gif_frame_index, last_frame_time
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time >= gif_frame_delay:
            gif_frame_index = (gif_frame_index + 1) % gif_frame_count
            last_frame_time = current_time
        screen.blit(gif_frames[gif_frame_index], (0, 0))
        
         # 绘制菜单标题 (粉色)
        draw_text('消除类小游戏', font, PINK, screen, WIDTH // 2, HEIGHT // 2 - 200)
        draw_text('按任意键开始游戏ヾ(≧▽≦*)o', load_font(30), WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('游戏说明：', load_font(17), WHITE, screen, WIDTH // 2, HEIGHT // 2+100)
        draw_text('倒计时由120s开始，玩家需要点击三个相同的图案方块进行消除。', load_font(17), WHITE, screen, WIDTH // 2, HEIGHT // 2+130)
        draw_text('每次成功消除后，得分增加并且方块会掉落。', load_font(17), WHITE, screen, WIDTH // 2, HEIGHT // 2+150)
        draw_text('每局游戏胜利会提升难度，每次获胜倒计时减少10s，至多减少50s。', load_font(17), WHITE, screen, WIDTH // 2, HEIGHT // 2+170)
        draw_text('超时导致闯关失败时，倒计时时间不变。', load_font(17), WHITE, screen, WIDTH // 2, HEIGHT // 2+190)
        draw_text('陈尚冰 102201313', load_font(30), WHITE, screen, WIDTH // 2, HEIGHT // 2 + 250)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return

def game_over_screen(message, final_score, total_time):
    # 设置不同的字体大小
    font_main = load_font(FONT_SIZE_MAIN)  # 主标题
    font_score = load_font(FONT_SIZE_SCORE)  # 分数
    font_time = load_font(FONT_SIZE_TIME)  # 时间
    font_continue = load_font(FONT_SIZE_CONTINUE)  # 重新开始

    while True:
        screen.fill(WHITE)
        
        # 绘制失败消息
        draw_text(message, font_main, RED, screen, WIDTH // 2, HEIGHT // 2 - 100)
        
        # 绘制分数
        draw_text(f"分数:", font_score, BLACK, screen, WIDTH // 2 - 50, HEIGHT // 2 - 10)
        draw_text(f"{final_score}", font_score, BLACK, screen, WIDTH // 2 + 70, HEIGHT // 2 - 10)
        
        # 绘制时间
        draw_text(f"所用时间: {total_time} 秒", font_time, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)
        
        # 绘制重新开始按钮
        draw_text('按任意键重新开始(´・・)ﾉ(._.`)', font_continue, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 100)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return


def victory_screen(final_score, total_time):
    font = load_font(font_size)
    while True:
        screen.fill(WHITE)
        # 绘制“恭喜你！”文本
        font_main = load_font(FONT_SIZE_MAIN)
        draw_text("恭喜通过本关！", font_main, PINK, screen, WIDTH // 2, HEIGHT // 2 - 80)
    
         # 绘制分数
        font_score = load_font(FONT_SIZE_SCORE)
        draw_text(f"你的得分是:", font_score, BLACK, screen, WIDTH // 2 - 50, HEIGHT // 2 - 10)
        draw_text(f"{final_score}", font_score, BLACK, screen, WIDTH // 2 + 120, HEIGHT // 2 - 10)
    
        # 绘制时间
        font_time = load_font(FONT_SIZE_TIME)
        draw_text(f"所用时间: {total_time} 秒", font_time, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)
    
        # 绘制继续按钮
        font_continue = load_font(FONT_SIZE_CONTINUE)
        draw_text('按任意键继续游戏(^_^*)', load_font(30), BLACK, screen, WIDTH // 2, HEIGHT // 2 + 100)
    
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return

# 加载中文字体
font_path = "Microsoft_YaHei_Bold.ttf"  # 请将此路径替换为你下载的字体文件路径
font_size = 55

# 创建初始游戏板
board = create_board()
selected = []
start_time = time.time()
score = 0  # 初始化分数
level = 1  # 初始关卡
countdown_time = INITIAL_COUNTDOWN_TIME  # 当前关卡的倒计时时间

# 主游戏循环
main_menu()
running = True
clock = pygame.time.Clock()


while running:
    clock.tick(FPS)

    # 计算剩余时间
    elapsed_time = time.time() - start_time
    remaining_time = max(countdown_time - int(elapsed_time), 0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // TILE_SIZE, y // TILE_SIZE
            if board[row][col] is not None:
                selected.append((row, col))
            if len(selected) == 3:
                check_match()

    # 检查超时情况
    if remaining_time == 0:
        total_time = int(elapsed_time)
        game_over_screen("超时，游戏失败(′⌒`)", score, total_time)
        board = create_board()
        selected = []
        score = 0  # 重置分数
        start_time = time.time()
        # 保持倒计时时间不变
        continue

    # 检查游戏是否胜利
    if all(all(tile is None for tile in row) for row in board):
        total_time = int(elapsed_time)
        victory_screen(score, total_time)
        board = create_board()
        selected = []
        score = 0  # 重置分数
        start_time = time.time()
        # 提升难度，减少倒计时时间
        countdown_time = max(70, countdown_time - 10)
        continue

    screen.fill(BG_COLOR)
    draw_board()
    
    # 绘制倒计时和分数

    draw_text('剩余时间:', load_font(20), PINK, screen, WIDTH - 150, 10)
    time_text = f'{remaining_time}'
    draw_text(time_text, load_font(20), PINK, screen, WIDTH - 70, 10)  # 调整位置，使其在"剩余时间"后面


    # 绘制“分数”文本和分数值
    draw_text('分数:', load_font(20), PINK, screen, 50, 10)
    score_text = f'{score}'
    draw_text(score_text, load_font(20), PINK, screen, 50 + 60, 10)  # 黄色分数值，调整位置使其在"分数"后面
    
    
    

    pygame.display.flip()

pygame.quit()
