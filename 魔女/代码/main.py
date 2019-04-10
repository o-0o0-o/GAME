
import pygame,sys,time,random,settings_file
		
def main():
	
		
	global x_move,y_move,ghost_list
	
	# 初始化pygame
	pygame.init()


	
	settings = settings_file.Settings()
	enviorment = Enviorment()	
	calculate = Calculate()
	control = Control()
	
	# 创建pygame显示层
	screen = pygame.display.set_mode( (settings.screen_width,settings.screen_height) )
	pygame.display.set_caption('游戏')
	

	#背景的RGB填充	
	screen.fill((100,100,120))		

	#加载中的图片显示
	enviorment.loading_display(settings,screen)
	# 刷新pygame显示层
	pygame.display.flip()	
	
	first_time = True
	
	x_move,y_move = 0,0
	
	
	

	
	ghost_list = []
	ore_list = [] #另一个列表（设计缺陷
	

	
	for i in range(3):
		magic_ore = Magic_ore(settings,screen,0,0,0,0,0,0,0,100,0)
		ore_list.append(magic_ore)
	
	fountain = Fountain(settings,screen,0,0,0,0,0,0,0,100,0)
		
	magic_ball = Magic_ball(settings,screen,0,0,0,0,0,0)

	frog_curse = Frog_curse(settings,screen,0,0,0,0,0,0)
	
	magic_drive = Magic_drive(settings,screen,0,0,0,0,0,0)
	
	cure = Cure(settings,screen,0,0,0,0,0,0)
	
	magic_barrier = Magic_barrier(settings,screen,0,0,0,0,0,0)
	
	telekinesis = Telekinesis(settings,screen,0,0,0,0,0,0)
	
	earthquake = Earthquake(settings,screen,0,0,0,0,0,0)
	
	revive = Revive(settings,screen,0,0,0,0,0,0)
	
	
	
	status = 1	#1代表初始状态,2代表游戏中状态
	
	
	#底色背景图片的处理
	back_pic =  pygame.image.load('images/地图_沙漠.bmp')
	back_pic = pygame.transform.smoothscale(back_pic, (8000, 8000))	
	back_rect = back_pic.get_rect()	
	
	game_time = 0
	
	if settings.music:
		pygame.mixer.init()
		pygame.mixer.music.load('music/4181.mp3')
		pygame.mixer.music.play(-1)
		
	while True:

		clock = pygame.time.Clock()
		time_passed = clock.tick(settings.fps_number)		
		
		if status==1:
			
			
			mouse_x,mouse_y=pygame.mouse.get_pos()
			
			
			enviorment.start_display(settings,screen)
			
			for event in pygame.event.get():
			
				if event.type == pygame.QUIT:
					sys.exit()		
			
				
				elif event.type == pygame.MOUSEBUTTONDOWN:
					
					#点击开始按钮
					if enviorment.check_if_start_rect_collidepoint(settings,screen,mouse_x,mouse_y):
						status=2		
					
					if enviorment.check_if_difficulty_level_rect_collidepoint(settings,screen,mouse_x,mouse_y):
						enviorment.change_difficulty_level()
							

			
			enviorment.check_if_point(screen,mouse_x,mouse_y)						
						

		if status==2:		
			game_time += 1	

			control.try_to_add_ghost(settings,screen,enviorment,game_time)
			
			if first_time:
				
				control.new_ghosts(settings,screen,enviorment)
				
				
				
				enviorment.loading_display(settings,screen)
				
				
				magician = Magician(settings,screen,0.5*settings.screen_width,0.5*settings.screen_height,settings.init_power,settings.init_friction,[0,0],0,settings.init_blood,0,0,settings.init_magic,settings.init_max_blood,settings.init_max_magic,0,0,0,enviorment)
				
				#初始化时的代码放这儿
				first_time = False
			
			#背景的RGB填充
			enviorment.playing_display(settings,screen)
			
			#底色背景图片的描绘
			screen.blit( back_pic,(int( x_move - 0.5*back_rect.width),int( y_move - 0.5*back_rect.height)) )	

			
			fountain.give_magic(settings,screen,magician,calculate)
			
			for i in range(len(ore_list)):
				ore_list[i].give_magic(settings,screen,magician,calculate)
			
			#强制打断
			magic_drive.if_can_execute(magician,settings)
			cure.if_can_execute(magician,settings)
			magic_barrier.if_can_execute(magician,settings)
			frog_curse.if_can_execute(magician,settings)
			telekinesis.if_can_execute(magician,settings)	
			earthquake.if_can_execute(magician,settings)
	

			#女巫的移动
			magician.act(settings,screen,calculate)
			
	
			#魔法泉的绘画
			fountain.draw_and_display(settings,screen,x_move,y_move)
			
		
			
			
			
			#鬼魂的活动
			for i in reversed(range(len(ghost_list))):
				if ghost_list[i].blood<0:#清除死亡的幽灵
					ghost_list.pop(i)
					continue
				ghost_list[i].act(magician,calculate,screen,fountain)
				ghost_list[i].draw_blood(screen,settings)
				ghost_list[i].try_to_attack(calculate,magician,screen)
				ghost_list[i].change_status()
				ghost_list[i].stain_fountain(calculate,fountain,settings,screen)
			
				
			#魔法的内部效果+图像效果


					
			magic_barrier.try_to_execute(magician,settings,screen)
			magic_barrier.turn_on_display_font(screen,magician)			
			
			magic_ball.try_to_execute(magician,settings,screen,calculate,ghost_list,x_move,y_move)

			magic_drive.try_to_execute(magician,settings)
			magic_drive.turn_on_display_font(screen,magician)
			
			frog_curse.try_to_execute(magician,settings,screen)
			frog_curse.turn_on_display_font(screen,magician)
			
			cure.try_to_execute(magician,settings)
			cure.turn_on_display_font(screen,magician)
			
			
			telekinesis.try_to_execute(magician,settings,screen,calculate,ghost_list)			
			telekinesis.turn_on_display_font(screen,magician)
			
			earthquake.try_to_execute(magician,settings,screen,calculate,ghost_list)			
			earthquake.turn_on_display_font(screen,magician)
			
			revive.try_to_execute(magician,settings)
			revive.turn_on_display_font(screen,magician)
			
			
			
			
			_list = ghost_list + ore_list + [magician] #所有需要判定绘画顺序的都放在这个列表中
			
			if 1: #节约性能
			
				#冒泡，让y值最大的沉底
				for i in range(len(_list)-1):
					for j in range(len(_list)-1-i):
						if (_list[j].y > _list[j+1].y):
							_list[j],_list[j+1] = _list[j+1],_list[j]			
			
			#怪物绘画
			for i in range(len(_list)):
				if calculate.distance_check(magician.x,magician.y,_list[i].x,_list[i].y,600): #一定范围之内的才绘画
					_list[i].draw_and_display(settings,screen,x_move,y_move,magician)
			
			
			
			
		
		
			#绘画红和蓝
			magician.display_blue_and_red(settings,screen)	
		
			#魔法泉
			fountain.show_status(settings,screen,calculate,magician)
			fountain.clean_up()
			
			#矿石
			for i in range(len(ore_list)):
				ore_list[i].show_status(settings,screen,calculate,magician)
			
			magician.lose_blood_display(screen)
			
			for event in pygame.event.get():
			
				if event.type == pygame.QUIT:
					sys.exit()		

				elif event.type == pygame.MOUSEBUTTONDOWN:
					frog_curse.curse(screen,calculate,ghost_list,magician)
					magician.move_status_change()
					
				elif event.type == pygame.MOUSEBUTTONUP:
					pass
					
				elif event.type == pygame.KEYUP :
				
					if event.key == pygame.K_c:
						cure.turn_off()
					elif event.key == pygame.K_x:
						telekinesis.turn_off()
					elif event.key == pygame.K_v:
						earthquake.turn_off()
						
					'''
					if event.key == pygame.K_LEFT or event.key == ord('a'):
						walk_left = False
					
					if event.key == pygame.K_UP or event.key == ord('w'):
						walk_up = False
						
					if event.key == pygame.K_DOWN or event.key == ord('s'):
						walk_down = False						
					'''	
				elif event.type == pygame.KEYDOWN :
				
					if event.key == pygame.K_a:
						if magic_drive.if_can_execute(magician,settings):
							magic_drive.turn_on()

					elif event.key == pygame.K_SPACE:	
						if magic_ball.if_can_execute(magician,settings):	
							magic_ball.turn_on(calculate,magician,settings)							
					elif event.key == pygame.K_c:
						if cure.if_can_execute(magician,settings):
							cure.turn_on()
							
					elif event.key == pygame.K_x:		
						if telekinesis.if_can_execute(magician,settings):	
							telekinesis.turn_on()	
							
					elif event.key == pygame.K_v:	
						if earthquake.if_can_execute(magician,settings):	
							earthquake.turn_on()
							
					elif event.key == pygame.K_z:	
						if frog_curse.if_can_execute(magician,settings):	
							frog_curse.turn_on()
							
					elif event.key == pygame.K_s:
						magic_barrier.turn_on_and_off()
					'''					
					if event.key == pygame.K_LEFT or event.key == ord('a'):
						walk_left = True

					if event.key == pygame.K_UP or event.key == ord('w'):
						walk_up = True
						
					if event.key == pygame.K_DOWN or event.key == ord('s'):
						walk_down = True				
				
					'''


			
			#受到干扰而被中断的技能

			
		#鼠标代替性质的光标
		enviorment.point_display(screen)			
		pygame.mouse.set_visible(False)
		
		
		# 刷新pygame显示层
		pygame.display.flip()	


		
