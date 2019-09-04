
import pygame,sys,time,random,math




def main():
	
	# 初始化pygame
	pygame.init()
	
	settings = Settings()
	image = Image()
	game = Game()
	player = Player()
	black_replenish = Black_replenish()
	
	shoots_list = []
	black_list = []
	
	# 创建pygame显示层
	screen = pygame.display.set_mode( (settings.screen_width,settings.screen_height) )
	pygame.display.set_caption('COLOR')

	left_move,right_move,up_move,down_move = False,False,False,False

	while True:
	
		game.game_time += 1
		if game.game_status=="gaming":
			game.gaming_time += 1		
		
		screen.fill([255,255,255])	
		clock = pygame.time.Clock()
		time_passed = clock.tick(settings.fps_number)
		
		game.mouse_x,game.mouse_y=pygame.mouse.get_pos()
		game.count_direction(settings)
		
		

			
		
		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				sys.exit()		
				
			elif event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_a:
					left_move = True
				elif event.key == pygame.K_d:
					right_move = True
				if event.key == pygame.K_w:
					up_move = True
				elif event.key == pygame.K_s:
					down_move = True
				elif event.key == pygame.K_e:
					player.change_shoots_type('r')
				elif event.key == pygame.K_q:
					player.change_shoots_type('l')
				
			elif event.type == pygame.KEYUP:	
				if event.key == pygame.K_a:
					left_move = False
				elif event.key == pygame.K_d:
					right_move = False
				if event.key == pygame.K_w:
					up_move = False
				elif event.key == pygame.K_s:
					down_move = False
					
				
				
			elif event.type == pygame.MOUSEBUTTONUP:
				game.mousebuttondown = False
				
				#游戏中途
				if game.game_status=='gaming':
				
					#停止射击
					player.shooting = False
				
				
			elif event.type == pygame.MOUSEBUTTONDOWN:
				game.mousebuttondown = True
				
				#开始界面
				if game.game_status=='start':
					
					if if_collidepoint(image.turn_rect_list[0],game.mouse_x,game.mouse_y):
						game.game_status = "gaming"
					
					elif if_collidepoint(image.turn_rect_list[8],game.mouse_x,game.mouse_y):
						game.game_status = 'show_rules'
					
					elif if_collidepoint(image.turn_rect_list[9],game.mouse_x,game.mouse_y):
						game.change_difficulty()
						
				
					elif if_collidepoint(image.turn_rect_list[1],game.mouse_x,game.mouse_y):
						sys.exit()
				
				elif game.game_status=='show_rules':
					game.game_status = "start"
				
				
				#游戏中途
				elif game.game_status=='gaming':
					
					#返回键
					if if_collidepoint(image.turn_rect_list[2],game.mouse_x,game.mouse_y):
						
						game.game_status='suspend'
					
					#射击
					else:
						player.shooting = True
						
						
					
				#暂停状态	
				elif game.game_status=='suspend':
					
					if if_collidepoint(image.turn_rect_list[3],game.mouse_x,game.mouse_y):
						game.game_status = "gaming"
					
					elif if_collidepoint(image.turn_rect_list[4],game.mouse_x,game.mouse_y):
						main()	
				
					elif if_collidepoint(image.turn_rect_list[5],game.mouse_x,game.mouse_y):
						sys.exit()	
				
				
				#死亡时
				elif game.game_status=='game_over' and game.game_over_picture_end:
					
					if if_collidepoint(image.turn_rect_list[6],game.mouse_x,game.mouse_y):
						main()
					
					elif if_collidepoint(image.turn_rect_list[7],game.mouse_x,game.mouse_y):
						sys.exit()	
						
				
				
		#绘画
		image.show_backpic(settings,screen,game.game_time)		
		image.show_white(settings,screen,game.gaming_time)
		
		if game.game_status=='gaming':					
			player.move(left_move,right_move,up_move,down_move,shoots_list,black_list)			
			player.shoot_cd_decrease()		
			black_replenish.replenish_black(black_list,game)			


		if game.game_status=='start':
	
			image.show_font(screen,"开始游戏",[settings.screen_width*0.06,settings.screen_height*0.4],game.mouse_x,game.mouse_y,game)

			image.show_font(screen,game.game_difficulty,[settings.screen_width*0.06,settings.screen_height*0.5],game.mouse_x,game.mouse_y,game)

			image.show_font(screen,"游戏规则",[settings.screen_width*0.06,settings.screen_height*0.6],game.mouse_x,game.mouse_y,game)
			
			image.show_font(screen,"退出游戏",[settings.screen_width*0.06,settings.screen_height*0.7],game.mouse_x,game.mouse_y,game)
			
			image.show_title_pic(screen)
			
		
		elif game.game_status=='show_rules':
			image.show_rules_pic(screen)
		
		
		elif game.game_status=='gaming' or game.game_status=='game_over':
				
			for i in reversed(shoots_list):	
				if i.impact_check(game,black_list,black_replenish):
					if i.type!='purple' and i.type!='blue':
						shoots_list.remove(i)
			
			eliminate_black_and_shoot(black_list,shoots_list,settings)
			
			for i in shoots_list:
				i.show_itself(settings,screen)
				i.fly()
			
			for i in black_list:
				if i.name=='black_rush':
					i.show_nucleon(screen)
				elif i.name=='black_geyser':
					i.cumulate_time()
					i.replenish_radius()
				elif i.name=='black_excite':
					i.check_excite(settings,shoots_list)
					i.show_nucleon(screen)
					i.exciting_move(settings)
				elif i.name=='black_split':
					i.show_nucleon(screen)
					i.cumulate(black_list)
					
				i.move()	
				i.check_kill_player(settings,game)
				i.show_itself(settings,screen)
				i.change_direction(settings)
				
			game.show_get_score_pic(screen)
			player.show_myself(settings,screen,game)
			if game.game_status=='gaming':
				player.show_afterimage(settings,screen,left_move,right_move,up_move,down_move)
				player.show_color_turntable(screen)
				if player.shooting:
					player.shoot(settings,game.mouse_direction,shoots_list)
					
			image.show_menu_logo(settings,screen)
			if if_collidepoint(image.turn_rect_list[2],game.mouse_x,game.mouse_y):
				image.menu_logo_pointed = True
			else:
				image.menu_logo_pointed = False
			
			game.show_how_many_score(screen)
			
			
		if game.game_status=='game_over':			
			game.death_picture(game,player)
		
		if game.game_status=='game_over' and game.game_over_picture_end:
			
			image.show_little_white(screen)
		
			image.show_font(screen,"返回主菜单",[settings.screen_width*0.38,settings.screen_height*0.48],game.mouse_x,game.mouse_y,game)
		
			image.show_font(screen,"结束游戏",[settings.screen_width*0.38,settings.screen_height*0.57],game.mouse_x,game.mouse_y,game)
		

		
				
		if game.game_status=='suspend':
			image.show_suspend_gray(settings,screen)
		
			image.show_font(screen,"继续游戏",[settings.screen_width*0.06,settings.screen_height*0.2],game.mouse_x,game.mouse_y,game)
		
			image.show_font(screen,"退回主菜单",[settings.screen_width*0.06,settings.screen_height*0.35],game.mouse_x,game.mouse_y,game)
		
			image.show_font(screen,"直接退出",[settings.screen_width*0.06,settings.screen_height*0.5],game.mouse_x,game.mouse_y,game)
		
		
		
		
		
		#特殊光标
		game.show_mouse_point(screen)	
		pygame.mouse.set_visible(False) #
		
		# 刷新pygame显示层
		pygame.display.flip()	





