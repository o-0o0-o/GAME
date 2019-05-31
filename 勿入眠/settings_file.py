class Settings():
	
	def __init__(self):
	
		#帧数
		self.fps_number = 75


		#游戏前的背景色
		self.start_groundcolor = (220,220,220)
		
		#开始字体
		self.start_font_color = (200,80,20)	
		
		#设置界面的框框色
		self.setting_rect_color = (150,50,50)
		
		#正常情况下的游戏中背景色
		self.groundcolor = (230,230,230)

		#score字的颜色
		self.score_color = (100,149,237)
		self.die_score_color = (30,30,30)
		
		#死亡后字显示颜色
		self.die_rect_color = (255,255,255)
		

		#其它字显示颜色
		self.black_rect_color = (20,20,20)
		
		#行走速度
		self.walk_speed = 14
		
		#屏幕大小
		self.screen_width=800
		self.screen_height=600	
		self.little_obj_distance = 1100		
		
		#游戏地图大小
		self.world_width = 10000
		self.world_height = 10000
		
		#停下
		self.stop_sleep_speed = 1.5
		
		#灯
		self.lamp_danger_distance = 100
		self.lamp_sleep_speed = 6
		

		#鬼火
		self.ghost_danger_distance = 75
		self.ghost_perceive_distance = 210
		self.ghost_pursue_distance = 270
		self.ghost_sleep_speed = 3
		self.ghost_random_speed = 7
		self.ghost_pursue_speed = 10.5
		
		
		#惊悚
		self.fright_hiding_speed = 4
		self.fright_no_hiding_speed = 1
		self.fright_sleep_speed = 6
		self.fright_no_hiding_distance = 85
		self.fright_danger_distance = 85
		self.fright_min_no_hiding_time = 35
		
		
		#花
		self.flower_touch_distance = 90
		self.flower_danger_distance = 1600
		self.flower_sleep_speed = 0.25
		
		
		#眼球
		self.eye_danger_distance = 140		
		self.eye_sleep_speed = 5
		self.eye_perceive_distance = 500
		self.the_time_prepare = 25
		self.the_time_cd = 20
		self.eyeball_turn = 95
		