class Enviorment():
	def __init__(self):
		self.t =0
		self.difficulty_level = 1
		self.start_pointed = False
		self.difficulty_level_pointed = False
		
		
	#开始画面的内容显示
	def start_display(self,settings,screen):

		#背景的RGB填充	
		screen.fill((255,255,255))		

		#背景显示
		pic =  pygame.image.load('images/初始背景.bmp')					
		a_rect = pic.get_rect()					
		screen.blit( pic,(0,0) )			
		
		#开始画面的字
		font = pygame.font.SysFont('SimHei',40)	
		
		
		#开始按钮的相关内容
		self.start_rect_list = [settings.screen_width*0.35,settings.screen_height*0.3,settings.screen_width*0.3,settings.screen_height*0.2]
		start_rect = pygame.Rect(self.start_rect_list)			
		pygame.draw.rect( screen,settings.setting_rect_color,start_rect,8 )	
	
		s = font.render(("开始游戏"),True,settings.start_font_color)			
		turn_rect = s.get_rect()
		turn_rect.center = start_rect.center
		screen.blit(s,turn_rect)
		
		
		#特效显示
		if self.start_pointed:

			pic =  pygame.image.load('images/显示特效.bmp')
			_rect = pic.get_rect()						
			_rect.center = turn_rect.center
			screen.blit( pic,_rect )		
		
	
	
		#难度设置的相关内容
		self.difficulty_level_rect_list = [settings.screen_width*0.35,settings.screen_height*0.6,settings.screen_width*0.3,settings.screen_height*0.2]
		start_rect = pygame.Rect(self.difficulty_level_rect_list)			
		pygame.draw.rect( screen,settings.setting_rect_color,start_rect,8 )

		if	self.difficulty_level ==1:
			str = "难度:萌新" 
		elif self.difficulty_level ==2:
			str = "难度:一般"		
		elif self.difficulty_level ==3:
			str = "难度:较难"		
		elif self.difficulty_level ==4:
			str = "难度:巨难"
		
		s = font.render((str),True,settings.start_font_color)
		turn_rect = s.get_rect()
		turn_rect.center = start_rect.center
		screen.blit(s,turn_rect)
			
		
		#特效显示
		if self.difficulty_level_pointed:	

			pic =  pygame.image.load('images/显示特效.bmp')
			_rect = pic.get_rect()						
			_rect.center = turn_rect.center
			screen.blit( pic,_rect )	
			
		
		
	def check_if_point(self,screen,mouse_x,mouse_y):
		
		_rect = pygame.Rect(self.start_rect_list)	

		if _rect.collidepoint(mouse_x,mouse_y):
			self.start_pointed = True
		else:
			self.start_pointed = False
			

		_rect = pygame.Rect(self.difficulty_level_rect_list)	

		if _rect.collidepoint(mouse_x,mouse_y):
			self.difficulty_level_pointed = True
		else:
			self.difficulty_level_pointed = False
		
		
	
	def check_if_start_rect_collidepoint(self,settings,screen,mouse_x,mouse_y):

		_rect = pygame.Rect(self.start_rect_list)	

		if _rect.collidepoint(mouse_x,mouse_y):
			return True
	
	
	def check_if_difficulty_level_rect_collidepoint(self,settings,screen,mouse_x,mouse_y):
	
	
		_rect = pygame.Rect(self.difficulty_level_rect_list)	

		if _rect.collidepoint(mouse_x,mouse_y):
			return True
			
	def change_difficulty_level(self,):
		
		if self.difficulty_level<4:
			self.difficulty_level += 1
		else:
			self.difficulty_level = 1
			
	
	def playing_display(self,settings,screen):

		#背景的RGB填充	
		screen.fill(settings.playing_groundcolor)	


	def point_display(self,screen):
		#鼠标
		mouse_x,mouse_y=pygame.mouse.get_pos()
		pic =  pygame.image.load('images/鼠标点.bmp')	
				
		a_rect = pic.get_rect()
					
		screen.blit( pic,( int(mouse_x - 0.5*a_rect.width),int(mouse_y - 0.5*a_rect.height)) )			
		
	
	def loading_display(self,settings,screen):
		#正在加载显示
		pic =  pygame.image.load('images/正在加载字样.bmp')	
				
		a_rect = pic.get_rect()
					
		screen.blit( pic,(settings.screen_width*0.5 - 0.5*a_rect.width,settings.screen_height*0.5 - 0.5*a_rect.height) )		
	
	
class Calculate():
	
	def distance_check(self,x1,y1,x2,y2,distance):
		#距离之内，返回True
		
		if ((x1-x2)**2+(y1-y2)**2)**0.5<distance:
			return True
		

	def another_direction_is(self,my_x,my_y,another_x,another_y): #返回代表有向矢量的列表表示方向
				#为什么一开始我只想到用斜率啊？？分类讨论快活赛神仙，枯了
		
		long = ((another_x-my_x)**2 + (another_y-my_y)**2)**0.5	
		if long==0:
			return [0,0]
		else:
			return [(another_x-my_x)/long,(another_y-my_y)/long]
					#目标在右，则第一个元素为正

				

					
		
	
					
					