class Game():

	def __init__(self):
		
		self.game_time = 1
		self.game_status = 'start'
		self.game_difficulty = '游戏难度:简单'
		self.gaming_time = 1
		self.game_over_picture_end = False
		self.mouse_direction = [0,0]
		self.mousebuttondown = False
		self.score = 0
		self.score_show_list = []
		
	
	def change_difficulty(self):
		list = ['游戏难度:简单','游戏难度:普通','游戏难度:困难']
		if self.game_difficulty==list[0]:
			self.game_difficulty = list[1]
		elif self.game_difficulty==list[1]:
			self.game_difficulty = list[2]
		elif self.game_difficulty==list[2]:
			self.game_difficulty = list[0]
		

	def count_direction(self,settings):
		
		relative_pos = [self.mouse_x-settings.screen_width*0.5,self.mouse_y-settings.screen_height*0.5]	
		
		if relative_pos==[0,0]:
			relative_pos=[0,1]
		self.mouse_direction = vector_unitize(relative_pos)
		
		
	def show_mouse_point(self,screen):
		
		if self.mousebuttondown:
			pic =  pygame.image.load('images/小图标/26.bmp')
		else:
			pic =  pygame.image.load('images/小图标/25.bmp')
		rect = pic.get_rect()
		rect.center = [self.mouse_x,self.mouse_y]
		screen.blit( pic,rect )
		
		
	
	def get_score(self,black):
		if black.name=='black_rush':
			self.score+=2	
			pic = '+2'
		else:
			self.score+=1	
			pic = '+1'
				
		self.score_show_list.append([pic,black.pos,30])	
	
	
	def show_how_many_score(self,screen):
		
		font = pygame.font.SysFont('SimHei',45)	
		s = font.render(str(self.score),True,[120,120,150])
		turn_rect = s.get_rect()		
		turn_rect.topright = [890,10]
		
		#绘制
		screen.blit(s,turn_rect)
		
		
	def death_picture(self,game,player):	
		if not self.game_over_picture_end:
			
			list = [40,40,40]		
			for i in range(3):
				if player.color[i]>=40:
					player.color[i]-=4
			if player.color[0]<=list[0] and player.color[1]<=list[1] and player.color[2]<=list[2]:
				self.game_over_picture_end = True
		
		

	def show_get_score_pic(self,screen,):
		#得分画面
		
		for i in reversed(self.score_show_list):
			if i[2]<=0:
				self.score_show_list.remove(i)
			else:
				i[2]-=1	
				if i[0]=='+1':
					if i[2]>=8:
						pic =  pygame.image.load('images/小图标/3.bmp')
					else:
						pic =  pygame.image.load('images/小图标/'+str(3+(7-i[2]))+'.bmp')
				elif i[0]=='+2':
					if i[2]>=8:
						pic =  pygame.image.load('images/小图标/11.bmp')
					else:
						pic =  pygame.image.load('images/小图标/'+str(11+(7-i[2]))+'.bmp')
						
				_rect = pic.get_rect()
					
				screen.blit(pic,[i[1][0]-0.5*_rect.width,i[1][1]-0.5*_rect.height])
			

