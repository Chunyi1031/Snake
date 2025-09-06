import time
import pygame
import json
import sys
import random

# 获取时间
def gettime():
    return time.strftime("%H:%M:%S ")

# 退出游戏
def quit():
    print(gettime() + "[游戏即将结束]2秒后退出")
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

print(gettime() + "[游戏开始运行]贪吃蛇1.1")

try:
    # 读取设置内容
    with open("setting.json") as f: 
        setting = json.load(f)
    FPS = setting["fps"]
    bgcolor = ((setting["bgcolor"])[0], (setting["bgcolor"])[1], (setting["bgcolor"])[2])
    snakecolor = ((setting["snakecolor"])[0], (setting["snakecolor"])[1], (setting["snakecolor"])[2])
    x = (setting["startxy"])[0] * 10
    y = (setting["startxy"])[1] * 10  # 修正了这里，应该是索引1而不是0
    print(f"帧率：{FPS}FPS")
    print(f"背景颜色(RGB)：{bgcolor}")
    print(f"蛇的颜色(RGB)：{snakecolor}")
    print(f"初始位置： x:{x} y:{y}")
except FileNotFoundError:
    print(gettime() + "[错误]无法打开配置文件setting.json")
    quit()

score = 0
# 初始化PyGame
print(gettime() + "[游戏运行中]正在初始化PyGame")
pygame.init()
# 创建窗口
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("贪吃蛇")
# 初始化时钟
clock = pygame.time.Clock()
# 设置文本
font = pygame.font.Font(None, 42)
# 填充背景
window.fill(bgcolor)
# 倒计时
window.blit(font.render('3', True, snakecolor), (130, 130))
pygame.display.flip()
pygame.time.wait(1000)
window.fill(bgcolor)
window.blit(font.render('2', True, snakecolor), (130, 130))
pygame.display.flip()
pygame.time.wait(1000)
window.fill(bgcolor)
window.blit(font.render('1', True, snakecolor), (130, 130))
pygame.display.flip()
pygame.time.wait(1000)
window.fill(bgcolor)
pygame.draw.rect(window, snakecolor, (x, y, 10, 10), 0)
pygame.display.flip()
print(gettime() + "[游戏运行中]游戏开始")

# 设置变量
running = True
direction = None  # 使用单个变量表示方向
last_move_time = pygame.time.get_ticks()
move_delay = (1000 / FPS) * 1.5  # 移动延迟(毫秒)，控制蛇的移动速度

snake_body = [(x, y)]
# 食物位置
food_x, food_y = random.randint(3, 27) * 10, random.randint(3, 27) * 10

while running:
    current_time = pygame.time.get_ticks()
    
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # 记录按键方向，但不立即移动
            elif event.key == pygame.K_a and direction != "right":
                direction = "left"
            elif event.key == pygame.K_d and direction != "left":
                direction = "right"
            elif event.key == pygame.K_w and direction != "down":
                direction = "up"
            elif event.key == pygame.K_s and direction != "up":
                direction = "down"
    
    # 每隔一定时间移动一次，而不是每帧都移动
    if current_time - last_move_time > move_delay and direction:
        last_move_time = current_time
        
        # 根据方向移动
        if direction == "left":
            x -= 10
        elif direction == "right":
            x += 10
        elif direction == "up":
            y -= 10
        elif direction == "down":
            y += 10
        
        # 撞墙检查
        if x > 290 or y > 290 or x < 0 or y < 0:
            print(f"{gettime()}[游戏运行中]你撞墙而死，分数{score}")
            window.fill((0, 0, 0))
            window.blit(font.render("You're dead!", True, (255, 0, 0)), (80, 130))
            pygame.display.flip()
            pygame.time.wait(1000)
            quit()
        
        # 判断是否吃掉食物
        if x == food_x and y == food_y:
            score += 1
            print(f"分数:{score}")
            food_x = random.randint(3, 27) * 10
            food_y = random.randint(3, 27) * 10

        # 判断是否撞到自己
        for i, (seg_x, seg_y) in enumerate(snake_body):
            if seg_x == x and seg_y == y and i > 0:
                print(f"{gettime()}[游戏运行中]你撞到了自己，分数{score}")
                window.fill((0, 0, 0))
                window.blit(font.render("You're dead!", True, (255, 0, 0)), (80, 130))
                pygame.display.flip()
                pygame.time.wait(1000)
                quit()
        
        # 更新蛇身
        snake_body.insert(0, (x, y))
        if len(snake_body) > score + 1:
            snake_body.pop()
        
        # 判断是否胜利
        if score == setting["full_marks"]:
            print(f"{gettime()}[游戏运行中]你胜利了，分数{score}")
            window.blit(font.render("You're win!", True, (255, 216, 81)), (80, 130))
            pygame.display.flip()
            quit()
    
    # 绘制游戏
    window.fill(bgcolor)
    
    # 绘制蛇
    for i, (seg_x, seg_y) in enumerate(snake_body):
        if i == 0:
            pygame.draw.rect(window, snakecolor, (seg_x, seg_y, 10, 10), 0)
        else:
            pygame.draw.rect(window, (220, 110, 0), (seg_x, seg_y, 10, 10), 0)
    
    # 绘制食物
    pygame.draw.rect(window, (255, 20, 0), (food_x, food_y, 10, 10), 0)
    
    # 显示分数
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)

quit()