class Object():

	
	def __init__(self,settings,screen,x,y,power,friction,walk_speed,interference,blood,status,name):	

		self.x = x
		self.y = y	
		self.power = power
		self.friction = friction
		self.walk_speed = walk_speed
		#目前受到的干扰强度
		self.interference = interference
		self.blood = blood
		self.status = ''
		self.name = ''
		
	def draw_and_display(self,settings,screen,x_move,y_move,magician):
		#显示本物体于屏幕上
		
		if self.name=="魔法师":
			if magician.mouse_direction=="right":
				pic =  pygame.image.load('images/魔女_右.bmp')
					
			else:
				pic =  pygame.image.load('images/魔女_左.bmp')
			
		elif self.name=="盾":
			if self.status == "normal":
				pic =  pygame.image.load('images/幽灵_盾.bmp')
			elif self.status == "red":
				pic =  pygame.image.load('images/幽灵_盾(红).bmp')
				
		elif self.name=="速":
			if self.status == "normal":
				pic =  pygame.image.load('images/幽灵_速.bmp')
			elif self.status == "red":
				pic =  pygame.image.load('images/幽灵_速(红).bmp')	
				
		elif self.name=="狡":
			if self.status == "normal":
				pic =  pygame.image.load('images/幽灵_狡.bmp')
			elif self.status == "red":
				pic =  pygame.image.load('images/幽灵_狡(红).bmp')	
				
		elif self.name=="怒":
			if self.status == "normal":
				pic =  pygame.image.load('images/幽灵_怒.bmp')
			elif self.status == "red":
				pic =  pygame.image.load('images/幽灵_怒(红).bmp')	



		elif self.name=="咒":
			if self.status == "normal":
				pic =  pygame.image.load('images/幽灵_咒.bmp')
			elif self.status == "red":
				if self.mode_of_action['attack_cd']:
					pic =  pygame.image.load('images/幽灵_咒(红)(攻击冷却中).bmp')	
				else:
					pic =  pygame.image.load('images/幽灵_咒(红).bmp')	
				
		a_rect = pic.get_rect()
					
		screen.blit( pic,(int(self.x + x_move - 0.5*a_rect.width),int(self.y + y_move - 0.5*a_rect.height)) )			
		

	
class Magician(Object):
	def __init__(self,settings,screen,x,y,power,friction,walk_speed,interference,blood,status,name,magic,init_max_blood,init_max_magic,mouse_x,mouse_y,mouse_direction,enviorment):
	
		super().__init__(settings,screen,x,y,power,friction,walk_speed,interference,blood,status,name)
		
		 
		self.difficulty_level_change = 1+1/enviorment.difficulty_level
		
		self.interference = 0
		self.magic = int(magic * self.difficulty_level_change)
		self.max_blood = int(init_max_blood * self.difficulty_level_change)
		self.max_magic = int(init_max_magic * self.difficulty_level_change)
		self.mouse_x,self.mouse_y = 0,0
		self.mouse_direction = 'middle'
		self.mouse_relative_direction_x,self.mouse_relative_direction_y = 0,0
		self.lose_blood_photos = 0
		self.name = "魔法师"
		self.moving = False
		
	#绘画魔法条和血条
	def display_blue_and_red(self,settings,screen):
		
		#蓝红外壳
		pic =  pygame.image.load('images/蓝与红.bmp')
		a_rect = pic.get_rect()
					
		screen.blit( pic,(20,0) )			
		
		
		font = pygame.font.SysFont('Arial',30)	
		if self.magic<0:	#不能为负数
			s = font.render(("0"+"/"+str(self.max_magic)),True,(53,79,207) )
		elif self.magic>self.max_magic:#不能超过最大值
			s = font.render((str(self.max_magic)+"/"+str(self.max_magic)),True,(53,79,207) )
		else:
			s = font.render((str(int(self.magic))+"/"+str(self.max_magic)),True,(53,79,207) )
		
		turn_rect = s.get_rect()
		turn_rect.center = (95,88)
		screen.blit(s,turn_rect)			


		if self.blood<0:	#不能为负数		
			s = font.render("0"+"/"+str(self.max_blood),True,(207,53,58) )		
		elif self.blood>self.max_blood:	#不能超过最大值		
			s = font.render(str(self.max_blood)+"/"+str(self.max_blood),True,(207,53,58) )
		else:
			s = font.render(str(int(self.blood))+"/"+str(self.max_blood),True,(207,53,58) )
		turn_rect = s.get_rect()
		turn_rect.center = (287,88)
		screen.blit(s,turn_rect)		
	
	def act(self,settings,screen,calculate):
		if self.interference>0:
			self.interference = 0
			
		self.move(settings,screen,calculate)

	def move_status_change(self):
		if self.moving:
			self.moving = False
		else:
			self.moving = True
			
		
		
		
	def move(self,settings,screen,calculate):
		#移动
		global x_move,y_move
		center_x,center_y = settings.screen_width*0.5,settings.screen_height*0.5
		
		self.mouse_x,self.mouse_y=pygame.mouse.get_pos()
	
		#速度改变位置
		self.x += self.walk_speed[0]
		x_move -= self.walk_speed[0]
		self.y += self.walk_speed[1]
		y_move -= self.walk_speed[1]
		
		all_walk_speed = (self.walk_speed[0]**2 + self.walk_speed[1]**2)**0.5	
		
		
		
		if all_walk_speed>0:
			accelerated_speed = self.power/all_walk_speed
			if accelerated_speed>4:
				accelerated_speed=4
		else:
			accelerated_speed = 0.001
			
		#处于移动状态
		if self.moving:
			
			#扫帚加速：90以下即可发动
			if self.interference < 90:
			
				#加速度改变速度
			
				if calculate.distance_check(self.mouse_x,self.mouse_y,0.5*settings.screen_width,0.5*settings.screen_height,0.1*settings.screen_width): #若鼠标和人物贴近，不加速
					pass
					
				else:	
				
					[self.mouse_relative_direction_x,self.mouse_relative_direction_y] = calculate.another_direction_is(center_x,center_y,self.mouse_x,self.mouse_y)
					
					
					if self.mouse_relative_direction_x>0:
						self.walk_speed[0] += accelerated_speed * (self.mouse_relative_direction_x**2)
					else:	
						self.walk_speed[0] -= accelerated_speed * (self.mouse_relative_direction_x**2)
						
					if self.mouse_relative_direction_y>0:	
						self.walk_speed[1] += accelerated_speed * (self.mouse_relative_direction_y**2)
					else: 
						self.walk_speed[1] -= accelerated_speed * (self.mouse_relative_direction_y**2)
					
					
					
				if (self.mouse_x-center_x)>0:
					self.mouse_direction = 'right'
				elif (self.mouse_x-center_x)<0:
					self.mouse_direction = 'left'
				elif self.mouse_x==center_x:
					self.mouse_direction = 'middle'					
						
					
		
		
		#摩擦力带来的加速度改变速度		
		[speed_relative_direction_x,speed_relative_direction_y] = calculate.another_direction_is(0,0,self.walk_speed[0],self.walk_speed[1])
		
		if speed_relative_direction_x>0:
			self.walk_speed[0] += self.friction * (speed_relative_direction_x**2)
		else:	
			self.walk_speed[0] -= self.friction * (speed_relative_direction_x**2)
					
		if speed_relative_direction_y>0:	
			self.walk_speed[1] += self.friction * (speed_relative_direction_y**2)
		else: 
			self.walk_speed[1] -= self.friction * (speed_relative_direction_y**2)		
		
	def lose_blood(self,damage,interference,screen):
		
		self.blood -= damage
		self.interference = interference
		self.turn_on_lose_blood_display(screen)
	
	def turn_on_lose_blood_display(self,screen):
		
		self.lose_blood_photos = 10
	
	def lose_blood_display(self,screen):
		
		if self.lose_blood_photos>=1:
			
			if self.lose_blood_photos>6:
				pic =  pygame.image.load('images/受伤6_副本.bmp')	
			else:
				pic =  pygame.image.load('images/受伤'+str(int(self.lose_blood_photos))+'_副本.bmp')	
				
			#pic = pygame.transform.smoothscale(pic, (4000, 4000))	
			a_rect = pic.get_rect()
						
			screen.blit( pic,(0,0) )	
			self.lose_blood_photos -= 1	
	
	
		
		
