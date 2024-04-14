import time

import pygame
import os
from plane_sprites import *
# 设置颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")
        pygame.init()  # 初始化所有pygame模块，包括字体模块
        #  初始化声音混合器
        pygame.mixer.init()
        # 0. 创建窗口标题
        pygame.display.set_caption("牢大复活赛")
        # 1. 创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        #  定义得分
        self.score = 0

        # 4. 设置定时器事件 - 创建敌机　1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 设置定时器，在5-10秒随机创建一个陨石
        # 生成一个5到10秒之间的随机数
        meteor_interval = random.randint(2000, 5000)
        pygame.time.set_timer(METEORITE_EVENT,meteor_interval)
        #  设置100s-1000S生成一个血包
        prop_interval = random.randint(100000, 1000000)
        pygame.time.set_timer(PROP_EVENT, prop_interval)
        #  发射子弹0.5s
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
        #  生成一个坤坤发射子弹的定时器
        pygame.time.set_timer(KUNKUN,500)
        # 用空字典来存储事件
        self.hero_hit = {}

        #  倒计时属性
        self.over_time = 3
        #  展示状态[0]-表示敌机血条是否一直展示
        self.show_Health_bar = [0,]
        #  血条比例
        self.remain = 1
        #  血条颜色
        self.color = RED
        #  记录敌机精灵
        self.shows = None
        #  调用Boss
        self.Kun = KUN()
        self.boss_width = 0
        self.boss_color = RED
        self.boss_remain = 1
        #  牢大肘击图片
        self.images_zhouji = []
        #  牢大肘击帧数
        self.clock_zhouji = None
        self.FPS_zhouji = 0
        #  牢大肘击的次数
        self.count = 0
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        # 定义字体
        #self.font_name = pygame.font.match_font("Microsoft YaHei.ttf")
        self.font_name = pygame.font.SysFont('Microsoft YaHei',36)  # 36是字体大小
        #  定义小图标，当作命数
        self.hero_mini = pygame.transform.scale(self.hero.image, (50, 50))
        #  开始页面
        self.show = True
        #  导入游戏背景音乐
        #  背景音效
        self.bg_sound = pygame.mixer.Sound(os.path.join('audio','背景音效.mp3'))
        self.laoda_sound = pygame.mixer.Sound(os.path.join("audio","laoda.mp3"))
        #  游戏开始音效
        self.pl_sound = pygame.mixer.Sound(os.path.join("audio", "敢不敢跟我比划比划2.mp3"))
        #  子弹发射音效
        self.fs_sound = pygame.mixer.Sound(os.path.join("audio", "射击音效.mp3"))
        #  飞机受伤音效
        self.sh_sound = pygame.mixer.Sound(os.path.join("audio", "答辩叫.mp3"))
        #  坤坤叫
        self.kun_sound =pygame.mixer.Sound(os.path.join("audio",'诶呦你干嘛.mp3'))
        #  肘击叫
        self.zj_sound = pygame.mixer.Sound(os.path.join('audio','曼.mp3'))


    def draw_text(self, surf, text, x, y):
            # 直接使用 self.font_name 来渲染文本
            text_surface = self.font_name.render(text, True, RED)
            text_rect = text_surface.get_rect(centerx=x, top=y)
            surf.blit(text_surface, text_rect)


    def show_play(self):

        # 创建背景精灵和精灵组

        pl_background = pygame.image.load(os.path.join('images', 'play_bg.png'))
        self.screen.blit(pl_background, (0, 0))
        #  开始界面的说明
        self.draw_text(surf=self.screen,text='| 飞 机 大 战 |',x=350,y=200)
        self.draw_text(surf= self.screen,text='小键盘上下左右控制方向',x=350, y=450)
        self.draw_text(surf=self.screen, text='注意*游玩时请切换英文键盘*', x=350, y=500)
        self.draw_text(surf=self.screen,text='按任意键开始',x=350,y= 700)

        pygame.display.flip()   # 更新屏幕xer

        while self.show:
            self.clock.tick(FRAME_PER_SEC)
            for event in pygame.event.get():   # 获取键盘

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:  # 当有按键落下
                    #触发游戏开始音效
                    self.pl_sound.play()
                    self.show = False


    def draw_heath(self,surf,hp,x,y):
        #   绘制飞机血条
        if hp <0:
            hp =0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (hp/100)*BAR_LENGTH
        out_reck = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
        fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
        pygame.draw.rect(surf, (255,0,0),fill_rect)
        pygame.draw.rect(surf, (255,255,255),out_reck,2)


    def drow_live(self,surf,lives,img,x,y):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 *i
            img_rect.y = y
            surf.blit(img,img_rect)

    def __create_sprites(self,laoda = False):

        # 创建背景精灵和精灵组
        bg1 = Background(laoda=laoda)
        bg2 = Background(laoda=laoda,is_alt= True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵类和精灵组
        self.enemy = Enemy()
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        if laoda:
            self.hero = Hero_laoda()
            self.hero_group = pygame.sprite.Group(self.hero)
        else:
            self.hero = Hero()
            self.hero_group = pygame.sprite.Group(self.hero)
        #  创建陨石类
        self.meteorite_group = pygame.sprite.Group()
        #  创建血包类
        self.prop_group = pygame.sprite.Group()
        #  创建特效类
        self.all_sprites = pygame.sprite.Group()

        #  创建Boss的类
        self.Kun_group = pygame.sprite.Group()
        # 将Boss精灵添加到Boss精灵组
        self.Kun_group.add(self.Kun)
    def start_game(self):
        print("游戏开始...")
        # 0.5 游戏开始画面
        #  是否是第一次死亡需要进入游戏开始画面
        if self.hero.die:
            #  展示首页
            self.show_play()
            #  游戏音效
            self.bg_sound.play()

        while True:

            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)

            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()

            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()
            if self.hero.die == False:
                #  播放牢大音效
                if not pygame.mixer.get_busy():  # 如果混音器没有在播放
                    self.laoda_sound.play()  # 再次播放
          
    #  事件监听
    def __event_handler(self):

        for event in pygame.event.get():

            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over(self)
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵
                enemy = Enemy()
                # 将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)
            elif event.type == METEORITE_EVENT:
                meteorite = Meteorite()
                #  将陨石添加到陨石组
                self.meteorite_group.add(meteorite)
                #  将血包添加到血包类
                prop = Prop()
                self.prop_group.add(prop)
            # 当坤坤出场自带篮球攻击
            elif event.type == KUNKUN and  self.hero.die == False and self.score >= 10000:
                #  将篮球攻击添加到陨石类
                basketball = Basketball()
                self.meteorite_group.add(basketball)


            if event.type == pygame.KEYDOWN :
                #z键手动，自动互相切换
                print(event)
                if event.key == 122:
                    self.hero.auto = not self.hero.auto
                #判断是否按空格进行开关,是否是手动，是才可以否则自动按空格也会射击
                if event.key == 32 and self.hero.auto == False :
                    #触发发射音效
                    self.fs_sound.play()
                    self.hero.fire()
            elif event.type == HERO_FIRE_EVENT and self.hero.auto == True:
                # 自动射击逻辑（当auto为True时）
                self.hero.fire()

            if event.type == pygame.KEYDOWN:
               if event.key ==113:
                    #检查是否是空格键被按下
                    pygame.quit()
                    exit()


    def Boom(self):
        # 设置动画的帧率
        frame_rate = 19
        if self.temp == 1:
            images = [pygame.image.load(os.path.join(f'images', f'enemy1_down{i + 1}.png'))for i in range(4)]

        elif self.temp == 3:
            images = [pygame.image.load(os.path.join(f'images', f'enemy2_down{i + 1}.png')) for i in range(4)]

        elif self.temp == 5:
            images = [pygame.image.load(os.path.join('images', f'enemy3_down{i + 1}.png')) for i in range(4)]



        # 获取图片的宽度
        image_width = images[0].get_width()

        # 计算动画的总时间
        total_frames = len(images)
        total_time = total_frames / frame_rate

        # 设置时钟
        clock = pygame.time.Clock()
        # 获取当前时间
        current_time = pygame.time.get_ticks()

        # 计算当前应该显示哪张图片
        current_frame = int(current_time / 1000 * frame_rate) % total_frames

        # 绘制图片
        self.screen.blit(images[current_frame],self.enemy_center )

        # 更新屏幕显示
        pygame.display.flip()

        # 设置每帧的持续时间
        clock.tick(frame_rate)
    def Elbow_strike(self):
        # 显示动画
        frame = 0
        play_animation = True
        while play_animation:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    play_animation = False

            # 显示当前帧的图片
            self.screen.blit(self.images_zhouji[frame], (100,100))

            # 更新帧数
            frame = (frame + 1) % len( self.images_zhouji)

            # 更新屏幕
            pygame.display.flip()

            # 控制帧率
            self.clock_zhouji.tick(self.FPS_zhouji)

        # 更新屏幕
        pygame.display.flip()
    def __check_collide(self):

        # 1. 子弹摧毁敌机
        self.hero_hit = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, False)

        for bullet, enemies in self.hero_hit.items():
            for enemy in enemies:
                enemy.show_healthy = True
                self.temp = enemy.title
                enemy.hit -= 1  # 减少敌机的打击数
                # 计算剩余生命值比例
                energy_remain = max(0, enemy.hit / self.temp)  # 确保能量剩余比例不会为负数

                # 根据剩余生命值比例绘制血槽的填充部分
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED

                pygame.draw.rect(self.screen, energy_color, (enemy.rect.left, enemy.rect.top + 30,
                                                             int(enemy.rect.width * energy_remain), 15))
                self.remain = energy_remain
                self.color = energy_color
                self.show_Health_bar[0] = 1
                self.shows = enemy
                # 更新屏幕
                pygame.display.flip()

                if enemy.hit <= 0:
                    self.temp = enemy.title
                    print(self.temp)
                    # 获取被击中的敌机的坐标
                    self.enemy_center = enemy.rect.center  # 获取敌机中心的坐标
                    self.show_Health_bar[0] = 0
                    if self.temp == 5:
                        # 假设您想要将敌机向右移动10个像素
                        offset = pygame.math.Vector2(-85, -135)  # 创建一个向量表示移动的方向和距离
                    if self.temp == 3:
                        offset = pygame.math.Vector2(-30, -50)  # 创建一个向量表示移动的方向和距离
                        # 获取敌机的当前中心坐标
                    if self.temp == 1:
                        offset = pygame.math.Vector2(-10, -25)  # 创建一个向量表示移动的方向和距离
                    enemy_center = enemy.rect.center

                    # 应用偏移量来更新敌机的坐标
                    new_center = enemy_center + offset
                    enemy.rect.center = new_center
                    self.enemy_center = new_center
                    # 播放击败敌机动画
                    self.Boom()

                    #  如果敌机的打击数小于等于0，销毁它并增加分
                    enemy_score = enemy.radius  # 获取敌机的大小
                    score_increase = enemy_score * 10  # 假设得分与敌机大小成正比，这里乘以一个系数
                    enemy.kill()
                    self.score += score_increase  # 根据敌机大小增加分数
        # 2. 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True,pygame.sprite.collide_circle)
        # 3. 陨石撞毁英雄
        enemies1 = pygame.sprite.spritecollide(self.hero, self.meteorite_group, True,pygame.sprite.collide_circle)
        # 4.血包碰到英雄
        enemies2 = pygame.sprite.spritecollide(self.hero, self.prop_group, True, pygame.sprite.collide_circle)
        # 判断列表时候有内容
        for enemy_group in [enemies, enemies1, enemies2]:
            for hit in enemy_group:
                if hit in enemies2 and self.hero.health < 100:
                    if self.hero.health > 90:
                        self.hero.health = 100
                    else:
                        self.hero.health += 20
                else:
                    self.hero.health -= hit.radius
                    #  飞机受伤音效
                    self.sh_sound.play()
                    if self.hero.health <= 0:
                        self.hero.lives -= 1
                        self.hero.health = 100
                        if self.hero.lives == 0:
                            self.hero.hide()
                            # 让英雄牺牲
                            self.hero.kill()
                            # 结束游戏
                            PlaneGame.__game_over(self)
                            return

            Boss_hit = pygame.sprite.groupcollide(self.hero.bullets, self.Kun_group, True, False)
            for bullet, enemies in Boss_hit.items():
                for boss in enemies:

                    temp = boss.title
                    boss.Kun_hit -= 1  # 减少敌机的打击数
                    #  被击中坤坤会叫
                    self.kun_sound.play()
                    # 计算剩余生命值比例
                    self.boss_remain = max(0,boss.Kun_hit/ temp)  # 确保能量剩余比例不会为负数

                    # 根据剩余生命值比例绘制血槽的填充部分
                    if 0.6< self.boss_remain > 0.4:
                        boss_color = GREEN
                    else:
                        boss_color = RED

                    pygame.draw.rect(self.screen, boss_color, (350, 20,
                                                                 int(boss.rect.width * self.boss_remain), 25))
                    self.boss_width = boss.rect.width
                    self.boss_color = boss_color
                    if boss.Kun_hit <= 0:
                        #  如果敌机的打击数小于等于0，销毁它并增加分
                        enemy_score = boss.radius  # 获取敌机的大小
                        score_increase = enemy_score * 10  # 假设得分与敌机大小成正比，这里乘以一个系数
                        boss.kill()
                        self.score += score_increase  # 根据敌机大小增加分数
    def __update_sprites(self):
        #  背景更新
        self.back_group.update()
        self.back_group.draw(self.screen)
        #  敌人更新
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        #  陨石类
        self.meteorite_group.update()
        self.meteorite_group.draw(self.screen)
        #  道具类
        self.prop_group.update()
        self.prop_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        #  英雄子弹类更新
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
        #  BOSS类更新
        if self.score >= 10000:
            #  更新BOSS 位置
            self.Kun.update()
            # 绘制到屏幕上
            self.Kun_group.draw(self.screen)

            pygame.draw.rect(self.screen, self.boss_color, (300, 15,
                                                       int(self.boss_width * self.boss_remain), 25))

        #  1代表可以显示，0则代表不可以显示
        if self.show_Health_bar[0] == 1:
            pygame.draw.rect(self.screen, self.color, (self.shows.rect.left, self.shows.rect.top + 30,
                                                         int(self.shows.rect.width * self.remain), 10))
        self.font_name = pygame.font.SysFont('Microsoft YaHei', 30)  # 30是字体大小
        #绘制得分背景
        score_bj = pygame.image.load(os.path.join('images', 'fenshu.png')).convert_alpha()
        self.screen.blit(score_bj, (50,15))
        #  把分数绘制到屏幕上
        self.draw_text(self.screen,str(self.score),120,10)
        #  模式背景图(头像，血条，武器状态)
        mode_show = pygame.image.load(os.path.join('images', 'mode_show.png')).convert_alpha()
        self.screen.blit(mode_show, (0, 800))
        if self.hero.die == False:
        #  更新牢大头像图片
            laoda_hand = pygame.image.load(os.path.join('images', 'laoda_hand1.png')).convert_alpha()
            laoda_hand_mini = pygame.transform.scale(laoda_hand, (80, 80))
            self.screen.blit(laoda_hand_mini, (20, 800))
        else:
            laoda_hand = pygame.image.load(os.path.join('images', 'laoda_hand.jpg')).convert_alpha()
            laoda_hand_mini = pygame.transform.scale(laoda_hand, (290, 290))
            self.screen.blit(laoda_hand_mini, (-85, 730))
        self.draw_heath(self.screen,self.hero.health,140,820)
        self.drow_live(self.screen,self.hero.lives,self.hero_mini,600,10)


        self.font_name = pygame.font.SysFont('Microsoft YaHei', 20)  # 20是字体大小
        image = pygame.image.load(os.path.join('images', '射击模式.png')).convert_alpha()
        #  定义小图标,提示当前实际模式
        images = pygame.transform.scale(image, (150,40))
        self.screen.blit(images, (0,300))
        self.font_name = pygame.font.SysFont('Microsoft YaHei', 30)  # 20是字体大小
        self.draw_text(surf=self.screen, text=f' {self.hero.auto}', x=155, y=300)
        self.font_name = pygame.font.SysFont('Microsoft YaHei', 15)  #15是字体大小
        image_z = pygame.image.load(os.path.join('images', 'Z键切换.png')).convert_alpha()
        #  定义小图标，当作提示按键切换
        images_z = pygame.transform.scale(image_z, (150,40))
        self.screen.blit(images_z, (5,330))
        pygame.display.flip()  # 更新屏幕


    def __die_text(self):
        #  死亡时的文字提示，触发牢大
        self.back_group.draw(self.screen)
        self.font = pygame.font.SysFont('Microsoft',45)
        self.draw_text(surf=self.screen,text=f' GAME OVER {self.over_time}', x=300, y=300 - self.over_time )

        pygame.display.flip()  # 更新屏幕
    def __game_over(self):
        print("触发复活赛")
        self.bg_sound.stop()
        self.font_name = pygame.font.SysFont('Microsoft YaHei', 45)  # 36是字体大小

        pygame.display.flip()
        while True:
            if self.hero.die:
                # 删除精灵和精灵组
                while self.over_time > 0:
                    self.__die_text()
                    self.over_time -= 1
                    time.sleep(1)
                #  恢复死亡倒计时
                self.over_time = 3
                self.runing = True
                self.count = 0
                #  设置牢大肘击限时的定时器
                pygame.time.set_timer(LAODA, 10000)
                #  加载牢大肘击的图片
                # 加载图片并设置背景色为白色
                self.images_zhouji= [pygame.image.load(os.path.join(f'images', f'laoda{i + 1}.png')).convert() for i in range(3)]
                self.draw_text(surf=self.screen, text='#  复   活   赛 #', x=350, y=800)
                images = pygame.image.load(os.path.join(f'images','肘击牢大.png')).convert_alpha()
                # 绘制图片
                self.screen.blit(images, (100,600))

                pygame.display.flip()
                for image in  self.images_zhouji:
                    image.set_colorkey((255, 255, 255))
                    # 设置帧率
                self.clock_zhouji = pygame.time.Clock()
                self.FPS_zhouji = 40  # 设置为每秒40帧
                while self.runing:

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:


                            #  要求按j键肘击
                            if event.key == 106:
                                self.count += 1
                                #  肘击叫
                                self.zj_sound.play()
                                self.Elbow_strike()

                            #  按空格直接跳过
                            if event.key == 32 or self.count == 24:
                                self.runing = False
                        elif event.type == LAODA:
                            self.draw_text(surf=self.screen, text=f'# 你的得分为 :{self.score} #', x=350, y=400)
                            self.draw_text(surf=self.screen, text='# 游戏结束 牢大已坠机 #', x=350, y=500)
                            self.draw_text(surf=self.screen, text='#你未在规定时间完成肘击 #', x=350, y=600)
                            pygame.display.flip()  # 更新屏幕
                            time.sleep(3)
                            # 检查是否是空格键被按下
                            pygame.quit()
                            exit()
                # 清除所有的精灵类
                self.hero.clear()
                self.enemy_group.empty()
                self.hero_group.empty()
                self.prop_group.empty()
                self.all_sprites.empty()
                self.hero.kill()
                #  修正牢大的飞机
                self.hero = Hero_laoda()
                #  修正牢大的生命图标
                self.hero_mini = pygame.transform.scale(self.hero.image, (50, 50))
                #  修正死亡状态
                self.hero.die = False
                #  重置分数
                self.score = 0

                # 创建游戏对象
                self.__create_sprites(laoda= True)
                pygame.time.set_timer(CREATE_ENEMY_EVENT, 800)
                break
            else:
                # 清除所有的精灵类
                self.hero.clear()
                self.enemy_group.empty()
                self.hero_group.empty()
                self.prop_group.empty()
                self.all_sprites.empty()
                self.hero.kill()
                # 检查是否是空格键被按下
                pygame.quit()
                exit()


if __name__ == '__main__':

    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()
