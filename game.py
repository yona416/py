# 1 引入需要的模块
import random, pygame, sys

# 1 配置图片地址
IMAGE_PATH = 'imgs/'
# 1 设置页面宽高
screen_width = 800
screen_height = 560
# 1 创建控制游戏结束的状态
GAMEOVER = False
# 4 图片加载报错处理
LOG = '文件:{}中的方法:{}出错'.format(__file__, __name__)
# 初始化混音器模块
pygame.mixer.init()


# 3 创建地图类
class Map:
    # 3 存储两张不同颜色的图片名称
    map_names_list = [IMAGE_PATH + 'map1.png', IMAGE_PATH + 'map2.png']

    # 3 初始化地图
    def __init__(self, x, y, img_index):
        self.image = pygame.image.load(Map.map_names_list[img_index])
        self.position = (x, y)
        # 是否能够种植
        self.can_grow = True

    # 3 加载地图
    def load_map(self):
        MainGame.window.blit(self.image, self.position)


# 4 植物类
class Plant(pygame.sprite.Sprite):
    def __init__(self):
        super(Plant, self).__init__()
        self.live = True

    # 加载图片
    def load_image(self):
        if hasattr(self, 'image') and hasattr(self, 'rect'):
            MainGame.window.blit(self.image, self.rect)
        else:
            print(LOG)