class Fountain(Object):

	def __init__(self,settings,screen,*args):	
		super().__init__(settings,screen,*args)		
		
		self.x,self.y = 0,0
		self.max_magic = 2500
		self.magic = 2500 
		self.width = 250
		self.height = 150
		self.show_status_distance = 250
		self.name = "魔法泉"
	
			
	def give_magic(self,settings,screen,magician,calculate):
		#给予魔法值
		
		
		if (abs(self.x - magician.x)<self.width) and (abs(self.y - magician.y)<self.height) :
		
			if self.magic >= self.max_magic:
			
				if magician.magic < magician.max_magic:
					magician.magic += random.uniform(0.25,1.25)
			
				
		
	
	def draw_and_display(self,settings,screen,x_move,y_move):
		#显示本物体于屏幕上

		pic = pygame.image.load('images/魔法泉.bmp')
		a_rect = pic.get_rect()
		screen.blit( pic,(int(self.x + x_move - 0.5*a_rect.width),int(self.y + y_move - 0.5*a_rect.height)) )
	
	
	def show_status(self,settings,screen,calculate,magician):
		#显示文字描述
		
		if (abs(self.x - magician.x)<self.width) and (abs(self.y - magician.y)<self.height) :
			
			font = pygame.font.SysFont('SimHei',30)	

			if self.magic >= self.max_magic:
				s = font.render(("魔法泉:一切良好,它能为你恢复魔法"),True,settings.magic_words_color)
			elif self.magic > 0:
				time = (self.max_magic-self.magic)//100
				s = font.render(("魔法泉:些许黯淡,需要"+str(time)+"个单位的时间来自我净化"),True,settings.magic_words_color)
			else:	
				s = font.render(("魔法泉:浑浊不堪,需要大量时间完成清洁"),True,settings.magic_words_color)
		
			turn_rect = s.get_rect()
			turn_rect.bottomleft = (0,settings.screen_height)
			screen.blit(s,turn_rect)		
			
	def clean_up(self,):
	
		if self.magic <= -1000:  #浑浊上限
			self.magic = -1000
	
		if self.magic <= 0:  #浑浊不堪
			self.magic += 1
		
		elif self.magic < self.max_magic:	#些许黯淡
			self.magic += 2
			
		
class Magic_ore(Object):
	def __init__(self,settings,screen,*args):	
		super().__init__(settings,screen,*args)		
	
		
		random_x,random_y = random.randint(-1500,1500),random.randint(-1500,1500)
		while abs(random_x)<1000 or abs(random_y)<1000:	
			random_x,random_y = random.randint(-1500,1500),random.randint(-1500,1500)		
		self.x,self.y = random_x,random_y
		self.max_magic = 800
		self.remainder_magic = self.max_magic
		self.width = 100
		self.height = 120
		self.show_status_distance = 250
		self.name = "魔法矿石"
	
			
	def give_magic(self,settings,screen,magician,calculate):
		#给予魔法值		
		
		if (abs(self.x - magician.x)<self.width) and (abs(self.y - magician.y)<self.height) :
		
			if self.remainder_magic>=0:
				
				if magician.magic < magician.max_magic:
					if random.randint(1,3)==1:
						magician.magic += random.uniform(5.0,10.0)	
						self.remainder_magic -= random.uniform(5.0,10.0)
						
		
	
	def draw_and_display(self,settings,screen,x_move,y_move,magician):
		#显示本物体于屏幕上

		pic = pygame.image.load('images/魔法矿石.bmp')
		a_rect = pic.get_rect()
		screen.blit( pic,(int(self.x + x_move - 0.5*a_rect.width),int(self.y + y_move - 0.5*a_rect.height)) )
	
	
	def show_status(self,settings,screen,calculate,magician):
		#显示文字描述
		
		if (abs(self.x - magician.x)<self.width) and (abs(self.y - magician.y)<self.height) :
			
			font = pygame.font.SysFont('SimHei',30)	
			rate = self.remainder_magic/self.max_magic
			if rate>0.7:
				s = font.render(("魔法矿石:魔法能量充足,它能为你快速补充魔法"),True,settings.magic_words_color)
			elif rate>0.4:
				s = font.render(("魔法矿石:魔法能量略有消耗,它能为你快速补充魔法"),True,settings.magic_words_color)
			elif rate>0:	
				s = font.render(("魔法矿石:魔法能量所剩无几,但它仍然能够为你补充魔法"),True,settings.magic_words_color)
			else :	
				s = font.render(("魔法矿石:魔法能量已经告罄,它已经不能补给魔法了"),True,settings.magic_words_color)
		
			turn_rect = s.get_rect()
			turn_rect.bottomleft = (0,settings.screen_height)
			screen.blit(s,turn_rect)	
	
	
	
		
class Magic():
	def __init__(self,settings,screen,magic_decrease,max_interference_allowed,sustainable_time,remaining_time,photos,name):
	
	
		self.magic_decrease = magic_decrease 
		
		self.max_interference_allowed = max_interference_allowed
		
		
		self.photos = 0
		self.remaining_time = 0
		

	def turn_on(self):	
		
		self.remaining_time += self.sustainable_time	
		self.photos = 25
		
		
	def turn_off(self):
	
		self.remaining_time = 0

	def interfere_turn_off(self,magician):
	
		
	#受到足够强度的干扰时，中断正在使用的技能	
		if magician.interference > self.max_interference_allowed:
			self.remaining_time = 0
			self.photos = 0
		
		
	def turn_on_display_font(self,screen,magician):
	#花哨字体展示
	
		if self.photos >=1:						
				
			if self.photos >10:
				pic =  pygame.image.load('images/'+str(self.name)+'10_副本.bmp')
			else:
				pic =  pygame.image.load('images/'+str(self.name)+str(int(self.photos))+'_副本.bmp')
		
			a_rect = pic.get_rect()
			screen.blit( pic,(int(magician.x + x_move - 0.5*a_rect.width),int(magician.y + y_move - a_rect.height - 100)) )			
			
			self.photos -= 0.5
	
	def if_can_execute(self,magician,settings):	
	#判定是否可以开启技能,是否可能被中断技能
		
		if (magician.magic >= self.magic_decrease) and (magician.interference < self.max_interference_allowed): #魔法足够+干扰比较小
			return True		
		else:
			self.remaining_time = 0
			self.photos = 0		
			return False

			