def eliminate_black_and_shoot(black_list,shoots_list,settings):
	
	for i in reversed(black_list):
		
		if (abs(settings.screen_width*0.5-i.pos[0])>settings.screen_width) or (abs(settings.screen_height*0.5-i.pos[1])>2*settings.screen_height):
	
			black_list.remove(i)
			
			
	for i in reversed(shoots_list):
		
		if (abs(settings.screen_width*0.5-i.pos[0])>0.6*settings.screen_width) or (abs(settings.screen_height*0.5-i.pos[1])>0.6*settings.screen_height):
	
			shoots_list.remove(i)


class Black_replenish():
	
	
	def __init__(self):
		self.cd_replenish = {'black_normal':0,'black_rush':500,'black_geyser':0,'black_excite':0,'black_split':500}
		
		self.max_number = {'black_normal':4,'black_rush':1,'black_geyser':15,'black_excite':2,'black_split':1}


	def replenish_black(self,black_list,game):
		
		to_do_list = [False,False,False,False,False]
		list = ['black_normal','black_rush','black_geyser','black_excite','black_split']
		for i in list:
			if self.cd_replenish[i]<=0:
				sum=0
				for x in black_list:	
					if x.name==i:
						sum+=1		
				
				if sum<self.max_number[i]:	
					to_do_list[list.index(i)] = True
					
			
		
		for x,y in self.cd_replenish.items():
			if y>0:
				self.cd_replenish[x]-=1
		
		
		#难度['游戏难度:简单','游戏难度:普通','游戏难度:困难']
		if game.game_difficulty=='游戏难度:简单':
			rate = 1
		elif game.game_difficulty=='游戏难度:普通':
			rate = 1.1
		elif game.game_difficulty=='游戏难度:困难':	
			rate = 1.2
					
		if to_do_list[0]:					
			black = Black_normal(3.5*rate,8)		
			black_list.append(black)
			
		if to_do_list[1]:				
			black = Black_rush(6*rate,18)		
			black_list.append(black)


		if to_do_list[2]:				
			black = Black_geyser(0,10)		
			flag = True
			while black.check_init_distance(black_list):
				if black.renew_times>2: #多次重置失败,放弃
					flag = False
					break
			if flag:		
				black_list.append(black)

		if to_do_list[3]:								
			black = Black_excite(0.5*rate,8)		
			black_list.append(black)
			
		if to_do_list[4]:				
			black = Black_split(2.5*rate,7)		
			black_list.append(black)
		

	def cd_add(self,name):
		#增加对应怪物的冷却时间
		
		cd_add = {'black_normal':100,'black_rush':500,'black_geyser':0,'black_excite':200,'black_split':500}
		
		self.cd_replenish[name]+=cd_add[name]+random.randint(-50,50)

		#增加难度
		if random.randint(0,3):
			self.max_number[name]+=1

			
		
class Black():
	
	def __init__(self,speed,max_blood):
		
		if random.randint(0,1):
			random_x = random.randint(-1800,-100)
		else:
			random_x = random.randint(1000,2700)
			
		if random.randint(0,1):
			random_y = random.randint(-1200,-100)
		else:
			random_y = random.randint(700,1800)			
			
		self.pos = [random_x,random_y]
		self.time_keep_one_direction = 0
		self.direction = [0,0]
		self.speed = speed
		self.black_points_list = [[self.pos,0,True] for i in range(12)]
		self.max_blood = max_blood
		self.blood = self.max_blood
		self.color = [50,50,50]
		self.radius = 40
		
		
	
	def show_itself(self,settings,screen):	
		for i in range(len(self.black_points_list)):
		
			if (self.black_points_list[i][1]<=0) and self.black_points_list[i][2]: 
				self.black_points_list[i][1]=random.randint(2,2+self.blood)
				self.black_points_list[i][0]=[self.pos[0]+random.randint(-25,25),self.pos[1]+random.randint(-25,25)]
				
			else:
				self.black_points_list[i][1]-=0.6
			
			if int(self.black_points_list[i][1])>0:
				_pos = [int(self.black_points_list[i][0][0]),int(self.black_points_list[i][0][1])]	
				pygame.draw.circle(screen,self.color,_pos,int(self.black_points_list[i][1]),0)
		
	
	def change_direction(self,settings):
		
		if self.time_keep_one_direction>0:
			self.time_keep_one_direction -= 1
			
		else:	
		
			direction = vector_unitize([settings.screen_width*0.5-self.pos[0],settings.screen_height*0.5-self.pos[1]])
		
			random_x = random.uniform(-1,1)
			random_y = (1 - random_x**2)**0.5
			if random.randint(0,1):
				random_y *= -1
			
			self.direction = vector_unitize([direction[0]+0.5*random_x,direction[1]+0.5*random_y])
			
			
			self.time_keep_one_direction = random.randint(50,150)
	
	
		
		
	def move(self,):
		
		self.pos[0] += self.direction[0]*self.speed
		self.pos[1] += self.direction[1]*self.speed
		
	
	def lose_blood_and_die_check(self,number,shoot,damage):
		#扣血时判定
		
		if damage>0:
			#稍微变色
			if shoot.type=='red':
				self.color[0] += damage*5
			elif shoot.type=='green':	
				self.color[1] += damage*5
			elif shoot.type=='blue':	
				self.color[1] += damage
				self.color[2] += damage*5
			elif shoot.type=='yellow':	
				self.color[0] += damage*5
				self.color[1] += damage*5
			elif shoot.type=='cyan':	
				self.color[1] += damage*5
				self.color[2] += damage*5
			elif shoot.type=='purple':	
				self.color[0] += damage*5
				self.color[2] += damage*5
			
			
			
		'''
		#减少黑粒数目
		for _ in range(number):
			
			for i in range(len(self.black_points_list)):				
				if self.black_points_list[i][2]:
					#self.black_points_list[i][2] = False
					break
		'''

		#击退
		self.pos[0]+=1*shoot.direction[0]
		self.pos[1]+=1*shoot.direction[1]
		
		if shoot.type=='blue':
			self.direction[0]*=0.95
			self.direction[1]*=0.95
		elif shoot.type=='cyan':
			self.direction[0]*=0.8
			self.direction[1]*=0.8	
		elif shoot.type=='purple':			
			self.pos[0]+=10*shoot.direction[0]
			self.pos[1]+=10*shoot.direction[1]
			self.direction[0]+=0.01*shoot.direction[0]
			self.direction[1]+=0.01*shoot.direction[1]
		
		#死亡判定
		if self.blood<=0:
			return True
			
	
	def check_kill_player(self,settings,game):
		
		if ((self.pos[0]-settings.screen_width*0.5)**2+(self.pos[1]-settings.screen_height*0.5)**2)<=(40+self.radius)**2:
			
			game.game_status = 'game_over'
		