# 5 向日葵类
class food1(Plant):
    def __init__(self, x, y):
        super(food1, self).__init__()
        self.image = pygame.image.load('imgs/sunflower.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 100
        # 5 时间计数器
        self.time_count = 0

    # 5 新增功能：生成阳光
    def produce_money(self):
        self.time_count += 1
        if self.time_count == 80:
            MainGame.money += 25
            self.time_count = 0

    # 5 向日葵加入到窗口中
    def display_sunflower(self):
        MainGame.window.blit(self.image, self.rect)


class food2(food1):
    def __init__(self, x, y):
        super(food2, self).__init__(x, y)
        # 修改价格和生成阳光的速度
        self.price = 45  # 修改为新太阳花的价格
        self.sun_production_speed = 70  # 修改为新太阳花生成阳光的速度（帧数）
        self.image = pygame.image.load('imgs/sunflower2.png')  # 修改为新太阳花的图片路径
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # 修改生成阳光的方法，根据新的速度生成阳光
    def produce_money(self):
        self.time_count += 1
        if self.time_count == self.sun_production_speed:
            MainGame.money += 25  # 生成阳光的数量
            self.time_count = 0


# 6 豌豆射手类
class attacker1(Plant):
    def __init__(self, x, y):
        super(attacker1, self).__init__()
        # self.image 为一个 surface
        self.image = pygame.image.load('imgs/peashooter.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 100
        self.hp = 200
        # 6 发射计数器
        self.shot_count = 0

    # 6 增加射击方法
    def shot(self):
        # 6 记录是否应该射击
        should_fire = False
        for zombie in MainGame.zombie_list:
            if zombie.rect.y == self.rect.y and 800 > zombie.rect.x > self.rect.x:
                should_fire = True
        # 6 如果活着
        if self.live and should_fire:
            self.shot_count += 1
            # 6 计数器到25发射一次
            if self.shot_count == 25:
                pygame.mixer.Sound.play(MainGame.shot_sound)
                # 6 基于当前豌豆射手的位置，创建子弹
                peabullet = bullet1(self)
                # 6 将子弹存储到子弹列表中
                MainGame.peabullet_list.append(peabullet)
                self.shot_count = 0

    # 6 将豌豆射手加入到窗口中的方法
    def display_peashooter(self):

        MainGame.window.blit(self.image, self.rect)

class attacker2(attacker1):
    def __init__(self, x, y):
        super(attacker2, self).__init__(x, y)
        self.image = pygame.image.load('imgs/peashooter2.png')


    def shot(self):
        # 6 记录是否应该射击
        should_fire = False
        for zombie in MainGame.zombie_list:
            if zombie.rect.y == self.rect.y and 800 > zombie.rect.x > self.rect.x:
                should_fire = True
        # 6 如果活着
        if self.live and should_fire:
            self.shot_count += 1
            # 6 计数器到25发射一次
            if self.shot_count == 25:
                pygame.mixer.Sound.play(MainGame.shot_sound)
                # 6 基于当前豌豆射手的位置，创建子弹
                peabullet = bullet2(self)
                # 6 将子弹存储到子弹列表中
                MainGame.peabullet_list.append(peabullet)
                self.shot_count = 0


# 7 豌豆子弹类
class bullet1(pygame.sprite.Sprite):
    def __init__(self, peashooter):
        self.live = True
        self.image = pygame.image.load('imgs/peabullet.png')
        self.damage = 50
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.x = peashooter.rect.x + 60
        self.rect.y = peashooter.rect.y + 15

    def move_bullet(self):
        # 7 在屏幕范围内，实现往右移动
        if self.rect.x < screen_width:
            self.rect.x += self.speed
        else:
            self.live = False

    # 7 新增，子弹与僵尸的碰撞
    def hit_zombie(self):
        for zombie in MainGame.zombie_list:
            if pygame.sprite.collide_rect(self, zombie):
                # 打中僵尸之后，修改子弹的状态，
                pygame.mixer.Sound.play(MainGame.hit_sound)
                self.live = False
                # 僵尸掉血
                zombie.hp -= self.damage
                if zombie.hp <= 0:
                    zombie.live = False
                    self.nextLevel()

    # 7闯关方法
    def nextLevel(self):
        MainGame.score += 20
        MainGame.remnant_score -= 20
        for i in range(1, 100):
            if MainGame.score == 100 * i and MainGame.remnant_score == 0:
                MainGame.remnant_score = 100 * i
                MainGame.guanka += 1
                MainGame.produce_zombie += 50

    def display_peabullet(self):
        MainGame.window.blit(self.image, self.rect)


class bullet2(bullet1):
    def __init__(self, peashooter):
        super().__init__(peashooter)  # 调用父类的构造函数，继承父类的属性和方法
        self.image = pygame.image.load('imgs/peabullet2.png')  # 加载新子弹的图像
        self.damage = 70

# 9 僵尸类
class tiredxiaoke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(tiredxiaoke, self).__init__()
        self.image = pygame.image.load('imgs/zombie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 800
        self.damage = 2
        self.speed = 0.8
        self.live = True
        self.stop = False

    # 9 僵尸的移动
    def move_zombie(self):
        if self.live and not self.stop:
            self.rect.x -= self.speed
            if self.rect.x < -80:
                # 8 调用游戏结束方法
                MainGame().gameOver()

    # 9 判断僵尸是否碰撞到植物，如果碰撞，调用攻击植物的方法
    def hit_plant(self):
        for plant in MainGame.plants_list:
            if pygame.sprite.collide_rect(self, plant):
                # 8  僵尸移动状态的修改
                self.stop = True
                self.eat_plant(plant)

    # 9 僵尸攻击植物
    def eat_plant(self, plant):
        # 9 植物生命值减少
        plant.hp -= self.damage
        # 9 植物死亡后的状态修改，以及地图状态的修改
        if plant.hp <= 0:
            a = plant.rect.y // 80 - 1
            b = plant.rect.x // 80
            map = MainGame.map_list[a][b]
            map.can_grow = True
            plant.live = False
            # 8 修改僵尸的移动状态
            self.stop = False

    # 9 将僵尸加载到地图中
    def display_zombie(self):
        MainGame.window.blit(self.image, self.rect)

class workingxiaoke(tiredxiaoke):
    def __init__(self, x, y):
        # 调用父类的初始化方法
        super().__init__(x, y)
        # 加载新僵尸的图像
        self.image = pygame.image.load('imgs/zombie2.png')
        # 修改新僵尸的属性，例如生命值、伤害值、速度等（根据需要进行调整）
        self.hp = 700
        self.damage = 1.5
        self.speed = 1.3

class coolxiaoke(tiredxiaoke):
    def __init__(self, x, y):
        # 调用父类的初始化方法
        super().__init__(x, y)
        # 加载新僵尸的图像
        self.image = pygame.image.load('imgs/zombie3.png')
        # 修改新僵尸的属性，例如生命值、伤害值、速度等（根据需要进行调整）
        self.hp = 700
        self.damage = 1
        self.speed = 1.51


# 1 主程序
class MainGame():
    # 0 游戏数据初始化
    def init_parameter(self):

        # 2 创建关数，得分，剩余分数，钱数
        MainGame.shot_sound = None
        MainGame.hit_sound = None
        MainGame.set_sound = None
        MainGame.fail_sound = None
        MainGame.begin_sound = None
        MainGame.clock_sound = None
        MainGame.window = None
        MainGame.guanka = 1
        MainGame.score = 0
        MainGame.remnant_score = 100
        MainGame.money = 50
        # 3 存储所有地图坐标点
        MainGame.map_points_list = []
        # 3 存储所有的地图块
        MainGame.map_list = []
        # 4 存储所有植物的列表
        MainGame.plants_list = []
        # 7 存储所有豌豆子弹的列表
        MainGame.peabullet_list = []
        # 9 新增存储所有僵尸的列表
        MainGame.zombie_list = []
        MainGame.count_zombie = 0
        MainGame.time_count = 0
        MainGame.produce_zombie = 100

    # 1 加载游戏窗口
    def init_window(self):
        # 1 调用显示模块的初始化
        pygame.init()
        # 1 创建窗口
        MainGame.window = pygame.display.set_mode([screen_width, screen_height])
        # 增加bgm和音效
        #
        # MainGame.set_sound = pygame.mixer.Sound("bgm/set2.wav")
        MainGame.set_sound = pygame.mixer.Sound("bgm/植物落地.wav")
        MainGame.shot_sound = pygame.mixer.Sound("bgm/射击.wav")
        MainGame.hit_sound = pygame.mixer.Sound("bgm/子弹打击.wav")
        MainGame.fail_sound = pygame.mixer.Sound("bgm/闯关失败.wav")
        MainGame.begin_sound = pygame.mixer.Sound("bgm/begin_game.wav")
        MainGame.clock_sound = pygame.mixer.Sound("bgm/begin_background.mp3")
        pygame.mixer.music.load("bgm/map_bgm.ogg")
        # vInfo = pygame.display.Info()  # 窗口全屏显示
        # size = width, height = vInfo.current_w, vInfo.current_h
        # MainGame.window = pygame.display.set_mode(size, pygame.FULLSCREEN)  # 窗口全屏显示

    # 2 文本绘制
    def draw_text(self, content, size, color):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', size)
        text = font.render(content, True, color)
        return text

    # 2 加载帮助提示
    def load_help_text(self):
        text1 = self.draw_text('光标悬浮，按1、2补充早餐能量，按3、4发起早八攻击', 26, (255, 0, 0))
        MainGame.window.blit(text1, (5, 5))

    # 3 初始化坐标点
    def init_plant_points(self):
        for y in range(1, 7):
            points = []
            for x in range(10):
                point = (x, y)
                points.append(point)
            MainGame.map_points_list.append(points)
            print("MainGame.map_points_list", MainGame.map_points_list)

    # 3 初始化地图
    def init_map(self):
        for points in MainGame.map_points_list:
            temp_map_list = list()
            for point in points:
                # map = None
                if (point[0] + point[1]) % 2 == 0:
                    map = Map(point[0] * 80, point[1] * 80, 0)
                else:
                    map = Map(point[0] * 80, point[1] * 80, 1)
                # 将地图块加入到窗口中
                temp_map_list.append(map)
                print("temp_map_list", temp_map_list)
            MainGame.map_list.append(temp_map_list)
        print("MainGame.map_list", MainGame.map_list)

    # 3 将地图加载到窗口中
    def load_map(self):
        for temp_map_list in MainGame.map_list:
            for map in temp_map_list:
                map.load_map()

    # 6 增加豌豆射手发射处理
    def load_plants(self):
        for plant in MainGame.plants_list:
            # 6 优化加载植物的处理逻辑
            if plant.live:
                if isinstance(plant, food1):
                    plant.display_sunflower()
                    plant.produce_money()
                elif isinstance(plant, attacker1):
                    plant.display_peashooter()
                    plant.shot()
            else:
                MainGame.plants_list.remove(plant)

    # 7 加载所有子弹的方法
    def load_peabullets(self):
        for b in MainGame.peabullet_list:
            if b.live:
                b.display_peabullet()
                b.move_bullet()
                # v1.9 调用子弹是否打中僵尸的方法
                b.hit_zombie()
            else:
                MainGame.peabullet_list.remove(b)

    # 8事件处理

    def deal_events(self):
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件列表，判断
        for e in eventList:
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:  # 键盘1键，选择种植Sunflower
                    plant_type = food1
                elif e.key == pygame.K_2:  # 键盘2键，选择种植Sunflower2
                    plant_type = food2
                elif e.key == pygame.K_3:  # 键盘3键，选择种植PeaShooter
                    plant_type = attacker1
                elif e.key == pygame.K_4:  # 键盘4键，选择种植PeaShooter2
                    plant_type = attacker2
                else:
                    plant_type = None

                if plant_type and MainGame.money >= 50:
                    pygame.mixer.Sound.play(MainGame.set_sound)
                    # 获取鼠标当前位置
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = mouse_x // 80
                    y = mouse_y // 80
                    if 0 <= x <= len(MainGame.map_list[0]) and 0 < y <= len(MainGame.map_list):
                        map = MainGame.map_list[y - 1][x]
                        if map.can_grow:
                            plant = plant_type(map.position[0], map.position[1])
                            MainGame.plants_list.append(plant)
                            map.can_grow = False
                            MainGame.money -= 50

    # 9 新增初始化僵尸的方法
    def init_zombies(self):
        for i in range(1, 7):
            dis = random.randint(1, 5) * 200

            random_number = random.randint(0, 8)
            if 0 <= random_number <= 3:
                zombie = tiredxiaoke(800 + dis, i * 80)
            elif 4 <= random_number <= 6:
                zombie = workingxiaoke(800 + dis, i * 80)
            else:
                zombie = coolxiaoke(800 + dis, i * 80)

            MainGame.zombie_list.append(zombie)

    # 9将所有僵尸加载到地图中
    def load_zombies(self):
        for zombie in MainGame.zombie_list:
            if zombie.live:
                zombie.display_zombie()
                zombie.move_zombie()
                # v2.0 调用是否碰撞到植物的方法
                zombie.hit_plant()
            else:
                MainGame.zombie_list.remove(zombie)

    # 10 初始化游戏开始背景
    def init_background(self):
        # 设置按钮
        button = pygame.Rect(462, 224, 256, 112)  # 开始游戏按钮初始位置和大小
        pygame.draw.rect(MainGame.window, (0, 0, 0), button)  # 在屏幕上绘制按钮
        # 先绘制按钮，再设置窗口背景(覆盖按钮)
        # 加载游戏背景图像
        background = pygame.image.load('imgs/begin_game1.png')
        # 将图片作为窗口背景
        MainGame.window.blit(background, (0, 0))
        # 添加背景音频
        pygame.mixer.Sound.play(MainGame.clock_sound)
        # 循环检测鼠标是否按下
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 如果关闭窗口事件发生，结束游戏主循环
                    running = False
                    self.quitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 如果鼠标左键在窗口内开始游戏位置按下，则进入游戏
                    if button.collidepoint(pygame.mouse.get_pos()):  # 检查鼠标位置是否与按钮开始游戏相交
                        if event.button == 1:
                            MainGame.clock_sound.stop()
                            # 播放游戏开始音频
                            pygame.mixer.Sound.play(MainGame.begin_sound)
                            print('Start game!')  # 游戏开始
                            running = False

            pygame.display.flip()  # 更新窗口等待游戏开始点击事件的发生，直到用户关闭窗口为止。运行结束后退出程序。

    # 11 初始化游戏退出界面
    def init_gameResult(self):
        # 停止游戏背景音
        pygame.mixer.music.stop()
        # 播放游戏结算界面音频
        pygame.mixer.Sound.play(MainGame.fail_sound)
        # 创建按钮对象
        button = [0, 0]
        button[0] = pygame.Rect(571, 115, 129, 78)  # 再来一局按钮初始位置和大小
        button[1] = pygame.Rect(619, 203, 129, 78)  # 退出游戏按钮初始位置和大小
        for i in range(2):
            pygame.draw.rect(MainGame.window, (255, 0, 0), button[i])  # 在屏幕上绘制按钮
        # 游戏结算界面背景
        MainGame.window.blit(pygame.image.load('imgs/gameResult.png'), (0, 0))
        # 显示玩家得分
        MainGame.window.blit(self.draw_text('通过关数:{}'.format(MainGame.guanka), 26, (255, 0, 0)),
                             (635, 310))
        MainGame.window.blit(self.draw_text('得分:{}'.format(MainGame.score), 26, (255, 0, 0)),
                             (635, 340))
        pygame.display.update()

        global GAMEOVER
        GAMEOVER = False
        # 结算界面检测鼠标是否按下
        running = True
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 监听鼠标点击事件
                    if button[1].collidepoint(pygame.mouse.get_pos()):  # 检查鼠标位置是否与按钮退出游戏相交
                        if event.button == 1:
                            running = False
                            self.quitGame()
                    if button[0].collidepoint(pygame.mouse.get_pos()):  # 检查鼠标位置是否与按钮再来一局相交
                        if event.button == 1:
                            print('再来一局')  # 再来一局按钮被点击
                            running = False


        pygame.mixer.Sound.stop(MainGame.fail_sound)
        MainGame.start_game(self)

    # 1 开始游戏
    def start_game(self):
        # 0 游戏数据初始化
        self.init_parameter()
        # 1 初始化窗口
        self.init_window()
        # 10 初始化游戏开始背景
        self.init_background()
        # 3 初始化坐标和地图
        self.init_plant_points()
        self.init_map()
        # 9 调用初始化僵尸的方法
        self.init_zombies()
        # 1 只要游戏没结束，就一直循环

        while not GAMEOVER:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.play()
            # 1 渲染白色背景
            MainGame.window.fill((255, 255, 255))
            # 2 渲染的文字和坐标位置
            MainGame.window.blit(self.draw_text('当前钱数$: {}'.format(MainGame.money), 26, (255, 0, 0)), (500, 40))
            MainGame.window.blit(self.draw_text(
                '当前关数{}，得分{},距离下关还差{}分'.format(MainGame.guanka, MainGame.score, MainGame.remnant_score),
                26,
                (255, 0, 0)), (5, 40))
            self.load_help_text()
            # 3 需要反复加载地图
            self.load_map()
            # 6 调用加载植物的方法
            self.load_plants()
            # 7  调用加载所有子弹的方法
            self.load_peabullets()
            # 8 调用事件处理的方法
            self.deal_events()
            # 9 调用展示僵尸的方法
            self.load_zombies()
            # 9 计数器增长，每数到100，调用初始化僵尸的方法
            MainGame.count_zombie += 1
            if MainGame.count_zombie == MainGame.produce_zombie:
                self.init_zombies()
                MainGame.count_zombie = 0
            # 新增 计数器增长，默认产生阳光
            MainGame.time_count += 1
            if MainGame.time_count == 80:
                MainGame.money += 25
                MainGame.time_count = 0
            # 9 pygame自己的休眠
            pygame.time.wait(10)
            # 1 实时更新
            pygame.display.update()

        if GAMEOVER:
            # 访问游戏结算界面
            MainGame.init_gameResult(self)

    # 10 程序结束方法程序结束进入结算界面
    def gameOver(self):
        global GAMEOVER
        GAMEOVER = True

    # 11 程序结束方法
    def quitGame(self):
        pygame.quit()
        sys.exit()


# 1 启动主程序
if __name__ == '__main__':
    game = MainGame()
    game.start_game()