class Magic_ball(Magic):	
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
	
		self.name = '普通攻击'
		self.sustainable_time = 1
		self.magic_decrease = -10
		self.attack_distance = 100
		self.attack_damage = 41
		self.max_interference_allowed = 30
		self.start_speed = 10
		self.start_pos = 50
		self.cd_time = 5


	def turn_on(self,calculate,magician,settings):	
		if self.cd_time==0 and self.photos==0:
			self.cd_time = 50
			self.remaining_time += self.sustainable_time	
			self.photos = 25	
			self.new_magic(calculate,magician,settings)

				
	def new_magic(self,calculate,magician,settings)	:	


		#发动时妨碍其它操作
		if magician.interference<self.max_interference_allowed :
			magician.interference = self.max_interference_allowed -1

	
		center_x,center_y = settings.screen_width*0.5,settings.screen_height*0.5
		
		mouse_x,mouse_y=pygame.mouse.get_pos()
		
		[mouse_relative_direction_x,mouse_relative_direction_y] = calculate.another_direction_is(center_x,center_y,mouse_x,mouse_y)
		
		self.speed = [mouse_relative_direction_x * self.start_speed + magician.walk_speed[0],mouse_relative_direction_y * self.start_speed + magician.walk_speed[1]]
	
		self.x,self.y = self.start_pos * mouse_relative_direction_x + magician.x,self.start_pos * mouse_relative_direction_y + magician.y
	

	def move(self):

		#速度改变位置
		self.x += self.speed[0]
		self.y += self.speed[1]
		

	
		
	def try_to_execute(self,magician,settings,screen,calculate,ghost_list,x_move,y_move):	
		
		if self.cd_time>0:
			self.cd_time -= 1
		
		if self.photos:	
					
			self.move()
			
			
			if self.photos > 22:
				pic = pygame.image.load('images/能量球22_副本.bmp')
			
			
			else:
				pic = pygame.image.load('images/能量球'+str(int(self.photos))+'_副本.bmp')	
			
			a_rect = pic.get_rect()						
			screen.blit( pic,( int(self.x + x_move - 0.5*a_rect.width),int(self.y + y_move - 0.5*a_rect.height)) )		
			self.photos -= 1.25
			
			
			for i in range(len(ghost_list)):
				if calculate.distance_check(self.x,self.y,ghost_list[i].x,ghost_list[i].y,self.attack_distance ):					
							
					#造成伤害
					ghost_list[i].blood -= self.attack_damage
					ghost_list[i].walk_speed[0]+=0.3*self.speed[0]
					ghost_list[i].walk_speed[1]+=0.3*self.speed[1]
					ghost_list[i].mode_of_action['red_time']=100				
				
					self.photos = 0

					#爆炸图像
					pic = pygame.image.load('images/能量球爆炸.bmp')
					a_rect = pic.get_rect()	
					
					_x = (ghost_list[i].x+self.x)*0.5
					_y = (ghost_list[i].y+self.y)*0.5
					screen.blit( pic,( int(_x + x_move - 0.5*a_rect.width),int(_y + y_move - 0.5*a_rect.height)) )		
					
			
class Frog_curse(Magic):
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
		
		self.name = '青蛙诅咒'
		self.sustainable_time = 1
		self.magic_decrease = 1
		self.attack_distance = 125
		self.max_interference_allowed = 15		
		self.false_photos = 0
		self.odds = 0.5
		
		
	def try_to_execute(self,magician,settings,screen):	
					
		if self.remaining_time:	
			
			#鼠标处画青蛙图标
			mouse_x,mouse_y=pygame.mouse.get_pos()
			pic = pygame.image.load('images/青蛙图标.bmp')	
			
			a_rect = pic.get_rect()						
			screen.blit( pic,( int(mouse_x- 0.5*a_rect.width),int(mouse_y - 0.5*a_rect.height)) )				

			
	def curse(self,screen,calculate,ghost_list,magician):
		if self.remaining_time:	
		
			self.remaining_time = 0
			mouse_x,mouse_y=pygame.mouse.get_pos()
		
			for i in range(len(ghost_list)):
			
				if calculate.distance_check(mouse_x,mouse_y,ghost_list[i].x+x_move,ghost_list[i].y+y_move,self.attack_distance ):	
					
					if (self.odds>random.uniform(0,1.0)):
						ghost_list.pop(i)
						self.odds = self.odds**2
						self.photos = 25
					else:
						self.odds = self.odds**0.5
						self.false_photos = 25
						
					break #一次诅咒只能试图诅咒范围内的一个敌人
		



	def turn_on(self):	
		
		self.remaining_time += self.sustainable_time	
		
	def turn_on_display_font(self,screen,magician):
	#诅咒失败也有字体
	
		if self.false_photos >=1:						
				
			if self.false_photos >10:
				pic =  pygame.image.load('images/诅咒失败'+'10_副本.bmp')
			else:
				pic =  pygame.image.load('images/诅咒失败'+str(int(self.false_photos))+'_副本.bmp')
		
			a_rect = pic.get_rect()
			screen.blit( pic,(int(magician.x + x_move - 0.5*a_rect.width),int(magician.y + y_move - a_rect.height - 100)) )			
			
			self.false_photos -= 0.5	
	
		if self.photos >=1:						
				
			if self.photos >10:
				pic =  pygame.image.load('images/'+str(self.name)+'10_副本.bmp')
			else:
				pic =  pygame.image.load('images/'+str(self.name)+str(int(self.photos))+'_副本.bmp')
		
			a_rect = pic.get_rect()
			screen.blit( pic,(int(magician.x + x_move - 0.5*a_rect.width),int(magician.y + y_move - a_rect.height - 100)) )			
			
			self.photos -= 0.5	
		

class Magic_barrier(Magic):
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
		
		self.name = '魔法屏障'
		self.sustainable_time = 1
		self.blood_add = 1
		self.magic_decrease = 0.1

		self.max_interference_allowed = 75		
		self.special_effects = 0.25
		
		self.record_blood = 0
		
	def try_to_execute(self,magician,settings):	
					
		if self.remaining_time:
			if (magician.blood >= magician.max_blood):
				self.remaining_time = 0  #满血少蓝自动停止
					
			else:
				magician.blood += self.blood_add
				magician.magic -= self.magic_decrease
					

	def turn_on_and_off(self):	
		
		if self.remaining_time:
			self.remaining_time =0
			self.photos = 0
			self.show_photos = 0
		else:
			self.remaining_time += self.sustainable_time	
			self.photos = 25
			self.show_photos = 15

		
	def show_special_effects(self,settings,screen):
	
		if self.show_photos == 0:
			pass
		
		if self.show_photos>1 or self.photos<20:
			if self.show_photos > 8:
				pic =  pygame.image.load('images/魔法护罩8_副本.bmp')	
			else:
				pic =  pygame.image.load('images/魔法护罩'+str(int(self.show_photos))+'_副本.bmp')	
				
			
			a_rect = pic.get_rect()
							
			screen.blit( pic,(int(0.5*settings.screen_width - 0.5*a_rect.width),int(0.5*settings.screen_height - 0.5*a_rect.height)) )		
			
			if self.show_photos>1:		
				self.show_photos -= self.special_effects	

		if self.show_photos==1 or self.show_photos==20:
			self.special_effects *= -1	
			self.show_photos -= self.special_effects
	
	
	def try_to_execute(self,magician,settings,screen):
	
		if self.remaining_time:	
	

			magician.magic -= self.magic_decrease	
			
			#特效
			self.show_special_effects(settings,screen)			
			
			#减少干扰强度
			magician.interference *= 0.75		
			
			#减少血量损失(本质上是弥补损失)
			difference = self.record_blood - magician.blood
			if difference >0 : #受到了伤害
				magician.blood += 0.25*difference
			
			self.record_blood = magician.blood
			
		
class Magic_drive(Magic):			
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
		
		self.name = '魔法驱动'
		self.sustainable_time = 3			
		self.speed_addition = 3
		self.magic_decrease = 0.1
		self.max_interference_allowed = 80
		
	def try_to_execute(self,magician,settings):
		
		if self.remaining_time:


			#发动时妨碍其它操作
			if magician.interference<10 :
				magician.interference = 10
				
			self.remaining_time -= 1		
			magician.magic -= 6
			
			if magician.mouse_relative_direction_x>0:
				magician.walk_speed[0] +=(magician.mouse_relative_direction_x**2)*self.speed_addition
				
			else:
				magician.walk_speed[0] -= (magician.mouse_relative_direction_x**2)*self.speed_addition
			

			if magician.mouse_relative_direction_y >0:	
				magician.walk_speed[1] += (magician.mouse_relative_direction_y**2)*self.speed_addition
			else:			
				magician.walk_speed[1] -= (magician.mouse_relative_direction_y**2)*self.speed_addition

	