class Black_normal(Black):	
	def __init__(self,*args):
	
		super().__init__(*args)
		self.name = 'black_normal'


		
class Black_rush(Black):	
	def __init__(self,*args):
	
		super().__init__(*args)
		self.name = 'black_rush'
		self.set_up_time = 0
		self.radius = 45
	
	
	def move(self,):
		if self.set_up_time<=0:
			self.pos[0] += self.direction[0]*self.speed
			self.pos[1] += self.direction[1]*self.speed
		else:
			self.set_up_time-=1
	
			
	def change_direction(self,settings):
		
		if self.time_keep_one_direction>0:
			self.time_keep_one_direction -= 1			
		else:			
			direction = vector_unitize([settings.screen_width*0.5-self.pos[0],settings.screen_height*0.5-self.pos[1]])
		
			random_x = random.uniform(-1,1)
			random_y = (1 - random_x**2)**0.5
			if random.randint(0,1):
				random_y *= -1
			
			self.direction = vector_unitize([direction[0]+0.1*random_x,direction[1]+0.1*random_y])
			
			
			self.time_keep_one_direction = random.randint(200,300)
			self.set_up_time = random.randint(40,50)
			
		
		
		
	def show_nucleon(self,screen):
		
		color = self.color[:]
		if self.set_up_time>0:
			color[0]+=50
			color[1]+=50
			color[2]+=50
	
	
		_pos = [int(self.pos[0])+random.randint(-2,2),int(self.pos[1])+random.randint(-2,2)] 
		
		pygame.draw.circle(screen,color,_pos,24,0)
		pygame.draw.circle(screen,color,_pos,26,1)
		
		


class Black_geyser(Black):	
	def __init__(self,*args):
	
		super().__init__(*args)
		self.name = 'black_geyser'
		self.color_1 = [50,50,50]
		self.color_2 = [150,150,150]
		self.color_3 = [180,180,180]
		
		self.cumulative_time = 0
		self.erupt_time = 16
		self.stop_time = random.randint(140,160)
		self.renew_times = 0
		self.status = 'cumulate'
		self.black_points_list = []
		
	
	def check_init_distance(self,black_list):
		#距离过近,返回真
		for i in black_list:
			if i.name=='black_geyser':
				if abs(self.pos[0]-i.pos[0])<300 or abs(self.pos[1]-i.pos[1])<300:
					self.renew_init_pos()
					self.renew_times += 1
					return True
		
		
	def renew_init_pos(self):	
		if random.randint(0,1):
			random_x = random.randint(-1800,-100)
		else:
			random_x = random.randint(1000,2700)
			
		if random.randint(0,1):
			random_y = random.randint(-1200,-100)
		else:
			random_y = random.randint(700,1800)			
			
		self.pos = [random_x,random_y]


			
	def cumulate_time(self,):	
		if self.status=='cumulate':
			
			if self.cumulative_time<self.erupt_time:
				self.cumulative_time+=0.1
			else:	
				self.cumulative_time+=5
			
			if self.cumulative_time>=self.stop_time: 
				self.status = 'no_cumulate' #状态切换
				
				
		else:
		
			if self.cumulative_time>self.erupt_time:
				self.cumulative_time-=0.8
			else:	
				self.cumulative_time-=0.3
		
			if self.cumulative_time<=1: 
				self.status = 'cumulate' #状态切换
		
		
	def show_itself(self,settings,screen):	
		
		_pos = [int(self.pos[0]),int(self.pos[1])] 
		
		if int(self.cumulative_time)>=1:
			pygame.draw.circle(screen,self.color_2,_pos,int(self.cumulative_time),0)
		pygame.draw.circle(screen,self.color_1,_pos,self.erupt_time,5)
		if int(self.cumulative_time)>=1:
			if self.cumulative_time>self.erupt_time:
				pygame.draw.circle(screen,self.color_3,_pos,int(self.cumulative_time)+1,2)
				
		
		
	def lose_blood_and_die_check(self,number,shoot,damage):
		self.status = 'no_cumulate'
		self.cumulative_time -= 5
		
		
	def replenish_radius(self,):
		self.radius = self.cumulative_time


