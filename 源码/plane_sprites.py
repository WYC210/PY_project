import os.path
import random
import pygame



# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 700, 900)
# 刷新的帧率
FRAME_PER_SEC = 40
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
#创建陨石的定时器常量
METEORITE_EVENT = pygame.USEREVENT + 2
#创建血包的定时器常量
PROP_EVENT = pygame.USEREVENT + 3
#测试体积图像大小时使用的颜色，勿删
RED = (0,255,255)
#创建牢大肘击的定时器常量
LAODA = pygame.USEREVENT + 4
#  创建坤坤射击定时器
KUNKUN = pygame.USEREVENT + 5
# 定义爆炸列表
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
for i in range(1, 5):
    expl_img2 = pygame.image.load(os.path.join('images',f'enemy2_down{i}.png'))
    expl_anim['lg'].append(expl_img2)
    expl_img3 = pygame.image.load(os.path.join('images',f'enemy3_down{i}.png'))
    expl_anim['sm'].append(expl_img3)


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name,set_blue_transparent=False, speed=1):

        # 调用父类的初始化方法
        super().__init__()
        """
        image : 图片对象
        rect : 坐标
        speed : 速度
   
        """
        # 定义对象的属性
        if image_name == "me4.png":
            image_name =  pygame.transform.scale(self.hero.image, (45, 45))

        self.image = pygame.image.load(os.path.join('images', image_name)).convert_alpha()
        # 如果需要将蓝色设置为透明
        if set_blue_transparent:
            self.set_blue_transparent()
        self.rect = self.image.get_rect()
        self.speed = speed

    def set_blue_transparent(self):
        """将图片中的蓝色部分设置为透明"""
        blue = (0, 0, 255)
        self.image.set_colorkey(blue)

    def update(self):
        "角色飞机移动"
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed




class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self,laoda, is_alt=False):
        if laoda:
            super().__init__(image_name="laoda_bg.png")
        else:
            # 1. 调用父类方法实现精灵的创建(image/rect/speed)
            super().__init__(image_name="xingkong.png")
        # 2. 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 1. 调用父类的方法实现
        super().update()

        # 2. 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):

        enemy_images = ["enemy1.png","enemy2.png","enemy3.png"]

        #  随机出现三种类型的飞机
        enemy_images = random.choice(enemy_images)
        if enemy_images == "enemy2.png":
            #  记录每个飞机需要被击打的次数
            self.hit = 3
            self.title = 3
            self.show = False
        elif enemy_images == "enemy3.png":
            self.hit = 5
            self.title = 5
            self.show = False
        else:
            self.hit = 1
            self.title = 1
            self.show = False
        # 1. 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(enemy_images)
        #  判断是否显示血条，如果被击打过那么就一直显示，否则不显示
        self.show_healthy = False
        #  飞机的原形半径
        self.radius = self.rect.width / 2
        #   测试圆的范围是否符合图像大小
        #pygame.draw.circle(self.image, RED, self.rect.centerx, self.radius)
        # 2. 指定敌机的初始随机速度 1 ~ 3
        self.speed = random.randint(2, 5)

        # 3. 指定敌机的初始随机位置
        self.rect.bottom = -20


        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):

        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()

        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()

class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 判断是否第一次死亡，如果是则开启牢大模式
        self.die = True
        # 1. 调用父类方法，设置image&speed

        super().__init__("me1.png", speed=7)

        #  飞机的原形半径
        self.radius = 45
        #pygame.draw.circle(self.image, RED, self.rect.centerx, self.radius)
        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.health = 15
        self.lives = 1
        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        #设置飞机是否自动射击
        self.auto = True
    #  用于隐藏飞机的三条命，其实就是把飞机放到地图外，如果这个飞机死了，那么地图外的飞机立刻进来
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (SCREEN_RECT.centerx,SCREEN_RECT.bottom +500)
    def update(self):
        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys_pressed[pygame.K_UP]:
            self.rect.y += -self.speed
        elif keys_pressed[pygame.K_LEFT]:
            self.rect.x += -self.speed
        elif keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        else:
            pass
        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.bottom = SCREEN_RECT.bottom - 120

    def clear(cls):
        #  清除英雄类的精灵组
        cls.bullets.empty()
    def fire(self):
        if self.auto:

            print("发射子弹...")
            for i in (0, 1):

                # 1. 创建子弹精灵
                bullet = Bullet()
                # 2. 设置精灵的位置
                bullet.rect.bottom = self.rect.y - i * 20
                bullet.rect.centerx = self.rect.centerx

                # 3. 将精灵添加到精灵组
                self.bullets.add(bullet)
        else:
            print("发射子弹...")
            # 1. 创建子弹精灵
            bullet = Bullet()
            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y - 1 * 20
            bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)