class Cure(Magic):			
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
		
		self.name = '快速治疗'
		self.sustainable_time = 1
		self.blood_add = 1.45
		self.magic_decrease = 1.25

		self.max_interference_allowed = 75		
		
		
	def try_to_execute(self,magician,settings):	
					
		if self.remaining_time:


			#发动时妨碍其它操作
			if magician.interference<self.max_interference_allowed :
				magician.interference = self.max_interference_allowed -1

			self.photos = 25
			if (magician.blood >= magician.max_blood):
				self.remaining_time = 0  #满血少蓝自动停止
					
			else:
				magician.blood += self.blood_add
				magician.magic -= self.magic_decrease
			

class Telekinesis(Magic):			
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
		
		self.name = '念动力'
		self.sustainable_time = 1
		self.magic_decrease = 1.75
		self.attack_distance = 200
		self.attack_damage = 1.75
		self.give_speed = 1
		self.max_interference_allowed = 55	
		self.show_photos = 0
	
	def show_special_effects(self,settings,screen):
		if self.show_photos>=1:
		
			if self.show_photos > 6:
				pic =  pygame.image.load('images/念动力特效6_副本.bmp')	
			else:
				pic =  pygame.image.load('images/念动力特效'+str(int(self.show_photos))+'_副本.bmp')	
				
			
			a_rect = pic.get_rect()
							
			screen.blit( pic,(int(0.5*settings.screen_width - 0.5*a_rect.width),int(0.5*settings.screen_height - 0.5*a_rect.height)) )		
			
			if self.show_photos>1:		
				self.show_photos -= 1

	def turn_on(self):	
		
		self.remaining_time += self.sustainable_time	
		self.photos = 25
		self.show_photos = 10

		
	def turn_off(self):
	
		self.show_photos = 0	
		self.remaining_time = 0		
			
		
	def try_to_execute(self,magician,settings,screen,calculate,ghost_list):	
					
		if self.remaining_time:

			#发动时妨碍其它操作
			if magician.interference<30 :
				magician.interference = 30
				
			self.photos = 25
			self.show_special_effects(settings,screen)

			magician.magic -= self.magic_decrease			
			
			for i in range(len(ghost_list)):
				if calculate.distance_check(magician.x,magician.y,ghost_list[i].x,ghost_list[i].y,self.attack_distance ):
					
					[relative_x,relative_y] = calculate.another_direction_is(magician.x,magician.y,ghost_list[i].x,ghost_list[i].y)
						
						
					#推远目标
					if relative_x >0:
						ghost_list[i].walk_speed[0]+=self.give_speed*relative_x**2
					else:	
						ghost_list[i].walk_speed[0]-=self.give_speed*relative_x**2
							
							
					if 	relative_y >0:
						ghost_list[i].walk_speed[1]+=self.give_speed*relative_y**2
					else:
						ghost_list[i].walk_speed[1]-=self.give_speed*relative_y**2
							
						
					#造成伤害
					ghost_list[i].blood -= self.attack_damage
					ghost_list[i].mode_of_action['red_time']=100
					
					

class  Earthquake(Magic):
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)

		self.name = '大地震'
		self.sustainable_time = 1
		self.magic_decrease = 0.1
		self.attack_distance = 800
		self.attack_damage = 4.6
		self.max_interference_allowed = 90 #发动时的
		

		
	def try_to_execute(self,magician,settings,screen,calculate,ghost_list):	
		global x_move,y_move
		if self.remaining_time:			

			#发动时妨碍其它操作
			if magician.interference<self.max_interference_allowed :
				magician.interference = self.max_interference_allowed -1
				
			self.photos=1  #使用地震时字体持续显示
			magician.magic -= 4.5
			
			for i in range(len(ghost_list)):
				if calculate.distance_check(magician.x,magician.y,ghost_list[i].x,ghost_list[i].y,self.attack_distance ):					
						
					#造成伤害
					ghost_list[i].blood -= self.attack_damage
					ghost_list[i].walk_speed[0]*=0.8
					ghost_list[i].walk_speed[1]*=0.8
					ghost_list[i].mode_of_action['red_time']=1
					
			if random.randint(0,1):
				x_move+=1
			else:
				x_move-=1
				
			if random.randint(0,1):
				y_move-=1
			else:				
				y_move+=1
				
				
	def turn_on(self):	
			
		self.photos = 25			


	def turn_off(self):
	
		self.remaining_time = 0
		self.photos = 0	
		
	def turn_on_display_font(self,screen,magician):
	#花哨字体展示
	
		if magician.interference>5: #吟唱时的最大干扰强度为5
			self.photos = 0
			
		if self.photos >=1:						
				
			if self.photos >10:
				pic =  pygame.image.load('images/'+str(self.name)+'10_副本.bmp')
			else:
				pic =  pygame.image.load('images/'+str(self.name)+str(int(self.photos))+'_副本.bmp')
		
			a_rect = pic.get_rect()
			screen.blit( pic,(int(magician.x + x_move - 0.5*a_rect.width),int(magician.y + y_move - a_rect.height - 100)) )			
			
			self.photos -= 0.25		
			
		if self.photos==1:
			self.remaining_time = 1 #字体展示结束，效果正式发动




class Revive(Magic):			
	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
		
		self.name = '大复活术'
		self.sustainable_time = 1
		self.remaining_time = 1
		self.blood_add = 1
		self.magic_decrease = 100
		self.max_magic_decrease = 300

		self.max_interference_allowed = 101		
		
	def try_to_execute(self,magician,settings):	
					
		if self.remaining_time: #被动技能，被激发之后remaining_time就一直为1
		
			if (magician.blood < 0) and (magician.magic > self.magic_decrease):
			
				self.photos = 40
				
				magician.blood = magician.max_blood
				magician.magic -= self.magic_decrease
				magician.max_magic -= self.max_magic_decrease

			
			
