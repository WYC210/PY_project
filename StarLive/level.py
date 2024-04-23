import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu

class Level:
	def __init__(self):
		# 获取显示界面
		self.display_surface = pygame.display.get_surface()

		# 创建所有精灵组
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()
		#  更新
		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.reset, self.player)

		# 天空
		self.rain = Rain(self.all_sprites)
		#  决定是否下雨
		self.raining = randint(0,10) > 6
		self.soil_layer.raining = self.raining
		self.sky = Sky()

		# 商店
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False

		# 音乐
		self.success = pygame.mixer.Sound('./audio/success.wav')
		self.success.set_volume(0.3)
		self.music = pygame.mixer.Sound('./audio/music.mp3')
		self.music.play(loops = -1)

	def setup(self):
		#  导入地图
		tmx_data = load_pygame('./data/map.tmx')

		#  房子的地板和地毯
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])
		#  房子的墙和家具
		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

		#  栅栏
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

		#  水池
		water_frames = import_folder('./graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)
			print("瓦片坐标：", x, y)

		#  树林
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)

		#  野花
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		#  地图的边界
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		#  玩家的初始生成位置
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), 
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer,
					toggle_shop = self.toggle_shop

				)

			
			if obj.name == 'Bed':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Trader':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)


		Generic(
			pos = (0,0),
			surf = pygame.image.load('./graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def player_add(self,item):
		# 玩家获得物品
		self.player.item_inventory[item] += 1
		self.success.play()

	def toggle_shop(self):
		# 商店页面是否打开
		self.shop_active = not self.shop_active

	def reset(self):
		# 更新植物
		self.soil_layer.update_plants()

		# 更新土，当新的一天来到，去除湿润的土
		self.soil_layer.remove_water()
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		if self.raining:
			self.soil_layer.water_all()

		#  树上的苹果
		for tree in self.tree_sprites.sprites():
			for apple in tree.apple_sprites.sprites():
				apple.kill()
			tree.create_fruit()

		# 天空颜色
		self.sky.start_color = [255,255,255]

	def plant_collision(self):
		#  植物收获
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				#  当玩家撞到成熟的植物，那么它可以直接收获
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.player_add(plant.plant_type)
					plant.kill()
					#  粒子效果
					Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
					# 成功收获的时候移除，之前存在的 P
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def run(self,dt):
		
		# 绘图逻辑
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)
		
		# 更新商店
		if self.shop_active:
			self.menu.update()
		else:
			self.all_sprites.update(dt)
			self.plant_collision()
		# 提示操作的文字
		self.tips()

		# 天气
		self.overlay.display()
		if self.raining and not self.shop_active:
			self.rain.update()
		self.sky.display(dt)

		# 新一天的过度动画
		if self.player.sleep:
			self.transition.play()

	def tips(self):
		# 新手教程的提示
		tip = self.player.tip
		# 新手教程
		font_name = "Microsoft YaHei"  # 使用微软雅黑字体
		font = pygame.font.SysFont(font_name, 15)  # 加载字体
		# 根据不同阶段提示不同的文字
		if tip == 0:
			text_tip = font.render('#新手教程', False, 'RED')
			text_tips = font.render('你可以按 Q 切换工具到 锄头', False, 'Black')
		elif tip == 1 :
			text_tip = font.render('#你已经完成了第一步', False, 'RED')
			text_tips = font.render('你可以按 E 切换种子', False, 'Black')
		elif tip == 2:
			text_tip = font.render('#你已经完成了第二步', False, 'RED')
			text_tips = font.render('你可以按 空格 使用工具', False, 'Black')
		elif tip == 3:
			text_tip = font.render('#你已经完成了第三步', False, 'RED')
			text_tips = font.render('你可以按 F 种植种子', False, 'Black')
		elif tip == 4:
			text_tip = font.render('#你已经完成了第四步', False, 'RED')
			text_tips = font.render('按 空格 使用水壶给植物浇水', False, 'Black')
		elif tip == 5:
			text_tip = font.render('#你已经完成了第五步', False, 'RED')
			text_tips = font.render('按 回车 可以跟商人交易一些植物种子', False, 'Black')
		elif tip == 6:
			text_tip = font.render('#你已经完成了第七步', False, 'RED')
			text_tips = font.render('回到床上按 回车 睡觉', False, 'Black')
		elif tip == 7:
			text_tip = font.render('#你已经完成了所有的教程', False, 'RED')
			text_tips = font.render('#开始你的养老生活', False, 'RED')

		text_rects = text_tip.get_rect(midbottom=(100, 120))
		text_rects0 = text_tips.get_rect(midbottom=(80, 100))
		self.display_surface.blit(text_tip, text_rects0)
		self.display_surface.blit(text_tips, text_rects)



class CameraGroup(pygame.sprite.Group):
	#  摄像机类
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		#  摄像机原理
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
		#  根据层级的不同，让主角正确的在地图绘制之后在绘制
		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)
					#  测试玩家的红框和范围
					# if sprite == player:
					# 	pygame.draw.rect(self.display_surface,'red',offset_rect,5)
					# 	hitbox_rect = player.hitbox.copy()
					# 	hitbox_rect.center = offset_rect.center
					# 	pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
					# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
					# 	pygame.draw.circle(self.display_surface,'blue',target_pos,5)