class Black_excite(Black):	
	def __init__(self,*args):
	
		super().__init__(*args)
		self.name = 'black_excite'
		
		self.excite_time = 0
		self.add_rate = 12
		self.check_radius = 75
		
	def check_excite(self,settings,shoots_list,):	
		#亢奋加速状态判定
		
		for x in shoots_list:
			
			if ((self.pos[0]-x.pos[0])**2+(self.pos[1]-x.pos[1])**2)<=self.check_radius**2:
				self.excite_time = random.randint(40,80)
				break
				
		if ((self.pos[0]-settings.screen_width*0.5)**2+(self.pos[1]-settings.screen_height*0.5)**2)<=(2*self.check_radius)**2 :
			self.excite_time = random.randint(40,80)
			

	def exciting_move(self,settings):
		
		add = 1
		if self.excite_time>0:
			self.excite_time-=1
			add = self.add_rate
			for _ in range(5):
				self.change_direction(settings)
		
		self.pos[0] += self.direction[0]*self.speed*add
		self.pos[1] += self.direction[1]*self.speed*add	
	
	
	def show_nucleon(self,screen):
		
		if self.excite_time>0:
			color = self.color
		else:
			color = [self.color[0]+40,self.color[1]+40,self.color[2]+40]
	
	
		_pos = [int(self.pos[0]),int(self.pos[1])] 
		
		pygame.draw.circle(screen,color,_pos,20,0)
	



class Black_split(Black):	
	def __init__(self,*args):
	
		super().__init__(*args)
		self.name = 'black_split'
		self.cumulative_time = 100
		self.split_time = 450
		self.max_split_times = 3
		self.radius = 35
		
		
	
	def cumulate(self,black_list):
		if self.cumulative_time>=self.split_time:
			self.cumulative_time = random.randint(0,100)
			self.max_split_times -=1	
			black = Black_split(self.speed,self.blood)
		
			black.pos[0] = self.pos[0]+random.randint(-5,5)
			black.pos[1] = self.pos[1]+random.randint(-5,5)
			black.color = self.color[:]
			black_list.append(black)
			
		else:
			if self.max_split_times>=1:
				self.cumulative_time+=1
	
	
	def show_nucleon(self,screen):
		
		pygame.draw.ellipse(screen,self.color,[self.pos[0],self.pos[1],2+28*(self.cumulative_time/self.split_time),30],0)
		#pygame.draw.circle(screen,color,[self.pos[0],self.pos[1]],20,0)
		
			