class Ghost(Object):			

	def __init__(self,settings,screen,x,y,power,friction,walk_speed,interference,blood,status,name,max_blood,attack_distance,attack_damage,detect_distance,want,want_default) :
	
	
		super().__init__(settings,screen,x,y,power,friction,walk_speed,interference,blood,status,name,)
		
		self.status = "normal"
		self.mode_of_action = {'red_time':0,'attack_cd':0}
		self.attack_damage = 25
		self.walk_speed = [0,0]
		self.want_default = 2.5
		self.want = [200,200,self.want_default]  #前两个元素是方向矢量，第三个是程度
		#程度:1差不多是直行,3~5大约是曲线直行
		
		random_x,random_y = random.randint(-1500,1500),random.randint(-1500,1500)
		while abs(random_x)<1000 or abs(random_y)<1000:	
			random_x,random_y = random.randint(-1500,1500),random.randint(-1500,1500)		
		self.x,self.y = random_x,random_y
	
	def stain_fountain(self,calculate,fountain,settings,screen):
		#玷污魔法泉
		
		if (abs(fountain.x - self.x)<fountain.width) and (abs(fountain.y - self.y)<fountain.height) :
			fountain.magic -= random.randint(2,4)
			self.stain_remind(settings,screen)
		
	def stain_remind(self,settings,screen):
	
		font = pygame.font.SysFont('SimHei',30)	
		s = font.render(("【魔法泉正在遭受玷污】"),True,settings.magic_words_color)
		
		turn_rect = s.get_rect()
		turn_rect.bottomleft = (0,settings.screen_height - 30)
		screen.blit(s,turn_rect)		
					
		
		
	
	def detect(self,magician,calculate):
		if calculate.distance_check(self.x,self.y,magician.x,magician.y,self.detect_distance):			

			self.mode_of_action['red_time']=100					
		
		

	def try_to_attack(self,calculate,magician,screen):
	

		if self.mode_of_action['attack_cd']:
			self.mode_of_action['attack_cd']-=1
		else:
			if calculate.distance_check(self.x,self.y,magician.x,magician.y,self.attack_distance):
				self.attack(magician,screen)
		
		
	def attack(self,magician,screen):
		
		#攻击会影响追击
		self.walk_speed[0]*=0.8
		self.walk_speed[1]*=0.8
		
		
		#冷却
		self.mode_of_action['attack_cd'] = 30
		
		magician.lose_blood(self.attack_damage,random.randint(50,75),screen)
		
		
		
		
		
	def change_status(self):
		if self.mode_of_action['red_time']<=0:
			self.status = "normal"
		elif self.mode_of_action['red_time']>0:
			self.status = "red"
			self.mode_of_action['red_time'] -= 1
		
	def draw_blood(self,screen,settings):
		if self.blood>0:
			if self.status == "normal":
				color = settings.blood_rect_color
			elif self.status == "red":
				color = settings.blood_rect_color_red
			blood_rect_long = int(0.5*self.max_blood)
			_list = [ 0,0,blood_rect_long,15 ]
			_rect = pygame.Rect(_list)
			_rect.midbottom = self.x+x_move,self.y-80+y_move		
			pygame.draw.rect( screen,color,_rect,2 )		
			
			blood_rect_long2 = int(0.5*self.blood)
			_list2 = [ 0,0,blood_rect_long2,15 ]
			_rect2 = pygame.Rect(_list2)
			_rect2.midleft = _rect.midleft 
			pygame.draw.rect( screen,color,_rect2,0 )	

			
	def act(self,magician,calculate,screen,fountain):	
		
		self.detect(magician,calculate)
		if self.mode_of_action['red_time']>0: #追主角
			self.want[2] = 1
			self.wander_walk(calculate,magician)
		else:
			self.want[2] = self.want_default
			self.wander_walk(calculate,fountain)
	
		
	def f_execute(self,calculate):	
		
		[speed_relative_direction_x,speed_relative_direction_y] = calculate.another_direction_is(0,0,self.walk_speed[0],self.walk_speed[1])
		
		if speed_relative_direction_x>0:
			self.walk_speed[0] += self.friction * (speed_relative_direction_x**2)
		else:	
			self.walk_speed[0] -= self.friction * (speed_relative_direction_x**2)
					
		if speed_relative_direction_y>0:	
			self.walk_speed[1] += self.friction * (speed_relative_direction_y**2)
		else: 
			self.walk_speed[1] -= self.friction * (speed_relative_direction_y**2)		
	
		
		
		
	

	def wander_walk(self,calculate,target):
	
		[self.want[0],self.want[1]] = calculate.another_direction_is(self.x,self.y,target.x,target.y)	
		
		[random_x,random_y] = self.random_a_vector()
		
		self.move(calculate,random_x,random_y)

		
		
	def move(self,calculate,random_x,random_y):
		#print(random_x,random_y)

	
		self.x += self.walk_speed[0]
		self.y += self.walk_speed[1]
		
		
		all_walk_speed = (self.walk_speed[0]**2 + self.walk_speed[1]**2)**0.5
		
		if all_walk_speed>0:
			accelerated_speed = self.power/all_walk_speed
			if accelerated_speed>4:
				accelerated_speed=4	
		else:
			accelerated_speed = 0.001
				
		if random_x>0:
			self.walk_speed[0] += accelerated_speed * (random_x**2)
		else:	
			self.walk_speed[0] -= accelerated_speed * (random_x**2)
					
		if random_y>0:	
			self.walk_speed[1] += accelerated_speed * (random_y**2)
		else: 
			self.walk_speed[1] -= accelerated_speed * (random_y**2)
			
		self.f_execute(calculate)	
					
		
	def random_a_vector(self):
	#抽一个随机矢量
		
		#正态分布的第一个参数，对应倾向的方向；第二个对应倾向的猛烈度（一般第一个参数足够调整倾向）
		x = random.normalvariate(self.want[0],self.want[2]) 
		while (x<-1 or x>1):
			x = random.normalvariate(self.want[0],self.want[2]) 
			#重复，直到取一个-1到1之内的值
			

		random_number = random.normalvariate(self.want[1],self.want[2])
		while (random_number<-1 or random_number>1):
			random_number = random.normalvariate(self.want[1],self.want[2])
		
		if random_number>0:
			y = (1 - x**2)**0.5
		else:
			y = -(1 - x**2)**0.5
			

		return [x,y]		
		

		
		
class Shield(Ghost):	

	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
				
		
		self.name = "盾"
		self.attack_distance = 90
		self.detect_distance = 160
		self.power = 2
		self.friction = -0.2
		self.max_blood = 250
		self.blood = self.max_blood 

		
class Speed(Ghost):	

	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
				
		
		self.name = "速"
		self.attack_distance = 75
		self.detect_distance = 250
		self.power = 3
		self.friction = -0.15
		self.max_blood = 120
		self.blood = self.max_blood 

	


class Curse(Ghost):	

	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
				
		
		
		self.name = "咒"
		self.attack_distance = 200
		self.attack_damage = 5
		self.detect_distance = 300
		self.power = 1.7
		self.friction = -0.15
		self.max_blood = 130
		self.blood = self.max_blood 
		self.photos = 0
		

	def attack(self,magician,screen):
	
		magician.lose_blood(self.attack_damage,random.randint(50,95),screen)
		
		#攻击附带降速
		magician.walk_speed[0] *= 0.6
		magician.walk_speed[1] *= 0.6
		
		self.mode_of_action['attack_cd'] = 120
		
		self.photos=10
		
	def act(self,magician,calculate,screen,fountain):	
		
		self.detect(magician,calculate)
		if self.mode_of_action['red_time']:
			self.want[2] = 1.5
			self.wander_walk(calculate,magician)
		else:
			self.want[2] = self.want_default
			self.wander_walk(calculate,fountain)

		if self.photos>0:
			self.show_special_effects(screen,magician)
		
		
	def show_special_effects(self,screen,magician):
		if 	self.photos>6:
			pic =  pygame.image.load('images/咒6_副本.bmp')
		else:
			pic =  pygame.image.load('images/咒'+str(self.photos)+'_副本.bmp')	
		self.photos -= 1
		
		a_rect = pic.get_rect()						
		screen.blit( pic,(int(magician.x + x_move - 0.5*a_rect.width),int(magician.y + y_move - a_rect.height)) )				
		
		


		
