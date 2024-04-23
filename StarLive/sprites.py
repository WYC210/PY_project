import pygame
from settings import *
from random import randint, choice
from timer import Timer


class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
		#  防止 all_sprites返回报错
		self.groups = groups

class Interaction(Generic):
	def __init__(self, pos, size, groups, name):
		surf = pygame.Surface(size)
		super().__init__(pos, surf, groups)
		self.name = name

class Water(Generic):
	def __init__(self, pos, frames, groups):

		#  动画更新
		self.frames = frames
		#  索引下标
		self.frame_index = 0
		# 水池坐标
		self.pos = pos
		#  精灵更新
		super().__init__(
				pos = pos, 
				surf = self.frames[self.frame_index], 
				groups = groups, 
				z = LAYERS['water']) 

	def animate(self,dt):
		self.frame_index += 5 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]


	def update(self,dt):
		self.animate(dt)

class WildFlower(Generic):
	# 野花
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)

class Particle(Generic):
	def __init__(self, pos, surf, groups, z, duration = 200):
		super().__init__(pos, surf, groups, z)
		self.start_time = pygame.time.get_ticks()
		self.duration = duration

		# 白色的背景框
		mask_surf = pygame.mask.from_surface(self.image)
		new_surf = mask_surf.to_surface()
		new_surf.set_colorkey((0,0,0))
		self.image = new_surf

	def update(self,dt):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time > self.duration:
			self.kill()

class Tree(Generic):
	# 树
	def __init__(self, pos, surf, groups, name, player_add):
		super().__init__(pos, surf, groups)

		#  树属性
		self.health = 5
		self.alive = True
		#  树桩
		stump_path = f'./graphics/stumps/{"small" if name == "Small" else "large"}.png'
		self.stump_surf = pygame.image.load(stump_path).convert_alpha()

		# 苹果
		self.apple_surf = pygame.image.load('./graphics/fruit/apple.png')
		self.apple_pos = APPLE_POS[name]
		self.apple_sprites = pygame.sprite.Group()
		self.create_fruit()

		self.player_add = player_add

		# 音效
		self.axe_sound = pygame.mixer.Sound('./audio/axe.mp3')

	def damage(self):

		#  树的血量 - 1
		self.health -= 1

		# 玩家的音效
		self.axe_sound.play()

		#  根据血量减少随机杀死苹果精灵
		if len(self.apple_sprites.sprites()) > 0:
			random_apple = choice(self.apple_sprites.sprites())
			Particle(
				pos = random_apple.rect.topleft,
				surf = random_apple.image, 
				groups = self.groups[0],
				z = LAYERS['fruit'])
			self.player_add('apple')
			random_apple.kill()

	def check_death(self):
		if self.health <= 0:
			Particle(self.rect.topleft, self.image, self.groups[0], LAYERS['fruit'], 300)
			self.image = self.stump_surf
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
			self.alive = False
			self.player_add('wood')

	def update(self,dt):
		if self.alive:
			self.check_death()

	def create_fruit(self):
		for pos in self.apple_pos:
			if randint(0,10) < 2:
				x = pos[0] + self.rect.left
				y = pos[1] + self.rect.top
				Generic(
					pos = (x,y), 
					surf = self.apple_surf, 
					groups = [self.apple_sprites,self.groups[0]],
					z = LAYERS['fruit'])
class Fishi(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.timers = {'fishing': Timer(randint(1000,10000)),
					   'no anymore' : Timer(randint(1000,10000))}
		# 随机选择一个定时器启动
		self.timer_to_start = 'fishing' if randint(0, 1) == 0 else 'no_anymore'
	def update(self):
		self.fishing_rod()
	def fishing_rod(self):
		# 启动选定的定时器
		self.timers[self.timer_to_start].start()
		# 检查定时器是否启动
		if self.timers['fishing'].timer.is_alive():
			print("已启动 'fishing' 定时器")
		elif self.timers['no_anymore'].timer.is_alive():
			print("已启动 'no_anymore' 定时器")



