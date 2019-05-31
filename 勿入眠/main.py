
import pygame,sys,time,random,math,settings_file

settings = settings_file.Settings()

		
def main():

	# 初始化pygame
	pygame.init()

	
	# 创建pygame显示层
	screen = pygame.display.set_mode( (settings.screen_width,settings.screen_height) )
	pygame.display.set_caption('勿入眠')


	#设置的相关内容
	setting_rect_list = [settings.screen_width*0.4,settings.screen_height*0.4,settings.screen_width*0.2,settings.screen_height*0.2]
	
	die_rect_list_1 = [settings.screen_width*0.35,settings.screen_height*0.35,settings.screen_width*0.3,settings.screen_height*0.3]	
	die_rect_list_2 = [settings.screen_width*0.32,settings.screen_height*0.32,settings.screen_width*0.36,settings.screen_height*0.36]
			
	setting_rect = pygame.Rect(setting_rect_list)
	die_rect_1 = pygame.Rect(die_rect_list_1) 
	die_rect_2 = pygame.Rect(die_rect_list_2) 
	
	
	start_game = False
	walk_down = False
	walk_left = False
	walk_right = False
	walk_up = False
	die = False
	
	the_time = 0
	list_obj = [["child",0.5*settings.screen_width ,0.5*settings.screen_height ]]
	list_me = ["child",int(0.5*settings.screen_width ),int(0.5*settings.screen_height )]
	x_move = 0
	y_move = 0
	sleep = 0
	groundcolor_of_now=list(settings.groundcolor)
	chlid_pic = pygame.image.load('images/child_down.bmp')
	fright_pic =  pygame.image.load('images/fright.bmp')
	
	pre_x_y = (0.5*settings.screen_width ,0.5*settings.screen_height)
	q= 0
	hit_by_flower = 0
	while True:
		if not start_game:
			

			# 绘制pygame显示层
			screen.fill(settings.start_groundcolor)	
			

			#绘画设置框框
			pygame.draw.rect( screen,settings.setting_rect_color,setting_rect,2 )
			
			#开始画面的字
			font = pygame.font.SysFont('SimHei',40)		
			s = font.render(("开始游戏"),True,settings.start_font_color)
			turn_rect = s.get_rect()
			turn_rect.center = (0.5*settings.screen_width ,0.5*settings.screen_height)
			screen.blit(s,turn_rect)			
	
			for event in pygame.event.get():
			
				if event.type == pygame.QUIT:
					sys.exit()		
					
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_x,mouse_y=pygame.mouse.get_pos()
					
					#点击开始按钮
					if setting_rect.collidepoint(mouse_x,mouse_y) :
						start_game = True			
						
			
		else:
	
	
			if the_time==0:
				
				for x in range(0,settings.world_width,100): 
					for y in range(0,settings.world_height,100):
					
						number = random.randint(1,17)
						
						if not distance_check( (x-0.5*settings.world_width,y-0.5*settings.world_height) ,(list_me[1],list_me[2]),300):
						
							if (number == 1) :
								
								#添加一个灯
								number_x_change = random.randint(-10,10)
								number_y_change = random.randint(-10,10)
								
								new_list_obj = ["lamp",x+number_x_change-0.5*settings.world_width,y+number_y_change-0.5*settings.world_height]
								list_obj.append(new_list_obj)
					
				#灯密度修正
				for x in range(0,settings.world_width,300): 
					for y in range(0,settings.world_height,300):
						number_of_lamp = 0
						for i in list_obj:
							if distance_check( (i[1],i[2]) ,(x,y),1000):
								number_of_lamp +=1
								if number_of_lamp >= 25 and i[0]!="child":
									list_obj.remove(i)
		

						#一定时间后
			if the_time==150:
				
				for i in list_obj:
					number = random.randint(1,15)
				
					if number==1 and (i[0]=="lamp"):
						
							#添加一只鬼火
						number_x_change = random.randint(-30,30)
						number_y_change = random.randint(1,30)
							
						new_list_obj = ["ghost",i[1]+number_x_change,i[2]+number_y_change,0,0,0]
						list_obj.append(new_list_obj)	
						

				
			if the_time==4500:	
				#出现惊悚
				#加大难度
				number_x_change = random.randint(-0.5*settings.world_width,0.5*settings.world_width)
				number_y_change = random.randint(-0.5*settings.world_height,0.5*settings.world_height)
				
				if distance_check((number_x_change,number_y_change),(list_me[1],list_me[2]),800):
					number_x_change = random.randint(-0.5*settings.world_width,0.5*settings.world_width)
					number_y_change = random.randint(-0.5*settings.world_height,0.5*settings.world_height)					
				new_list_obj = ["fright",number_x_change,number_y_change,0]
				list_obj.append(new_list_obj)	
				print(new_list_obj)

			if the_time%1300==400:
				#添加一朵花
				#加大难度				
				number_x_change = random.randint(-0.5*settings.world_width,0.5*settings.world_width)
				number_y_change = random.randint(-0.5*settings.world_height,0.5*settings.world_height)
				
				if distance_check((number_x_change,number_y_change),(list_me[1],list_me[2]),1000):
					number_x_change = random.randint(-0.5*settings.world_width,0.5*settings.world_width)
					number_y_change = random.randint(-0.5*settings.world_height,0.5*settings.world_height)

					
				new_list_obj = ["flower",number_x_change,number_y_change,0]
				list_obj.append(new_list_obj)	
				
			
			if the_time%2300==300:
				#眼球
				#加大难度
				number_x_change = random.randint(-0.5*settings.world_width,0.5*settings.world_width)
				number_y_change = random.randint(-0.5*settings.world_height,0.5*settings.world_height)
				
				if distance_check((number_x_change,number_y_change),(list_me[1],list_me[2]),800):
					number_x_change = random.randint(-0.5*settings.world_width,0.5*settings.world_width)
					number_y_change = random.randint(-0.5*settings.world_height,0.5*settings.world_height)
					
				new_list_obj = ["eye",number_x_change,number_y_change,0,[0,0]]
				
				new_list_obj[1] = 0
				new_list_obj[2] =0
				
				list_obj.append(new_list_obj)					
				
				
			
			if not die:		
				the_time+=1
			
			
			
			#事件
			for event in pygame.event.get():
			
				if event.type == pygame.QUIT:
					sys.exit()					
					
				elif event.type == pygame.KEYUP :
					if event.key == pygame.K_RIGHT or event.key == ord('d'):
						walk_right = False
						
					if event.key == pygame.K_LEFT or event.key == ord('a'):
						walk_left = False
					
					if event.key == pygame.K_UP or event.key == ord('w'):
						walk_up = False
						
					if event.key == pygame.K_DOWN or event.key == ord('s'):
						walk_down = False						
						
				elif event.type == pygame.KEYDOWN and not die:
				
					if event.key == pygame.K_RIGHT or event.key == ord('d'):
						walk_right = True
						
					if event.key == pygame.K_LEFT or event.key == ord('a'):
						walk_left = True

					if event.key == pygame.K_UP or event.key == ord('w'):
						walk_up = True
						
					if event.key == pygame.K_DOWN or event.key == ord('s'):
						walk_down = True
					
				elif die and event.type == pygame.MOUSEBUTTONDOWN :
					mouse_x,mouse_y=pygame.mouse.get_pos()
					
					#点击开始按钮
					if die_rect_1.collidepoint(mouse_x,mouse_y) :
						main()		
				
				
				
			#行走
			if walk_down:
				y_move -= settings.walk_speed
				list_me[2] += settings.walk_speed
				chlid_pic=pygame.image.load('images/child_down.bmp')
				if the_time%4<=1:
					chlid_pic = pygame.transform.rotate(chlid_pic, 1)
				else:
					chlid_pic = pygame.transform.rotate(chlid_pic, -1)
				
			elif walk_up:

				y_move += settings.walk_speed
				list_me[2] -= settings.walk_speed
				
				chlid_pic=pygame.image.load('images/child_back.bmp')
				if the_time%2==0:
					chlid_pic = pygame.transform.rotate(chlid_pic, 1)
				else:
					chlid_pic = pygame.transform.rotate(chlid_pic, -1)					
			if walk_left:
				x_move += settings.walk_speed
				list_me[1] -= settings.walk_speed
				chlid_pic=pygame.image.load('images/child_left.bmp')
				if the_time%2==0:
					chlid_pic = pygame.transform.rotate(chlid_pic, 1)
				else:
					chlid_pic = pygame.transform.rotate(chlid_pic, -1)
				
			elif walk_right:
				x_move -= settings.walk_speed
				list_me[1] += settings.walk_speed
				chlid_pic=pic = pygame.transform.flip( pygame.image.load('images/child_left.bmp'), True, False)
				if the_time%2==0:
					chlid_pic = pygame.transform.rotate(chlid_pic, 1)
				else:
					chlid_pic = pygame.transform.rotate(chlid_pic, -1)				
				
		
				

			
			# 绘制pygame显示层
			screen.fill(groundcolor_of_now)				
			
			#背景色
			if sleep>0 and sleep<settings.groundcolor[0]-1:
				groundcolor_of_now[0] = int(settings.groundcolor[0] - sleep)
				groundcolor_of_now[1] = int(settings.groundcolor[1] - sleep)
				groundcolor_of_now[2] = int(settings.groundcolor[2] - sleep)
			if sleep>0:
				sleep -= 0.1
			if sleep>=settings.groundcolor[0]-1:
				die = True

			#紫色
			if hit_by_flower>0:
				hit_by_flower -=1

			#活跃生物的列表更新
			little_list_obj = []			
			for i in list_obj:
				if (distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.little_obj_distance)):
					little_list_obj.append(i)
			
			#超大范围追杀
			for i in list_obj:
				
				if i[0]=="fright":
					if i[3]>0:#显形阶段
						if i[1]>list_me[1]:
							i[1] -= settings.fright_no_hiding_speed
						elif i[1]<list_me[1]:						
							i[1] += settings.fright_no_hiding_speed

						if i[2]>list_me[2]:
							i[2] -= settings.fright_no_hiding_speed
						elif i[2]<list_me[2]:						
								i[2] += settings.fright_no_hiding_speed
						
						i[3] -= 1

						
					else:	#潜藏阶段
						if i[1]>list_me[1]:
							i[1] -= settings.fright_hiding_speed
						elif i[1]<list_me[1]:						
							i[1] += settings.fright_hiding_speed

						if i[2]>list_me[2]:
							i[2] -= settings.fright_hiding_speed
						elif i[2]<list_me[2]:						
								i[2] += settings.fright_hiding_speed
						
						#判定惊悚是否可以进入显形阶段
						if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.fright_no_hiding_distance):
							i[3] = settings.fright_min_no_hiding_time
					
				elif i[0]=="flower":
					#催眠
					if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.flower_danger_distance):
						sleep += settings.flower_sleep_speed
						if hit_by_flower<48:
							hit_by_flower += 2
						
					#接触
					if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.flower_touch_distance):
						sleep = 0	
						groundcolor_of_now[0] = int(settings.groundcolor[0] - sleep)
						groundcolor_of_now[1] = int(settings.groundcolor[1] - sleep)
						groundcolor_of_now[2] = int(settings.groundcolor[2] - sleep)
						list_obj.remove(i)
						hit_by_flower = 0
			
			
			#--------移动-----------
			for i in little_list_obj:
			
				#鬼火
				if i[0]=="ghost" :
					
					if i[5] == 0:
						if i[3]>0:
							if i[3]%4==0:
								i[1] += settings.ghost_random_speed
								i[3] -=2							
							elif i[3]%4==1:
								i[1] -= settings.ghost_random_speed
								i[3] -=2	
							else:
								i[3] -=2

						else:
							i[3] = random.randint(80,100)
							
						if i[4]>0:	
							
							if i[4]%4==0:
								i[2] += settings.ghost_random_speed
								i[4] -=2
							elif i[4]%4==1:
								i[2] -= settings.ghost_random_speed
								i[4] -=2	
							else:
								i[4] -=2
							
						else:
							i[4] = random.randint(80,100)
					
					#喜闻乐见的追杀模式					
					else:
						if i[1]>list_me[1]:
							i[1] -= settings.ghost_pursue_speed
						elif i[1]<list_me[1]:						
							i[1] += settings.ghost_pursue_speed

						if i[2]>list_me[2]:
							i[2] -= settings.ghost_pursue_speed
						elif i[2]<list_me[2]:						
							i[2] += settings.ghost_pursue_speed					
				#追击			
				if i[0]=="ghost":
				
					if i[5]==1:	
						if not distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.ghost_pursue_distance):
							i[5] = 0
							
					else:
						if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.ghost_perceive_distance):
						
							i[5] = 1
							
		

				elif i[0]=="eye":
					if i[3]==0:#可发动移动瞄准
						if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.eye_perceive_distance):
							i[3] -= settings.the_time_prepare
							i[4] = (0,list_me[1],list_me[2])
							
					elif i[3]<-1:#移动瞄准准备中
						i[3]+=1
						
					elif i[3]==-1:#移动瞄准发动
						i[1],i[2] = i[4][1],i[4][2]
						i[3] += settings.the_time_cd
						
					elif i[3]>0:
						i[3] -=1
						
				
				
				#--------撞鬼---------
				if i[0]=="lamp":
					if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.lamp_danger_distance):
						sleep += settings.lamp_sleep_speed
						
				if i[0]=="ghost":
					if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.ghost_danger_distance):
						sleep += settings.ghost_sleep_speed				
						
				elif i[0]=="fright":						
					if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.fright_danger_distance):
						sleep += settings.fright_sleep_speed

				elif i[0]=="eye":
					
					if distance_check((i[1],i[2]),(list_me[1],list_me[2]),settings.eye_danger_distance):
						sleep += settings.eye_sleep_speed	
						
						

							
			#玩家停下时逐渐沉睡	
			if the_time%4==0:
				if (pre_x_y)==(list_me[1],list_me[2]):
					sleep += settings.stop_sleep_speed
					
				pre_x_y = (list_me[1],list_me[2])
					
		
			#冒泡，让y值最大的沉底
			for i in range(len(little_list_obj)-1):
				for j in range(len(little_list_obj)-1-i):
					if (little_list_obj[j][2] > little_list_obj[j+1][2]):
						little_list_obj[j],little_list_obj[j+1] = little_list_obj[j+1],little_list_obj[j]
			
						
			
			for i in little_list_obj:
				if i[0]=="child":
					i[1]=list_me[1]
					i[2]=list_me[2]
			
			#生物的绘画		
			for i in little_list_obj:		
				if i[0]=="lamp":
					
					pic =  pygame.image.load('images/lamp.bmp')
					a_rect = pic.get_rect()
					
					screen.blit( pic,(int(i[1] + x_move - 0.5*a_rect.width),int(i[2] + y_move - 0.8*a_rect.height)) )	
					
					
				elif i[0]=="ghost":
					pic =  pygame.image.load('images/ghost.bmp')
					a_rect = pic.get_rect()
					
					screen.blit( pic,(int(i[1] + x_move - 0.5*a_rect.width),int(i[2] + y_move - 0.8*a_rect.height)) )	
				
				elif i[0]=="fright":
					if i[3]:#显形状态下才绘画
						if i[1]>list_me[1]:
							fright_pic = pygame.transform.flip( pygame.image.load('images/fright.bmp'), True, False)		
							
						a_rect = fright_pic.get_rect()
						
						screen.blit( fright_pic,(int(i[1] + x_move - 0.5*a_rect.width),int(i[2] + y_move - 0.8*a_rect.height)) )	
						
				elif i[0]=="flower":
					pic =  pygame.image.load('images/flower.bmp')
					a_rect = pic.get_rect()
					
					screen.blit( pic,(int(i[1] + x_move - 0.5*a_rect.width),int(i[2] + y_move - 0.8*a_rect.height)) )						
				elif i[0]=="eye":

					pic =  pygame.image.load('images/eye.bmp')
					a_rect = pic.get_rect()

					
					screen.blit( pic,(int(i[1] + x_move - 0.5*a_rect.width),int(i[2] + y_move - 0.8*a_rect.height)) )
								
					if i[3]<-1:
						
						if not (i[1]==i[4][1]):
							k = (i[4][2]-i[2])/(i[4][1]-i[1])
							x = (settings.eyeball_turn/(1+k*k))**0.5
							y = k*x
						if (i[1]<i[4][1]):
							pygame.draw.circle(screen,(10,10,10),(int(i[1] + x_move +x),int(i[2] + y_move - 0.3*a_rect.height +y)),12,0)
							
						elif (i[1]>i[4][1]):
							pygame.draw.circle(screen,(10,10,10),(int(i[1] + x_move -x),int(i[2] + y_move - 0.3*a_rect.height -y)),12,0)
							
						elif (i[1]==i[4][1]):
							if (i[2]>i[4][2]):
								pygame.draw.circle(screen,(10,10,10),(int(i[1] + x_move ),int(i[2] + y_move - 0.3*a_rect.height -settings.eyeball_turn**0.5)),12,0)
																
							elif (i[2]<i[4][2]):
								pygame.draw.circle(screen,(10,10,10),(int(i[1] + x_move ),int(i[2] + y_move - 0.3*a_rect.height +settings.eyeball_turn**0.5)),12,0)							
					else:
						pygame.draw.circle(screen,(10,10,10),(int(i[1] + x_move),int(i[2] + y_move - 0.3*a_rect.height)),12,0)	
						
				elif i[0]=="child":
					
					a_rect = chlid_pic.get_rect()
					screen.blit( chlid_pic,(int(list_me[1] + x_move - 0.5*a_rect.width),int(list_me[2] + y_move - 0.8*a_rect.height)) )	
					
			#得分显示		
			font = pygame.font.SysFont(None,50)		
			s = font.render(("score "+str(the_time//10)),True,settings.score_color)
			turn_rect = s.get_rect()
			turn_rect.midtop = (0.5*settings.screen_width ,25)
			screen.blit(s,turn_rect)					
						
			
			#墙	
			if (0.5*settings.world_width - list_me[1]) <= -200:
			
				font = pygame.font.SysFont('SimHei',35)		
				s = font.render("【这是你无法走出的边界】",True,settings.black_rect_color)
				turn_rect = s.get_rect()
				turn_rect.bottomleft = (30 ,settings.screen_height -30)
				screen.blit(s,turn_rect)
					
			elif (list_me[1] + 0.5*settings.world_width) <= -200:
			
				font = pygame.font.SysFont('SimHei',35)		
				s = font.render("【这是你无法走出的边界】",True,settings.black_rect_color)
				turn_rect = s.get_rect()
				turn_rect.bottomleft = (30 ,settings.screen_height -30)
				screen.blit(s,turn_rect)
				
			if (0.5*settings.world_height - list_me[2]) <= -200:
			
				font = pygame.font.SysFont('SimHei',35)		
				s = font.render("【这是你无法走出的边界】",True,settings.black_rect_color)
				turn_rect = s.get_rect()
				turn_rect.bottomleft = (30 ,settings.screen_height -30)
				screen.blit(s,turn_rect)
					
			elif (list_me[2] + 0.5*settings.world_height) <= -200:
			
				font = pygame.font.SysFont('SimHei',35)		
				s = font.render("【这是你无法走出的边界】",True,settings.black_rect_color)
				turn_rect = s.get_rect()
				turn_rect.bottomleft = (30 ,settings.screen_height -30)
				screen.blit(s,turn_rect)
		

		
			#墙的反弹
			if (0.5*settings.world_width - list_me[1]) <= -300:
				
				list_me[1] -= settings.walk_speed
				x_move += settings.walk_speed
			
			elif (list_me[1] + 0.5*settings.world_width) <= -300:
				
				list_me[1] += settings.walk_speed				
				x_move -= settings.walk_speed		
			
	
			if (0.5*settings.world_height - list_me[2]) <= -300:
				
				list_me[2] -= settings.walk_speed
				y_move += settings.walk_speed
			
			elif (list_me[2] + 0.5*settings.world_height) <= -300:
				
				list_me[2] += settings.walk_speed				
				y_move -= settings.walk_speed		
						
			
			#装饰用的框框
			list_decorate_rect = [10 ,10 ,settings.screen_width -20,settings.screen_height -20]
			decorate_rect = pygame.Rect(list_decorate_rect)
			if hit_by_flower<48:
				pygame.draw.rect(screen,(50,50 - hit_by_flower,50),decorate_rect,9)
			else:
				pygame.draw.rect(screen,(50,0,50),decorate_rect,10)				
			
			
			if die:
				#绘画设置框框
				pygame.draw.rect( screen,settings.die_rect_color,die_rect_1,0 )
				pygame.draw.rect( screen,settings.die_rect_color,die_rect_2,4 )			
				
				font = pygame.font.SysFont('SimHei',40)		
				s = font.render(("score "+str(the_time//10)),True,settings.die_score_color)
				turn_rect = s.get_rect()
				turn_rect.midbottom = (0.5*settings.screen_width ,0.5*settings.screen_height -5)
				screen.blit(s,turn_rect)	
				
				s = font.render(("你永眠于此"),True,settings.die_score_color)
				turn_rect = s.get_rect()
				turn_rect.midtop = (0.5*settings.screen_width ,0.5*settings.screen_height)
				screen.blit(s,turn_rect)					

		
		# 刷新pygame显示层
		pygame.display.flip()	

		clock = pygame.time.Clock()
		#初始化Clock对象
		time_passed = clock.tick()
		#返回上一个调用的时间（ms）
		time_passed = clock.tick(settings.fps_number)

		
		
		
		
def distance_check(one_xy,another_xy,st):
	if ( (one_xy[0] - another_xy[0])**2 + (one_xy[1] - another_xy[1])**2 <= st**2 ):
		return 1
	else:
		return 0


		
main()	
	



