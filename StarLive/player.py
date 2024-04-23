import time

import pygame
from settings import *
from support import *
from timer import Timer
from sprites import Water , Fishi
from random import randint,random



class Player(pygame.sprite.Sprite):
	"""
	pos:  用来指定位置
	group: 传进来精灵组可以直接创建

	"""
	def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop):
		super().__init__(group)
		#  必须置顶
		self.import_assets()
		#  人物状态
		self.status = 'down_idle'
		#  帧索引
		self.frame_index = 0
		# 常规属性
		self.image = self.animations[self.status][self.frame_index]
		# 获取图片大小
		self.rect = self.image.get_rect(center = pos)
		#  图片的Z轴
		self.z = LAYERS['main']
		# 运动常量
		self.direction = pygame.math.Vector2()
		#  获取位置
		self.pos = pygame.math.Vector2(self.rect.center)
		#  速度
		self.speed = 200
		# 物体的碰撞体积
		self.hitbox = self.rect.copy().inflate((-126,-70))
		self.collision_sprites = collision_sprites
		# 用于更新新手任务提示的索引
		self.tip = 0
		#  定时器
		self.timers = {
			'tool use': Timer(350,self.use_tool),
			'tool switch': Timer(200),
			'seed use': Timer(100,self.use_seed),
			'seed switch': Timer(200),
			'fishing': Timer(1000)
		}


		# 工具类
		self.tools = ['hoe','axe','water','fishi']
		#  工具索引
		self.tool_index = 2
		self.selected_tool = self.tools[self.tool_index]

		# 种子
		self.seeds = ['corn', 'tomato']
		self.seed_index = 0
		self.selected_seed = self.seeds[self.seed_index]

		# 钓鱼相关属性初始化
		self.fishing = False  # 是否正在钓鱼
		self.fish_caught = 0  # 是否钓到鱼
		self.fish_num = 0 # 钓鱼数字

		# 库存
		self.item_inventory = {
			'wood':   20,
			'apple':  20,
			'corn':   20,
			'tomato': 20
		}
		self.seed_inventory = {
		'corn': 5,
		'tomato': 5
		}
		self.money = 200

		#  交互
		self.tree_sprites = tree_sprites
		self.interaction = interaction
		self.sleep = False
		self.soil_layer = soil_layer
		self.toggle_shop = toggle_shop

		# 音乐
		self.watering = pygame.mixer.Sound('./audio/water.mp3')
		self.watering.set_volume(0.2)


	def fishi(self):
		if self.status == 'down_fishi':
			self.fishing = True
			self.status = 'down_fishing'
			# 定时器
			self.timers['fishing'].activate()
			print(self.status)


	def reel_in_fish(self):
		# 模拟收杆的动作
		self.fish_caught = randint(1,11)
		if self.fish_caught > 5:
			print("你钓到了一条鱼！")
		# 这里可以执行钓到鱼之后的操作，例如增加钓到的鱼的数量等
		else:
			print("很遗憾，什么都没钓到。")
		# 重置钓鱼状态和计时器
		self.fishing = False
		self.status = 'down'


	def use_tool(self):
		if self.selected_tool == 'hoe':
			self.soil_layer.get_hit(self.target_pos)
		
		if self.selected_tool == 'axe':
			for tree in self.tree_sprites.sprites():
				if tree.rect.collidepoint(self.target_pos):
					tree.damage()
		
		if self.selected_tool == 'water':
			self.soil_layer.water(self.target_pos)
			self.watering.play()

	def get_target_pos(self):

		self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

	def use_seed(self):
		if self.seed_inventory[self.selected_seed] > 0:
			self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
			self.seed_inventory[self.selected_seed] -= 1

	def import_assets(self):
		#  引进外部图片
		#  引入这些时间的动画文件夹
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'down_fishi': [] , 'down_fishing' : [] ,
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

		for animation in self.animations.keys():
			full_path = './graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self,dt):
		# 如果当前处于钓鱼状态，直接播放钓鱼动画
		if self.status == 'down_fishing':
			self.image = self.animations[self.status][0]
			print(100)
		else:
			self.frame_index += 4 * dt
			#  如果帧索引大于他的状态长度，那么就归零
			if self.frame_index >= len(self.animations[self.status]):
				self.frame_index = 0
			#  确保帧索引是整数
			self.image = self.animations[self.status][int(self.frame_index)]



	def input(self):
		#  获取按键的列表
		keys = pygame.key.get_pressed()
		#  如果玩家在使用工具，那么就不可以移动或者再次使用工具
		if not self.timers['tool use'].active and not self.sleep and not self.fishing:
			# 按键
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# 使用工具-空格
			if keys[pygame.K_SPACE] and self.selected_tool != 'fishi' :

				# 定时器
				self.timers['tool use'].activate()

				self.direction = pygame.math.Vector2()
				self.frame_index = 0
				# 更换新手教程提示
				if self.tip == 2:
					self.tip = 3
				if self.tip == 4 and self.selected_tool == 'water':
					self.tip = 5
			elif  keys[pygame.K_SPACE] and self.selected_tool == 'fishi' and 657 < self.pos.x <= 2490 and self.pos.y == 2109:
				# 更新状态为钓鱼状态

				print("在钓鱼")
				# 生成一个5到10秒之间的随机数
				self.fish_num = randint(30, 70)
				self.status = 'down_fishi'
				self.fishi()

				# 定时器
				self.timers['tool use'].activate()

				self.direction = pygame.math.Vector2()
				self.frame_index = 0
			# 切换工具-q
			if keys[pygame.K_q] and not self.timers['tool switch'].active:
				#  激活定时器
				self.timers['tool switch'].activate()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
				self.selected_tool = self.tools[self.tool_index]
				# 更换新手教程提示
				if self.tip == 0:
					self.tip = 1

			# 使用种子-f
			if keys[pygame.K_f]:

				#  激活定时器
				self.timers['seed use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0
				# 更换新手教程提示
				if self.tip == 3:
					self.tip = 4

			# 切换种子-e
			if keys[pygame.K_e] and not self.timers['seed switch'].active:
				#  激活定时器
				self.timers['seed switch'].activate()
				self.seed_index += 1
				self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
				self.selected_seed = self.seeds[self.seed_index]
				# 更换新手教程提示
				if self.tip == 1:
					self.tip = 2

			#  回车
			if keys[pygame.K_RETURN]:
				#  立马把角色的初始速度设置为 0
				self.direction = pygame.math.Vector2()
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Trader':
						self.toggle_shop()
						# 更换新手教程提示
						if self.tip == 5:
							self.tip = 6
					else:
						self.status = 'left_idle'
						self.sleep = True
						# 更换新手教程提示
						if self.tip == 6:
							self.tip = 7

	def get_status(self):
		#  判断玩家此时是否处于空闲状态
		#  如果玩家没有移动 ，那么添加_状态idle 到 status
		# 如果当前处于钓鱼状态，直接播放钓鱼动画
		if self.status == 'down_fishing':
			self.status = self.status.split('_')[0] + '_fishing'
		if self.direction.magnitude() == 0 and not self.fishing:
			#  这样防止无限的在状态后面添加_idle，会造成left_water_idle_idle_idle
			self.status = self.status.split('_')[0] + '_idle'

		# 工具使用
		if self.timers['tool use'].active and not self.fishing:
			self.status = self.status.split('_')[0] + '_' + self.selected_tool

	def update_timers(self):
		#  更新定时器
		for timer in self.timers.values():
			timer.update()

	def collision(self, direction):
		# 碰撞处理
		for sprite in self.collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					#  如果它等于水平
					if direction == 'horizontal':
						if self.direction.x > 0: # 向左移动
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: # 向右移动
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx
					#  如果它等于垂直
					if direction == 'vertical':
						if self.direction.y > 0:  # 向下移动
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0:  # 向上移动
							self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery

	def move(self,dt):
		#  归一化向量,根据毕达哥拉斯定理（勾股定理）同时按下上和左，他的速度是根号二，为了防止这种情况
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()
		#  变化的位移 = 方向 * 速度 * 时间间隔
		#  水平移动
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		#  垂直移动
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def update(self, dt):
		self.input()
		self.get_status()
		self.update_timers()
		self.get_target_pos()
		# 钓鱼状态的更新
		self.move(dt)
		self.animate(dt)
		if  self.timers['fishing'].active and self.fishing:

			self.fishing = False
			self.reel_in_fish()