class Hero_laoda(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 判断是否第一次死亡，如果是则开启牢大模式
        self.die = False
        # 1. 调用父类方法，设置image&speed
        super().__init__(image_name="me3.png", speed=10)
        #  飞机的原形半径
        self.radius = 45
        #pygame.draw.circle(self.image, RED, self.rect.centerx, self.radius)
        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.health = 100
        self.lives = 3
        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        #设置飞机是否自动射击
        self.auto = True
    #  用于隐藏飞机的三条命，其实就是把飞机放到地图外，如果这个飞机死了，那么地图外的飞机立刻进来
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (SCREEN_RECT.centerx,SCREEN_RECT.bottom +500)
    def update(self):
        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys_pressed[pygame.K_UP]:
            self.rect.y += -self.speed
        elif keys_pressed[pygame.K_LEFT]:
            self.rect.x += -self.speed
        elif keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        else:
            pass
        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.bottom = SCREEN_RECT.bottom - 120

    def clear(cls):
        #  清除英雄类的精灵组
        cls.bullets.empty()

    def fire(self):
        if self.auto:

            print("发射子弹...")
            for i in (0, 1):

                # 1. 创建子弹精灵
                bullet = Bullet()
                # 2. 设置精灵的位置
                bullet.rect.bottom = self.rect.y - i * 20
                bullet.rect.centerx = self.rect.centerx

                # 3. 将精灵添加到精灵组
                self.bullets.add(bullet)
        else:
            print("发射子弹...")
            # 1. 创建子弹精灵
            bullet = Bullet()
            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y - 1 * 20
            bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """英雄子弹精灵"""

    def __init__(self):

        # 调用父类方法，设置子弹图片，设置初始速度,设置负二为了子弹向上移动

        super().__init__(image_name="bullet1.png",speed =-10)

    def update(self):

        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁...")


# 陨石精灵类
class Meteorite(GameSprite):
    def __init__(self, ):

        super().__init__("enemy1_down3.png")
        # 2. 指定陨石的初始随机速度 5 ~ 10
        self.speed = random.randint(5,10)
        # 3. 指定陨石的初始随机位置
        self.rect.bottom = 0
        self.radius = 20

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
    def update(self):
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()
        move = random.randint(-4,4)
        self.rect.x += move
        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()
class Basketball(GameSprite):
    def __init__(self, ):

        images = ['kun1.png', 'kun2.png']
        image =  random.choice(images)

        super().__init__(image)
        # 2. 指定陨石的初始随机速度 5 ~ 10
        self.speed = random.randint(5,16)
        # 3. 指定陨石的初始随机位置
        self.rect.bottom = random.randint(5,15)
        self.radius = 20

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
    def update(self):
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()
        move = random.randint(-4,4)
        self.rect.x += move
        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()
class Prop(GameSprite):
    def __init__(self):
        dec = random.randint(1, 4)
        super().__init__(f"xuebao{dec}.png")
        # 2. 指定血包的初始随机速度 5 ~ 10
        self.speed = random.randint(2, 10)
        # 3. 指定血包的初始随机位置
        self.rect.bottom = 0
        self.radius = 20

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
    def update(self):
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()
        move = random.randint(-4,4)
        self.rect.x += move
        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()
class KUN(GameSprite):
    def __init__(self):
        super().__init__(image_name="kun.png", set_blue_transparent=True)
        #  需要被打击的次数
        self.Kun_hit = 100
        self.title = 100
        self.rect.x = 20
        #  kun的半径
        self.radius = 50
        # pygame.draw.circle(self.image, RED, self.rect.centerx, self.radius)
        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.centery = SCREEN_RECT.top + SCREEN_RECT.height // 4 - 200

        self.lives = 3
        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()
        #  用于隐藏飞机的三条命，其实就是把飞机放到地图外，如果这个飞机死了，那么地图外的飞机立刻进来
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (SCREEN_RECT.centerx, SCREEN_RECT.top + 12000)
    def update(self):
        #  让他左右横移
        move = random.randint(-40, 40)
        self.rect.x += move
        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.midtop = (SCREEN_RECT.centerx, SCREEN_RECT.top + 60)