class Shoots():	
	
	def __init__(self,type,pos,direction,speed,damage,radius):
		self.type = type
		self.pos = pos
		self.radius = radius
		self.direction = direction
		self.speed = speed
		self.damage = damage
		
		
		self.record = [0,[0,0]] #时间,坐标
	
	def show_itself(self,settings,screen):	
		if self.type=='red':
			pygame.draw.circle(screen,[190,130,130],[int(self.pos[0])+random.randint(-1,1),int(self.pos[1])+random.randint(-1,1)],random.randint(10,11),0)		
			pygame.draw.circle(screen,[140,80,80],[int(self.pos[0])+random.randint(-1,1),int(self.pos[1])+random.randint(-1,1)],random.randint(8,9),0)
		
		
		elif self.type=='green':	
			for i in self.points:
				if i[1]<1:
					i[0] = [self.pos[0],self.pos[1]]
					i[1] = len(self.points)*3
				
				pygame.draw.circle(screen,[50,150-5*i[1],50],[int(i[0][0]),int(i[0][1])],i[1],0)
				i[1]-=1
			
			
			
		elif self.type=='blue':			
			
			for i in self.points:
				if i[1]<1:
					i[0] = [self.pos[0]+random.randint(-40,40),self.pos[1]+random.randint(-40,40)]
					i[1] = len(self.points)*3
			
				pygame.draw.circle(screen,[40,180-2*i[1],230],[int(i[0][0]),int(i[0][1])],i[1]//6,0)
					
				i[1]-=1
					
					
			
		elif self.type=='yellow':
			for i in self.points:
				if i[1]<1:
					i[0] = [self.pos[0],self.pos[1]]
					i[1] = len(self.points)*3
			
				pygame.draw.circle(screen,[180,190-3*i[1],30],[int(i[0][0]),int(i[0][1])],int(i[1]+2*self.speed//4),0)
				i[1]-=1
			
			
			
			
		elif self.type=='cyan':
			pygame.draw.circle(screen,[60,200,190],[int(self.pos[0])+random.randint(-1,1),int(self.pos[1])+random.randint(-1,1)],random.randint(8,9),0)		
			pygame.draw.circle(screen,[40,175,160],[int(self.pos[0])+random.randint(-2,2),int(self.pos[1])+random.randint(-2,2)],3,1)	

		elif self.type=='purple':
			pygame.draw.circle(screen,[120,30,110],[int(self.pos[0]),int(self.pos[1])],24,4)		
			pygame.draw.circle(screen,[80,10,70],[int(self.pos[0]),int(self.pos[1])],19,0)	
			
		
	def fly(self):
		
		self.pos[0] += self.direction[0]*self.speed
		self.pos[1] += self.direction[1]*self.speed
		
		if self.type=='yellow':
			self.speed+=0.22
			self.damage = 1+self.speed//4
			self.radius = 1+self.speed//4
			
		
	def impact_check(self,game,black_list,black_replenish):
		
		for i in reversed(black_list):
			
			if ((self.pos[0]-i.pos[0])**2+(self.pos[1]-i.pos[1])**2)<=(i.radius+self.radius)**2:
				
				i.blood -= self.damage
				if i.lose_blood_and_die_check(self.damage,self,self.damage):
					game.get_score(i)
					black_replenish.cd_add(i.name)
					black_list.remove(i)
					
				return True
			


	
		
class Player():
	
	def __init__(self):
		
		self.pos = [450,300]
		self.afterimage_points_list = [ [[450,300],0,True] for i in range(12) ] 
		
		self.prepare_shoots_type = 'red'
		self.shooting = False
		self.direction = [0,0]
		self.move_speed = 3
		self.shoot_cd = 0
		self.color = [150,90,90]
		
		
	def move(self,left_move,right_move,up_move,down_move,shoots_list,black_list,):		
		
		for i in shoots_list+black_list:
			if left_move:
				i.pos[0]+=self.move_speed
					
			if right_move:
				i.pos[0]-=self.move_speed
				
			if up_move:
				i.pos[1]+=self.move_speed
					
			if down_move:
				i.pos[1]-=self.move_speed
				
				
		for shoot in shoots_list:
			if shoot.type=='blue' or shoot.type=='yellow' or shoot.type=='green':
				for i in shoot.points:
					if left_move:
						i[0][0]+=self.move_speed
							
					if right_move:
						i[0][0]-=self.move_speed
						
					if up_move:
						i[0][1]+=self.move_speed
							
					if down_move:
						i[0][1]-=self.move_speed
		
		
		
		for x in black_list:
			
			for i in range(len(x.black_points_list)):
				if left_move:
					x.black_points_list[i][0][0]+=self.move_speed
					
				if right_move:
					x.black_points_list[i][0][0]-=self.move_speed
					
				if up_move:
					x.black_points_list[i][0][1]+=self.move_speed
						
				if down_move:
					x.black_points_list[i][0][1]-=self.move_speed
			
		
		
		
		for i in range(len(self.afterimage_points_list)):
			if left_move:
				self.afterimage_points_list[i][0][0]+=self.move_speed
				
			if right_move:
				self.afterimage_points_list[i][0][0]-=self.move_speed
				
			if up_move:
				self.afterimage_points_list[i][0][1]+=self.move_speed
					
			if down_move:
				self.afterimage_points_list[i][0][1]-=self.move_speed
		
		
		'''
		print(self.pos  ,  self.afterimage_points_list[0][0][0]  ,  self.afterimage_points_list[1][0][0])
		self.afterimage_points_list[1][0][0]+=0.5
		print(self.pos  ,  self.afterimage_points_list[0][0][0]  ,  self.afterimage_points_list[1][0][0])
		print("`````````")
		
		'''
	def shoot_cd_decrease(self,): 
		if self.shoot_cd>0:
			self.shoot_cd-=1
			
			
	def change_shoots_type(self,direc):		
		#改变子弹类型
		list = ['red','yellow','green','cyan','blue','purple']
		if direc=='r':
			if self.prepare_shoots_type==list[-1]:
				self.prepare_shoots_type=list[0]
			else:
				self.prepare_shoots_type=list[list.index(self.prepare_shoots_type)+1]
		elif direc=='l':
			if self.prepare_shoots_type==list[0]:
				self.prepare_shoots_type=list[-1]
			else:
				self.prepare_shoots_type=list[list.index(self.prepare_shoots_type)-1]
			

	def shoot(self,settings,direction,shoots_list):
		#射击
		if self.shoot_cd>0:
			return 0
			
		if self.prepare_shoots_type=='red':
			self.red_shoot(settings,direction,shoots_list)
		
		elif self.prepare_shoots_type=='green':		
			self.green_shoot(settings,direction,shoots_list)
			
		elif self.prepare_shoots_type=='blue':		
			self.blue_shoot(settings,direction,shoots_list)
			
		elif self.prepare_shoots_type=='yellow':		
			self.yellow_shoot(settings,direction,shoots_list)
			
		elif self.prepare_shoots_type=='cyan':		
			self.cyan_shoot(settings,direction,shoots_list)

		elif self.prepare_shoots_type=='purple':		
			self.purple_shoot(settings,direction,shoots_list)



	def red_shoot(self,settings,direction,shoots_list):				
		
		self.shoot_cd += 50
		for i in range(random.randint(3,5)):
			
			random_x = random.uniform(-1,1)
			random_y = (1 - random_x**2)**0.5
			if random.randint(0,1):
				random_y *= -1
			
			direction = vector_unitize([direction[0]+0.15*random_x,direction[1]+0.15*random_y])				
			
			pos = [settings.screen_width*0.5+direction[0]*random.randint(40,60),settings.screen_height*0.5+direction[1]*random.randint(40,60)]
		
			speed = random.randint(5,9)
			
			shoot = Shoots('red',pos,direction,speed,2,1)
			
			shoots_list.append(shoot)			
				

	def green_shoot(self,settings,direction,shoots_list):
		#高频率的快速攻击,伤害低
		
		self.shoot_cd += 10
		direction = vector_unitize([direction[0],direction[1]])				
			
		speed = 12
			
		pos = [settings.screen_width*0.5+direction[0]*40,settings.screen_height*0.5+direction[1]*40]
		
		shoot = Shoots('green',pos,direction,speed,3,1)
		shoot.points = [[[-100,-100],3*i] for i in range(3)] #坐标+时间,[-100,100]本身没有任何意义
		shoots_list.append(shoot)			
		
	
	def blue_shoot(self,settings,direction,shoots_list):
		#范围冰冻,没有伤害
	
		
		self.shoot_cd += 16
		
			
		random_x = random.uniform(-1,1)
		random_y = (1 - random_x**2)**0.5
		if random.randint(0,1):
			random_y *= -1
		
		direction = vector_unitize([direction[0]+0.13*random_x,direction[1]+0.13*random_y])
		
		pos = [settings.screen_width*0.5+direction[0]*random.randint(30,80),settings.screen_height*0.5+direction[1]*random.randint(30,80)]	
				
		speed = 4
		
		shoot = Shoots('blue',pos,direction,speed,0,35)
	
		shoot.points = [[[-100,-100],3*i] for i in range(16)] #坐标+时间
	
		shoots_list.append(shoot)	
			
			

	def yellow_shoot(self,settings,direction,shoots_list):
		#高频率,子弹会花费一点时间进行加速并提升威力
	
		self.shoot_cd += 10
		direction = vector_unitize([direction[0],direction[1]])				
			
		speed = 1.5
			
		pos = [settings.screen_width*0.5+direction[0]*40,settings.screen_height*0.5+direction[1]*40]
		
		shoot = Shoots('yellow',pos,direction,speed,1,1)
		shoot.points = [[[-100,-100],3*i] for i in range(3)] #坐标+时间
		shoots_list.append(shoot)			
		
	
	
	def cyan_shoot(self,settings,direction,shoots_list):
		#快速攻击,伤害低,附带冻结
	
		self.shoot_cd += 6
			
		random_x = random.uniform(-1,1)
		random_y = (1 - random_x**2)**0.5
		if random.randint(0,1):
			random_y *= -1
		
		direction = vector_unitize([direction[0]+0.25*random_x,direction[1]+0.25*random_y])
		
		pos = [settings.screen_width*0.5+direction[0]*random.randint(30,80),settings.screen_height*0.5+direction[1]*random.randint(30,80)]	
				
		speed = random.randint(7,10)
		
		shoot = Shoots('cyan',pos,direction,speed,1,1)
		
		shoots_list.append(shoot)		
	
	
	
	def purple_shoot(self,settings,direction,shoots_list):	
		
		self.shoot_cd += 30
		
		random_x = random.uniform(-1,1)
		random_y = (1 - random_x**2)**0.5
		if random.randint(0,1):
			random_y *= -1
		
		random_direction = [random_x,random_y]
		direction = vector_unitize([direction[0]+0.05*random_x,direction[1]+0.05*random_y])
		
		
		pos = [settings.screen_width*0.5+direction[0]*random.randint(40,60),settings.screen_height*0.5+direction[1]*random.randint(40,60)]
	
		speed = 4
		
		shoot = Shoots('purple',pos,direction,speed,0,10)
		shoot.random_direction = random_direction
		shoots_list.append(shoot)	
	
	
	
	
	
	def show_myself(self,settings,screen,game):
		#绘画自身
		
		if game.game_status!='game_over':
			#变色
			dict = {'red':[150,90,90],'yellow':[200,210,50],'green':[50,175,50],'cyan':[70,210,220],'blue':[50,115,190],'purple':[160,85,180],}
			
			if self.prepare_shoots_type in dict.keys():
				for i in range(3):
					if self.color[i]>dict[self.prepare_shoots_type][i]:
						self.color[i]-=1
					elif self.color[i]<dict[self.prepare_shoots_type][i]:
						self.color[i]+=1
			
		
		_pos = [int(self.pos[0]+5*self.direction[0]),int(self.pos[1]+5*self.direction[1])]
		pygame.draw.circle(screen,self.color,_pos,int(40),5)	
		
		_pos = [int(self.pos[0]+10*self.direction[0]),int(self.pos[1]+10*self.direction[1])] #移动时微微倾斜
		if int(4.2*self.shoot_cd**0.5)>2:
			pygame.draw.circle(screen,self.color,_pos,int(4.2*self.shoot_cd**0.5),2)
		
		
	def show_afterimage(self,settings,screen,left_move,right_move,up_move,down_move):	
		#残影
		for i in range(len(self.afterimage_points_list)):
		
			if (self.afterimage_points_list[i][1]<=0) and self.afterimage_points_list[i][2]: 
				self.afterimage_points_list[i][1]=random.randint(6,12)
				
				if left_move:
					self.direction[0]=-1
				if right_move:
					self.direction[0]=1
				if up_move:	
					self.direction[1]=-1
				if down_move:
					self.direction[1]=1
				
				if self.direction==[0,0]:
					pass
				else:
					self.direction = vector_unitize(self.direction)
				distance = 40
				self.afterimage_points_list[i][0]=[self.pos[0]+random.randint(-25,25)-distance*self.direction[0],self.pos[1]+random.randint(-25,25)-distance*self.direction[1]]
				
			else:
				self.afterimage_points_list[i][1]-=0.5
			
			if int(self.afterimage_points_list[i][1])>0:
				_pos = [int(self.afterimage_points_list[i][0][0]),int(self.afterimage_points_list[i][0][1])]	
				pygame.draw.circle(screen,self.color,_pos,int(self.afterimage_points_list[i][1]),0)
				
				
	def show_color_turntable(self,screen):
		list = ['red','yellow','green','cyan','blue','purple']
		number = 19+list.index(self.prepare_shoots_type)
	
		pic =  pygame.image.load('images/小图标/'+str(number)+'.bmp')
		rect = pic.get_rect()	
		rect.bottomleft = [0,600]
		screen.blit( pic,rect )
		
		
	
class Image():
	
	def __init__(self):
		self.turn_rect_list = [i for i in range(20)]
		
		self.menu_logo_pointed = False
	
		self.afterimage = [i for i in range(12)]
		

	def show_backpic(self,settings,screen,game_time):
		#背景
		
		number = (int(game_time*0.65))%26 + 1  # 1~16 17~32
		
		if number<14:
			pass
		else:
			number = 27-number
		
		back_pic =  pygame.image.load('images/双子/'+str(number)+'.bmp')
		back_rect = back_pic.get_rect()	
		
		screen.blit( back_pic,[0,0] )

	
		
	
	
	def show_white(self,settings,screen,gaming_time):
		#模糊背景
		
		if gaming_time<26:
			number = gaming_time%26 + 1 
		else:
			number = 26
		
		back_pic =  pygame.image.load('images/白/'+str(number)+'.bmp')
		
		back_rect = back_pic.get_rect()	
		
		screen.blit( back_pic,[0,0] )


	def show_title_pic(self,screen):
		#背景
		
		pic =  pygame.image.load('images/小图标/27.bmp')
		rect = pic.get_rect()	
		rect.center = [600,100]
		screen.blit( pic,rect )

	
	def show_little_white(self,screen):
		#死亡时小白框
		pic =  pygame.image.load('images/未分类/4.bmp')
		rect = pic.get_rect()	
		rect.center = [450,300]
		screen.blit( pic,rect )
	
	
	
	
	def show_suspend_gray(self,settings,screen):
		#暂停的灰色背景
		
		back_pic =  pygame.image.load('images/未分类/1.bmp')
		
		back_rect = back_pic.get_rect()	
		
		screen.blit( back_pic,[0,0] )
		
		
	def show_menu_logo(self,settings,screen):
		#返回键
		if self.menu_logo_pointed:
			back_pic =  pygame.image.load('images/小图标/1.bmp')			
		else:	
			back_pic =  pygame.image.load('images/小图标/2.bmp')
		
		back_rect = back_pic.get_rect()	
		
		screen.blit( back_pic,[10,10] )

		self.turn_rect_list[2] = back_rect

	
	def show_rules_pic(self,screen):	
		pic =  pygame.image.load('images/未分类/3.bmp')
		rect = pic.get_rect()
		screen.blit( pic,[0,0] )
		
		pic =  pygame.image.load('images/未分类/2.bmp')
		rect = pic.get_rect()
		rect.center = [450,300]
		screen.blit( pic,rect )
		
		
	

	def show_font(self,screen,content,font_pos,mouse_x,mouse_y,game):
		#绘画字

		font = pygame.font.SysFont('SimHei',35)	
		s = font.render((content),True,[0,0,0])
		turn_rect = s.get_rect()
		turn_rect.bottomleft = font_pos
		
		#碰撞变色
		if if_collidepoint(turn_rect,mouse_x,mouse_y):
			color = [180,170,150]
			font_pos[0] += 15
		else:
			color = [100,100,100]
		
		s = font.render((content),True,color)
		turn_rect = s.get_rect()		
		turn_rect.bottomleft = font_pos
		
		#绘制
		screen.blit(s,turn_rect)
		
		if content=="开始游戏":
			self.turn_rect_list[0] = turn_rect
		elif content=="退出游戏":
			self.turn_rect_list[1] = turn_rect
		elif content=="继续游戏":
			self.turn_rect_list[3] = turn_rect
		elif content=="退回主菜单":
			self.turn_rect_list[4] = turn_rect
		elif content=="直接退出":
			self.turn_rect_list[5] = turn_rect
			
		elif content=="返回主菜单":
			self.turn_rect_list[6] = turn_rect
		elif content=="结束游戏":
			self.turn_rect_list[7] = turn_rect
			
		elif content=="游戏规则":
			self.turn_rect_list[8] = turn_rect
		elif content==game.game_difficulty:
			self.turn_rect_list[9] = turn_rect
			

class Settings():
	
	def __init__(self):
	
		#帧数
		self.fps_number = 80
		
		#屏幕大小
		self.screen_width=900
		self.screen_height=600		
		


def vector_unitize(vector):
	k = (1/(vector[0]**2+vector[1]**2))**0.5
	new_vector = [0,0]
	new_vector[0] = k*vector[0]
	new_vector[1] = k*vector[1]
	return new_vector
	



def if_collidepoint(turn_rect,mouse_x,mouse_y):

	if turn_rect.collidepoint(mouse_x,mouse_y):
		return True





main()