class Hide(Ghost):	

	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
				
		
		self.name = "隐"
		self.attack_distance = 75
		self.detect_distance = 400
		self.power = 2
		self.friction = -0.15
		self.max_blood = 140
		self.blood = self.max_blood 
		
		self.hiding_photos = 10
		self.want[2] = self.want_default
		
		
	
	def detect(self,magician,calculate):
		if calculate.distance_check(self.x,self.y,magician.x,magician.y,self.detect_distance):		
			self.want[2] = 2	
		else:
			self.want[2] = self.want_default
		

	def try_to_attack(self,calculate,magician,screen):
	

		if self.mode_of_action['attack_cd']:
			self.mode_of_action['attack_cd']-=1
		else:
			if calculate.distance_check(self.x,self.y,magician.x,magician.y,self.attack_distance):
				self.attack(magician,screen)
				self.mode_of_action['red_time']=50	

				
	def draw_blood(self,screen,settings):
		if self.blood>0:
			if self.status == "red":
				color = settings.blood_rect_color_red
				blood_rect_long = int(0.5*self.max_blood)
				_list = [ 0,0,blood_rect_long,15 ]
				_rect = pygame.Rect(_list)
				_rect.midbottom = self.x+x_move,self.y-80+y_move		
				pygame.draw.rect( screen,color,_rect,2 )		
				
				blood_rect_long2 = int(0.5*self.blood)
				_list2 = [ 0,0,blood_rect_long2,15 ]
				_rect2 = pygame.Rect(_list2)
				_rect2.midleft = _rect.midleft 
				pygame.draw.rect( screen,color,_rect2,0 )		

			
	def act(self,magician,calculate,screen,fountain):	
		
		self.detect(magician,calculate)
		if self.mode_of_action['red_time']>0:
			self.want[2] = 1
			self.hiding_photos = 20
			self.wander_walk(calculate,magician)
		else:
			self.wander_walk(calculate,fountain)
					
		
	
	def draw_and_display(self,settings,screen,x_move,y_move,magician):
		#显示本物体于屏幕上
		
		if self.status == "red":	
			pic =  pygame.image.load('images/幽灵_隐(红)_副本.bmp')	
			#self.hiding_photos = 20
			
		else :
			if self.hiding_photos > 9:
				pic =  pygame.image.load('images/幽灵_隐9_副本.bmp')	
			else:
				pic =  pygame.image.load('images/幽灵_隐'+str(int(self.hiding_photos))+'_副本.bmp')				
				
			if self.hiding_photos > 1:
				self.hiding_photos -= 0.5
				
		a_rect = pic.get_rect()
					
		screen.blit( pic,(int(self.x + x_move - 0.5*a_rect.width),int(self.y + y_move - 0.5*a_rect.height)) )			


class Fox(Ghost):

	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
				
		
		self.name = "狡"
		self.attack_distance = 90
		self.detect_distance = 300
		self.attack_damage = 25
		self.power = 2.5
		self.friction = -0.18
		self.max_blood = 165
		self.blood = self.max_blood 


	
	def detect(self,magician,calculate):
	
		if calculate.distance_check(self.x,self.y,magician.x,magician.y,self.detect_distance):				
		
			if self.mode_of_action['red_time']<=0:
				self.mode_of_action['red_time'] = 100


	def act(self,magician,calculate,screen,fountain):	
		
		self.detect(magician,calculate)
		if self.mode_of_action['red_time']>0:
			self.want[2] = 1
			self.wander_walk(calculate,magician)
		else:
			self.want[2] = self.want_default
			self.wander_walk(calculate,fountain)		

		
	def wander_walk(self,calculate,magician):
	
		[self.want[0],self.want[1]] = calculate.another_direction_is(self.x,self.y,magician.x,magician.y)	
		
		[random_x,random_y] = self.random_a_vector()
		
		if self.status == "red":	
			self.escape(calculate,-random_x,-random_y)
		else:
			self.move(calculate,random_x,random_y)	
	

	def escape(self,calculate,x,y):
		for i in range(3):
			self.move(calculate,x,y)
			if self.mode_of_action['red_time']>0:
				self.mode_of_action['red_time']-=2
	
	
			
class Anger(Ghost):

	def __init__(self,settings,screen,*args):
	
		super().__init__(settings,screen,*args)
				
		
		
		self.name = "怒"
		self.attack_distance = 60
		self.detect_distance = 150
		self.attack_damage = 15
		self.power = 2
		self.friction = -0.15
		self.max_blood = 150
		self.blood = self.max_blood 
	
	def detect(self,magician,calculate):
		pass #没有察觉能力	
			

	def act(self,magician,calculate,screen,fountain):	
		
		self.detect(magician,calculate)
		if self.mode_of_action['red_time']>0:
			self.want[2] = 0.75
			
			#暴怒状态
			for i in range(2):
				self.wander_walk(calculate,magician)
			self.attack_damage = 25
			self.attack_distance = 90			
			
		else:
			self.want[2] = self.want_default
			self.attack_damage = 15
			self.attack_distance = 60	
			self.wander_walk(calculate,fountain)
		

	def attack(self,magician,screen):		
		
		if self.mode_of_action['red_time']>0:	#暴怒状态		
	
			magician.lose_blood(self.attack_damage,random.randint(50,95),screen)
			
			#冷却
			self.mode_of_action['attack_cd'] = 20
			
			
		else:
			#攻击会影响追击
			self.walk_speed[0]*=0.8
			self.walk_speed[1]*=0.8			
	
			magician.lose_blood(self.attack_damage,random.randint(50,75),screen)
			self.mode_of_action['attack_cd'] = 30		
		

		
class Control():	

	def __init__(self):
		self.max_number_ghost = 20
	
	def new_ghosts(self,settings,screen,enviorment):
	
		global ghost_list
		if enviorment.difficulty_level==4:
			number = 6
		else:
			number = 8
			
		shield = Shield(settings,screen,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)		
		shield.x,shield.y = (-500,-500)
		ghost_list.append(shield)	
			
				
			
		
	def try_to_add_ghost(self,settings,screen,enviorment,game_time):
		
		global ghost_list				
		
		if len(ghost_list)<self.max_number_ghost:
			
			add_cd_time = 500/enviorment.difficulty_level
			
				
			#进行一次幽灵刷新
			if game_time%add_cd_time == 1:
			
				#时间长短决定刷新种类
				if game_time<700:
					ghost_variety = 1
					
				elif game_time<1400:
					ghost_variety = 2
					
				else :	
					ghost_variety = 3			
					
				
				
				#幽灵刷新比例：
				#盾:速:咒:隐:狡:怒 = 4:5:2:3:3:2
				if ghost_variety ==1:				
					random_number = random.randint(1,12)
					
				elif ghost_variety ==2:
					random_number = random.randint(1,17)
					
				elif ghost_variety ==3:
					random_number = random.randint(1,19)
					
					
				if random_number<=4:
					self.add_ghost(settings,screen,'shield')
				elif random_number<=9:	
					self.add_ghost(settings,screen,'speed')
				elif random_number<=11:	
					self.add_ghost(settings,screen,'curse')
				elif random_number<=14:	
					self.add_ghost(settings,screen,'hide')
				elif random_number<=17:	
					self.add_ghost(settings,screen,'fox')
				elif random_number<=19:	
					self.add_ghost(settings,screen,'anger')
					
				
			
	def add_ghost(self,settings,screen,want):
		global ghost_list
		
		print(len(ghost_list))
		if want == "shield":
			shield = Shield(settings,screen,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)		
			
			ghost_list.append(shield)	
			

		if want == "speed":			
			speed = Speed(settings,screen,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			ghost_list.append(speed)


		if want == "curse":
			curse = Curse(settings,screen,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			ghost_list.append(curse)			
			

		if want == "hide":			
			hide = Hide(settings,screen,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			ghost_list.append(hide)
			

		if want == "fox":			
			fox = Fox(settings,screen,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			ghost_list.append(fox)


		if want == "anger":			
			anger = Anger(settings,screen,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
			ghost_list.append(anger)
		
						
		
		
	
main()	
	



